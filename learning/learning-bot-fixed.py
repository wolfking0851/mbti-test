#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心理学知识库学习追踪机器人 - 稳定版
功能：
1. 每 10 分钟检查进度（兜底）
2. 检查是否按计划进行
3. 如果中断，记录日志
4. 完成时通知老板

注意：此脚本只负责追踪，不负责执行学习任务
学习任务由 AI 主动调用 complete-task.sh 完成
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = Path("/home/admin/.openclaw/workspace")
LEARNING_DIR = WORKSPACE / "learning"
PROGRESS_FILE = LEARNING_DIR / "progress.json"
LOG_FILE = LEARNING_DIR / "learning.log"

def load_progress():
    """加载进度"""
    try:
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        log_message(f"❌ 加载进度失败：{e}")
        return None

def save_progress(data):
    """保存进度"""
    try:
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        log_message(f"❌ 保存进度失败：{e}")

def log_message(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_line)
    except Exception as e:
        print(f"写入日志失败：{e}")
    
    print(log_line.strip())

def check_checkpoint(progress_data):
    """检查检查点"""
    if not progress_data:
        return
    
    now = datetime.now()
    
    for checkpoint in progress_data['checkpoints']:
        if checkpoint['status'] == 'pending':
            try:
                checkpoint_time_str = checkpoint['time'].replace('+08:00', '').replace('T', ' ')
                checkpoint_time = datetime.strptime(checkpoint_time_str, "%Y-%m-%d %H:%M:%S")
            except:
                continue
            
            # 如果到了检查点时间
            if now >= checkpoint_time:
                # 计算当前总进度
                total_progress = sum(
                    stage['progress_percent'] 
                    for stage in progress_data['stages']
                )
                
                checkpoint['actual_progress'] = total_progress
                checkpoint['status'] = 'checked'
                
                # 检查是否延迟
                if total_progress < checkpoint['expected_progress']:
                    checkpoint['status'] = 'delayed'
                    log_message(f"⚠️ 检查点延迟：{checkpoint['time']} - 预期{checkpoint['expected_progress']}%，实际{total_progress}%")
                else:
                    log_message(f"✅ 检查点正常：{checkpoint['time']} - 预期{checkpoint['expected_progress']}%，实际{total_progress}%")
                
                # 如果是里程碑，特别通知
                if 'milestone' in checkpoint:
                    log_message(f"🎯 里程碑：{checkpoint['milestone']}")
    
    save_progress(progress_data)

def get_current_stage(progress_data):
    """获取当前阶段"""
    if not progress_data:
        return None
    
    for stage in progress_data['stages']:
        if stage['status'] == 'in_progress':
            return stage
    return None

def check_all_completed(progress_data):
    """检查是否所有阶段完成"""
    if not progress_data:
        return False
    
    for stage in progress_data['stages']:
        if stage['status'] != 'completed':
            return False
    return True

def main():
    """主函数 - 只检查，不修改学习状态"""
    log_message("=" * 50)
    log_message("🎯 心理学知识库学习追踪检查（只读模式）")
    log_message("=" * 50)
    
    # 加载进度
    progress_data = load_progress()
    
    if not progress_data:
        log_message("❌ 无法加载进度文件，请检查配置")
        return
    
    # 检查是否全部完成
    if check_all_completed(progress_data):
        log_message("✅ 所有阶段已完成！等待老板审核...")
        return
    
    # 获取当前阶段
    current_stage = get_current_stage(progress_data)
    
    if current_stage is None:
        log_message("⚠️ 没有进行中的阶段，请检查进度配置")
        log_message("💡 提示：应该有且只有一个阶段状态为'in_progress'")
        return
    
    log_message(f"📚 当前阶段：第{current_stage['id']}阶段 - {current_stage['name']}")
    log_message(f"📊 当前进度：{current_stage['progress_percent']}%")
    
    # 显示子任务状态
    log_message("📋 子任务状态:")
    for i, subtask in enumerate(current_stage['subtasks'], 1):
        status_icon = "✅" if subtask['status'] == 'completed' else "⏳"
        log_message(f"  {i}. {status_icon} {subtask['name']}")
    
    # 检查检查点
    check_checkpoint(progress_data)
    
    # 显示下一步操作提示
    log_message("💡 下一步操作:")
    pending_tasks = [s for s in current_stage['subtasks'] if s['status'] == 'pending']
    if pending_tasks:
        next_task = pending_tasks[0]
        log_message(f"  继续学习：{next_task['name']}")
        log_message(f"  完成后执行：./complete-task.sh {current_stage['id']} {next_task['name']}")
    
    log_message("📝 检查完成，10 分钟后再次检查...")

if __name__ == "__main__":
    main()
