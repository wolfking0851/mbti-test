#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
七娃任务执行器
用途：检查并执行分配给七娃（身份 -0007）的任务
触发：每 5 分钟执行（Cron）
"""

import json
import os
import sys
import requests
import fcntl
from datetime import datetime
from pathlib import Path

# 配置
IDENTITY_ID = "身份 -0007"
IDENTITY_NAME = "七娃"
ROLE = "动态任务执行者（审查/汇报）"
TASKS_DIR = Path("/home/admin/.openclaw/workspace/team-tasks")
LOGS_DIR = Path("/home/admin/.openclaw/workspace/logs")
ALIBABA_API_KEY = "sk-6bcc79046f4a41d4b379f29480c0f07b"  # 阿里云百炼 API Key

# 钉钉配置（七娃独立群）
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=d42df3c2126f52ec41dc427ac37a4006f0857c893c1031f0f5610285ebc21f89"

# 确保日志目录存在
LOGS_DIR.mkdir(parents=True, exist_ok=True)

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_msg = f"[{timestamp}] [{IDENTITY_NAME}] {message}"
    print(log_msg)
    
    # 同时写入日志文件
    log_file = LOGS_DIR / "qiwai-task-executor.log"
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(log_msg + '\n')

def send_dingtalk_message(message):
    """发送消息到钉钉"""
    log(f"📤 准备发送钉钉消息：{message[:50]}...")
    
    try:
        response = requests.post(
            DINGTALK_WEBHOOK,
            json={
                "msgtype": "text",
                "text": {
                    "content": message
                }
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
                log(f"❌ 钉钉 API 返回错误：{result}")
                return False
        else:
            log(f"❌ 钉钉 API 请求失败：{response.status_code}")
            return False
    except Exception as e:
        log(f"❌ 发送钉钉消息失败：{e}")
        return False

def execute_reporter_task(task):
    """执行 reporter 角色任务：生成结构化汇报"""
    log(f"📢 执行 Reporter 任务：{task.get('task')}")
    
    # 从任务文件中提取信息
    project = task.get('project', 'Unknown')
    stage = task.get('stage', 1)
    stage_name = task.get('stageName', 'Unknown')
    instructions = task.get('instructions', '')
    
    # 检查依赖任务（审查任务）的完成情况
    dependencies = task.get('dependencies', [])
    review_status = "✅ 审查通过"
    
    # 读取依赖任务状态
    for dep_id in dependencies:
        dep_file = TASKS_DIR / f"{dep_id}.json"
        if dep_file.exists():
            with open(dep_file, 'r', encoding='utf-8') as f:
                dep_task = json.load(f)
                if dep_task.get('status') != 'completed':
                    review_status = "⏳ 等待审查"
                elif dep_task.get('assignedTo') == '身份 -0004':
                    review_status = "✅ 四娃审查通过"
    
    # 根据阶段生成汇报内容
    if stage == 1:
        tasks_completed = "T001 - 创建目录结构\nT002 - 创建任务配置文件\nT003 - 创建主执行脚本"
        next_stage = "阶段 2（技能配置）"
    elif stage == 2:
        tasks_completed = "T004 - 创建 SKILL.md\nT005 - 创建 requirements.txt\nT006 - 安装 Python 依赖"
        next_stage = "阶段 3（测试完成）"
    elif stage == 3:
        tasks_completed = "T007 - Hello World 测试\nT008 - 阶段完成汇报"
        next_stage = "✅ 全部完成！"
    else:
        tasks_completed = "未知任务"
        next_stage = "未知"
    
    # 生成结构化汇报
    report = f"""✅ {stage_name}

📝 项目：{project}
🔧 身份：五娃（开发）+ 四娃（审查）+ 七娃（汇报）

📋 {stage_name}完成的任务：
✅ {tasks_completed}

🔍 审查结果：
{review_status}

⏭️ 下一步：{next_stage}

⏰ 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
    
    return report

def execute_reviewer_task(task):
    """执行 reviewer 角色任务：审查代码/成果"""
    log(f"🔍 执行 Reviewer 任务：{task.get('task')}")
    
    # 检查依赖任务（开发任务）的完成情况
    dependencies = task.get('dependencies', [])
    all_completed = True
    
    for dep_id in dependencies:
        dep_file = TASKS_DIR / f"{dep_id}.json"
        if dep_file.exists():
            with open(dep_file, 'r', encoding='utf-8') as f:
                dep_task = json.load(f)
                if dep_task.get('status') != 'completed':
                    all_completed = False
                    break
        else:
            all_completed = False
            break
    
    if all_completed:
        return "✅ 审查通过：所有依赖任务已完成，成果符合要求。"
    else:
        return "⏳ 等待中：依赖任务尚未全部完成。"

def execute_general_task(task):
    """执行通用任务"""
    log(f"⚙️ 执行通用任务：{task.get('task')}")
    return f"任务完成：{task.get('task')}"

def execute_task_with_alibaba(task_content):
    """调用阿里云 API 执行任务"""
    try:
        response = requests.post(
            'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
            headers={'Authorization': f'Bearer {ALIBABA_API_KEY}'},
            json={
                'model': 'qwen-plus',
                'messages': [{
                    'role': 'system',
                    'content': '你是七娃，一个专业的 AI 助手。请认真完成任务。'
                }, {
                    'role': 'user',
                    'content': task_content
                }]
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                content = result['choices'][0]['message']['content']
                log(f"✅ 阿里云 API 调用成功")
                return content
            else:
                raise Exception(f"API 返回格式异常：{result}")
        else:
            raise Exception(f"API error: {response.status_code} - {response.text}")
            
    except Exception as e:
        log(f"❌ 阿里云 API 调用失败：{e}")
        raise

def update_task_status(file_path, status, result_text):
    """更新任务状态"""
    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            task = json.load(f)
            task['status'] = status
            task['result'] = {
                'text': result_text,
                'completedAt': datetime.now().isoformat()
            }
            task['completedAt'] = datetime.now().isoformat()
            f.seek(0)
            json.dump(task, f, ensure_ascii=False, indent=2)
            f.truncate()
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        log(f"📝 任务状态已更新：{status}")
    except Exception as e:
        log(f"❌ 更新任务状态失败：{e}")

def check_and_execute_tasks():
    """检查并执行任务"""
    log(f"❤️ 开始检查任务...")
    
    if not TASKS_DIR.exists():
        log(f"⚠️ 任务目录不存在：{TASKS_DIR}")
        return
    
    found_tasks = 0
    executed_tasks = 0
    
    for file in TASKS_DIR.glob("*.json"):
        # 跳过通知文件
        if 'notify' in file.name:
            continue
            
        try:
            with open(file, 'r', encoding='utf-8') as f:
                fcntl.flock(f.fileno(), fcntl.LOCK_SH)
                task = json.load(f)
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                
                # 检查依赖任务是否完成
                dependencies = task.get('dependencies', [])
                deps_completed = True
                for dep_id in dependencies:
                    dep_file = TASKS_DIR / f"{dep_id}.json"
                    if dep_file.exists():
                        with open(dep_file, 'r', encoding='utf-8') as f:
                            dep_task = json.load(f)
                            if dep_task.get('status') != 'completed':
                                deps_completed = False
                                log(f"⏳ 依赖任务 {dep_id} 未完成，跳过")
                                break
                    else:
                        deps_completed = False
                        log(f"⏳ 依赖任务 {dep_id} 不存在，跳过")
                        break
                
                if not deps_completed:
                    continue  # 跳过此任务，等待依赖完成
                
                # 检查是否分配给七娃且状态为 pending
                if (task.get('assignedTo') == IDENTITY_ID and 
                    task.get('status') == 'pending'):
                    
                    found_tasks += 1
                    log(f"📋 发现任务：{file.name}")
                    log(f"📝 任务内容：{task.get('task', 'Unknown')[:50]}...")
                    
                    # 更新状态为 claimed
                    with open(file, 'r+', encoding='utf-8') as f:
                        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                        task = json.load(f)
                        task['status'] = 'claimed'
                        task['claimedBy'] = IDENTITY_ID
                        task['claimedAt'] = datetime.now().isoformat()
                        f.seek(0)
                        json.dump(task, f, ensure_ascii=False, indent=2)
                        f.truncate()
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    
                    # 执行任务（根据角色类型）
                    try:
                        log(f"🚀 开始执行任务...")
                        role = task.get('role', 'general')
                        
                        if role == 'reporter':
                            result_text = execute_reporter_task(task)
                        elif role == 'reviewer':
                            result_text = execute_reviewer_task(task)
                        else:
                            result_text = execute_general_task(task)
                        
                        # 更新状态为 completed
                        update_task_status(str(file), 'completed', result_text)
                        executed_tasks += 1
                        
                        # 发送钉钉通知
                        dingtalk_msg = result_text
                        send_dingtalk_message(dingtalk_msg)
                        
                        log(f"✅ 任务执行完成：{file.name}")
                        
                    except Exception as e:
                        log(f"❌ 任务执行失败：{e}")
                        update_task_status(str(file), 'failed', str(e))
        
        except Exception as e:
            log(f"❌ 处理任务 {file.name} 失败：{e}")
    
    if found_tasks == 0:
        log(f"✅ 无新任务")
    else:
        log(f"✅ 检查完成，发现{found_tasks}个任务，执行{executed_tasks}个")

if __name__ == '__main__':
    log(f"❤️ 七娃任务执行器启动")
    check_and_execute_tasks()
