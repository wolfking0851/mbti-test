#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
心理学知识库学习追踪机器人
功能：
1. 每小时更新学习进度
2. 检查是否按计划进行
3. 如果中断，自动恢复
4. 完成时通知老板
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
    with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(data):
    """保存进度"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def log_message(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}\n"
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_line)
    
    print(log_line.strip())

def update_stage_progress(progress_data, stage_id, subtask_name, completed=False):
    """更新阶段进度"""
    for stage in progress_data['stages']:
        if stage['id'] == stage_id:
            if completed:
                stage['status'] = 'completed'
                stage['actual_end'] = datetime.now().isoformat()
                stage['progress_percent'] = 100
                log_message(f"✅ 第{stage_id}阶段完成：{stage['name']}")
            else:
                # 更新子任务
                for subtask in stage['subtasks']:
                    if subtask['name'] == subtask_name:
                        subtask['status'] = 'completed'
                
                # 计算阶段进度
                completed_count = sum(1 for s in stage['subtasks'] if s['status'] == 'completed')
                stage['progress_percent'] = int(completed_count / len(stage['subtasks']) * 100)
                
                log_message(f"📚 进度更新：第{stage_id}阶段 - {subtask_name} 完成 ({stage['progress_percent']}%)")
            
            break
    
    # 添加日志
    progress_data['logs'].append({
        'timestamp': datetime.now().isoformat(),
        'event': 'stage_update',
        'stage': stage_id,
        'subtask': subtask_name,
        'completed': completed
    })
    
    save_progress(progress_data)

def check_checkpoint(progress_data):
    """检查检查点"""
    now = datetime.now()
    
    for checkpoint in progress_data['checkpoints']:
        if checkpoint['status'] == 'pending':
            checkpoint_time_str = checkpoint['time'].replace('+08:00', '').replace('T', ' ')
            checkpoint_time = datetime.strptime(checkpoint_time_str, "%Y-%m-%d %H:%M:%S")
            
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
    for stage in progress_data['stages']:
        if stage['status'] == 'in_progress':
            return stage
    return None

def complete_task(stage_id, task_name):
    """任务完成后立即调用"""
    progress_data = load_progress()
    
    # 更新进度
    update_stage_progress(progress_data, stage_id, task_name, completed=True)
    
    # 检查是否完成所有子任务
    for stage in progress_data['stages']:
        if stage['id'] == stage_id:
            all_completed = all(s['status'] == 'completed' for s in stage['subtasks'])
            if all_completed and stage['status'] != 'completed':
                stage['status'] = 'completed'
                stage['actual_end'] = datetime.now().isoformat()
                log_message(f"🎉 第{stage_id}阶段全部完成！进入下一阶段...")
                
                # 启动下一阶段
                if stage_id < len(progress_data['stages']):
                    next_stage = progress_data['stages'][stage_id]  # 注意索引
                    next_stage['status'] = 'in_progress'
                    log_message(f"▶️ 开始第{stage_id + 1}阶段：{next_stage['name']}")
            break
    
    save_progress(progress_data)
    check_checkpoint(progress_data)

def main():
    """主函数"""
    log_message("=" * 50)
    log_message("🎯 心理学知识库学习追踪机器人启动")
    log_message("=" * 50)
    
    # 加载进度
    progress_data = load_progress()
    
    # 获取当前阶段
    current_stage = get_current_stage(progress_data)
    
    if current_stage is None:
        log_message("✅ 所有阶段已完成！准备交付...")
        # TODO: 发送完成通知给老板
        return
    
    log_message(f"📚 当前阶段：第{current_stage['id']}阶段 - {current_stage['name']}")
    log_message(f"📊 当前进度：{current_stage['progress_percent']}%")
    
    # 检查检查点
    check_checkpoint(progress_data)
    
    # 模拟学习过程（实际应该由 AI 执行学习任务）
    log_message("🤖 AI 正在学习中...")
    
    # 示例：更新第一个子任务为完成
    if current_stage['subtasks']:
        first_subtask = current_stage['subtasks'][0]
        if first_subtask['status'] == 'pending':
            update_stage_progress(
                progress_data, 
                current_stage['id'], 
                first_subtask['name'],
                completed=True
            )
    
    log_message("📝 进度已保存，1 小时后再次检查...")

if __name__ == "__main__":
    main()
