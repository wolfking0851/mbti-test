#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
{IDENTITY_NAME} 通用任务执行器
身份：{IDENTITY_ID}
职责：动态任务执行（根据任务类型分配角色）
触发：Cron 每 5 分钟
"""

import json
import os
import sys
import subprocess
import requests
import fcntl
from datetime import datetime
from pathlib import Path

# ==================== 身份配置 ====================

IDENTITY_ID = "{IDENTITY_ID}"
IDENTITY_NAME = "{IDENTITY_NAME}"
ROLE = "动态任务执行者"

# ==================== 目录配置 ====================

WORKSPACE_DIR = Path("/home/admin/.openclaw/workspace")
TASKS_DIR = WORKSPACE_DIR / "team-tasks"
LOGS_DIR = WORKSPACE_DIR / "logs"

# ==================== 钉钉配置 ====================

DINGTALK_WEBHOOK = "{WEBHOOK}"

# ==================== API 配置 ====================

ALIBABA_API_KEY = "sk-6bcc79046f4a41d4b379f29480c0f07b"

# ==================== 超时配置 ====================

TASK_TIMEOUT_DEFAULT = 600  # 默认 10 分钟
MAX_RETRIES = 3

# ==================== 日志 ====================

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] [{IDENTITY_NAME}] [{level}] {message}"
    print(log_msg)
    
    # 写入日志文件
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / f"wawa-{IDENTITY_ID.split('-')[1]}.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

# ==================== 钉钉通知 ====================

def send_dingtalk_message(message, msg_type="text"):
    """发送钉钉消息"""
    try:
        response = requests.post(
            DINGTALK_WEBHOOK,
            json={
                "msgtype": msg_type,
                "text": {"content": message} if msg_type == "text" else None
            },
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('errcode') == 0:
                log(f"✅ 钉钉消息发送成功")
                return True
            else:
                log(f"❌ 钉钉 API 返回错误：{result}", "ERROR")
                return False
        else:
            log(f"❌ 钉钉 API 请求失败：{response.status_code}", "ERROR")
            return False
    except Exception as e:
        log(f"❌ 发送钉钉消息失败：{e}", "ERROR")
        return False

def send_task_started_notification(task):
    """发送任务开始通知"""
    message = f"""🔧 {IDENTITY_NAME} 任务开始

📝 任务：{task.get('task', 'Unknown')[:50]}
🎯 角色：{task.get('role', 'executor')}
⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

开始执行... 🚀"""
    send_dingtalk_message(message)

def send_task_complete_notification(task, result=""):
    """发送任务完成通知"""
    message = f"""✅ {IDENTITY_NAME} 任务完成

📝 任务：{task.get('task', 'Unknown')[:50]}
🎯 角色：{task.get('role', 'executor')}
📄 结果：{result[:100] if result else '完成'}
⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

任务已完成！🎉"""
    send_dingtalk_message(message)

def send_help_request(task, reason, error=None):
    """发送求助消息"""
    message = f"""🆘 {IDENTITY_NAME} 求助！

📝 任务：{task.get('task', 'Unknown')[:50]}
🎯 角色：{task.get('role', 'executor')}
❌ 问题：{reason}
📄 错误：{error if error else '无'}
⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

需要老板指导！🙏"""
    send_dingtalk_message(message)

# ==================== 任务管理 ====================

def load_progress():
    """加载进度"""
    progress_file = TASKS_DIR / f"progress-{IDENTITY_ID}.json"
    if progress_file.exists():
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "identity": IDENTITY_ID,
        "completedTasks": [],
        "failedTasks": [],
        "currentTask": None,
        "lastUpdateTime": datetime.now().isoformat()
    }

def save_progress(progress):
    """保存进度"""
    progress["lastUpdateTime"] = datetime.now().isoformat()
    progress_file = TASKS_DIR / f"progress-{IDENTITY_ID}.json"
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    log(f"💾 进度已保存")

def get_pending_task():
    """获取待执行任务"""
    if not TASKS_DIR.exists():
        return None
    
    for file in TASKS_DIR.glob("task-*.json"):
        # 跳过已完成或失败的任务
        if 'completed' in file.name or 'failed' in file.name:
            continue
        
        try:
            with open(file, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                task = json.load(f)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            
            # 检查是否分配给当前身份
            if task.get('assignedTo') == IDENTITY_ID:
                # 检查状态
                status = task.get('status', 'pending')
                if status in ['pending', 'claimed']:
                    return task, file
        except Exception as e:
            log(f"❌ 读取任务文件失败：{file}: {e}", "ERROR")
    
    return None, None

def claim_task(task, task_file):
    """Claim 任务"""
    try:
        with open(task_file, 'r+', encoding='utf-8') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            task = json.load(f)
            task['status'] = 'claimed'
            task['claimedBy'] = IDENTITY_ID
            task['claimedAt'] = datetime.now().isoformat()
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        log(f"📌 已 Claim 任务：{task.get('id')}")
        return True
    except Exception as e:
        log(f"❌ Claim 任务失败：{e}", "ERROR")
        return False

def complete_task(task, task_file, result=""):
    """完成任务"""
    try:
        with open(task_file, 'r+', encoding='utf-8') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            task = json.load(f)
            task['status'] = 'completed'
            task['completedAt'] = datetime.now().isoformat()
            task['result'] = result
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        log(f"✅ 任务完成：{task.get('id')}")
        return True
    except Exception as e:
        log(f"❌ 完成任务失败：{e}", "ERROR")
        return False

def fail_task(task, task_file, error=""):
    """标记任务失败"""
    try:
        with open(task_file, 'r+', encoding='utf-8') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            task = json.load(f)
            task['status'] = 'failed'
            task['failedAt'] = datetime.now().isoformat()
            task['error'] = error
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        log(f"❌ 任务失败：{task.get('id')}")
        return True
    except Exception as e:
        log(f"❌ 标记失败失败：{e}", "ERROR")
        return False

# ==================== 任务执行 ====================

def execute_task(task):
    """执行任务（根据角色类型）"""
    role = task.get('role', 'executor')
    task_type = task.get('type', 'general')
    
    log(f"🚀 开始执行任务：{task.get('id')} - 角色：{role}")
    
    try:
        if role == 'builder':
            return execute_builder_task(task)
        elif role == 'reviewer':
            return execute_reviewer_task(task)
        elif role == 'reporter':
            return execute_reporter_task(task)
        elif role == 'researcher':
            return execute_researcher_task(task)
        elif role == 'writer':
            return execute_writer_task(task)
        elif role == 'deployer':
            return execute_deployer_task(task)
        else:
            return execute_general_task(task)
    except Exception as e:
        log(f"❌ 任务执行异常：{e}", "ERROR")
        raise

def execute_builder_task(task):
    """执行 builder 角色任务（开发/构建）"""
    log(f"🔨 执行 Builder 任务：{task.get('task')}")
    # 这里可以根据具体任务类型调用不同的处理函数
    return f"Builder 完成：{task.get('task')}"

def execute_reviewer_task(task):
    """执行 reviewer 角色任务（审查/测试）"""
    log(f"🔍 执行 Reviewer 任务：{task.get('task')}")
    # 审查逻辑
    return f"Reviewer 完成：{task.get('task')}"

def execute_reporter_task(task):
    """执行 reporter 角色任务（汇报/协调）"""
    log(f"📢 执行 Reporter 任务：{task.get('task')}")
    # 汇报逻辑
    return f"Reporter 完成：{task.get('task')}"

def execute_researcher_task(task):
    """执行 researcher 角色任务（调研/分析）"""
    log(f"🔬 执行 Researcher 任务：{task.get('task')}")
    # 调研逻辑
    return f"Researcher 完成：{task.get('task')}"

def execute_writer_task(task):
    """执行 writer 角色任务（写作/文档）"""
    log(f"✍️ 执行 Writer 任务：{task.get('task')}")
    # 写作逻辑
    return f"Writer 完成：{task.get('task')}"

def execute_deployer_task(task):
    """执行 deployer 角色任务（部署/运维）"""
    log(f"🚀 执行 Deployer 任务：{task.get('task')}")
    # 部署逻辑
    return f"Deployer 完成：{task.get('task')}"

def execute_general_task(task):
    """执行通用任务"""
    log(f"⚙️ 执行通用任务：{task.get('task')}")
    return f"任务完成：{task.get('task')}"

# ==================== 主程序 ====================

def main():
    """主程序"""
    log("=" * 60)
    log(f"{IDENTITY_NAME} 启动")
    log(f"角色：{ROLE}")
    log("=" * 60)
    
    # 获取待执行任务
    task, task_file = get_pending_task()
    
    if task is None:
        log("✅ 无新任务")
        return
    
    # Claim 任务
    if not claim_task(task, task_file):
        log("❌ Claim 任务失败，跳过", "ERROR")
        return
    
    # 发送开始通知
    send_task_started_notification(task)
    
    # 执行任务
    try:
        result = execute_task(task)
        
        # 完成任务
        if complete_task(task, task_file, result):
            send_task_complete_notification(task, result)
            log("✅ 任务执行完成")
        else:
            send_help_request(task, "完成任务失败")
            
    except Exception as e:
        log(f"❌ 任务执行失败：{e}", "ERROR")
        fail_task(task, task_file, str(e))
        send_help_request(task, "任务执行失败", str(e))

if __name__ == '__main__':
    main()
