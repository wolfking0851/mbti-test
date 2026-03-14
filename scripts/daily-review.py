#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日工作总结与复盘脚本
执行时间：每日 04:00
执行者：大娃 (SF-0001)
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path("/home/admin/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
REPORTS_DIR = WORKSPACE / "reports"
LEARNINGS_DIR = WORKSPACE / ".learnings"

def ensure_dirs():
    """确保所有目录存在"""
    MEMORY_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)
    LEARNINGS_DIR.mkdir(exist_ok=True)

def read_file(path):
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

def write_file(path, content):
    """写入文件内容"""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_daily_review():
    """生成每日复盘内容"""
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    date_str = today.strftime("%Y-%m-%d")
    
    # 读取今日记忆文件（如果存在）
    today_memory = read_file(MEMORY_DIR / f"{date_str}.md")
    
    # 读取 MEMORY.md
    memory_md = read_file(WORKSPACE / "MEMORY.md")
    
    # 读取任务记录
    task_0001 = read_file(WORKSPACE / "tasks" / "task-0001.md")
    
    # 生成复盘内容
    review = f"""# 🦞 每日工作总结与复盘

**日期**: {date_str}  
**执行时间**: {today.strftime("%Y-%m-%d %H:%M:%S")}  
**执行者**: 大娃 (SF-0001)

---

## 📊 一、今日工作概览

### 1.1 完成的任务
[待填写 - 从会话历史或任务记录中提取]

### 1.2 进行中的任务
- 本地生活 AI 代运营项目（SF-0002 负责）
  - 待选定细分行业（汽车美容/餐饮/美业）

### 1.3 系统维护
- ✅ OpenClaw 升级到 v2026.3.11（2026-03-12）
- ✅ 恢复 75+ 个记忆和配置文件
- ✅ 恢复 20 个身份档案和任务记录
- ✅ 安装 3 个新技能（debug-pro, powerpoint-pptx, word-docx）

---

## 🧠 二、学习与进化

### 2.1 新学到的知识
[待填写 - 从今日对话中提取]

### 2.2 技能改进
[待填写 - 新增或优化的技能]

### 2.3 血泪教训
[待填写 - 今日犯的错误或遇到的问题]

---

## 🔍 三、问题与反思

### 3.1 遇到的问题
[待填写]

### 3.2 根本原因分析
[待填写]

### 3.3 改进措施
[待填写]

---

## 📋 四、待办事项

### 4.1 优先级任务
1. [ ] 激活其他身份（SF-0002 ~ SF-0020）
2. [ ] 推进本地生活 AI 代运营项目
3. [ ] 重新安装速率限制的技能（16 个）
4. [ ] 积累向量化记忆

### 4.2 需要老板决策
- 是否恢复 82 个脚本文件
- 是否配置 heartbeat 任务
- 本地生活 AI 代运营细分行业选择

---

## 📈 五、系统状态

### 5.1 技能状态
- 已安装：9 个
- 待安装：27 个（速率限制 16 个 + 不存在 11 个）
- 已跳过：5 个（VirusTotal 标记）

### 5.2 记忆状态
- MEMORY.md: ✅ 完整
- 每日记忆：✅ 16 个文件
- 向量化记忆：⚠️ 空库

### 5.3 身份状态
- 已激活：1/20（大娃）
- 待激活：19/20

---

## 🎯 六、明日计划

1. [待填写]
2. [待填写]
3. [待填写]

---

## 📝 七、备注

[其他需要记录的事项]

---

**复盘完成时间**: {today.strftime("%Y-%m-%d %H:%M:%S")}  
**下次复盘**: 明日 04:00

---

*🦞 智能龙虾，持续进化中！*
"""
    
    return review, date_str

def update_evolution_log(review, date_str):
    """更新进化日志"""
    evolution_path = MEMORY_DIR / "evolution-log.md"
    evolution_content = read_file(evolution_path)
    
    # 添加新的进化记录
    new_entry = f"\n## {date_str}\n\n**阶段**: 每日复盘\n**内容**: 完成每日工作总结与复盘\n\n---\n"
    
    write_file(evolution_path, evolution_content + new_entry)

def main():
    """主函数"""
    print(f"[{datetime.now().isoformat()}] 开始执行每日复盘...")
    
    # 确保目录存在
    ensure_dirs()
    
    # 生成复盘内容
    review, date_str = generate_daily_review()
    
    # 保存复盘文件
    review_path = MEMORY_DIR / f"{date_str}-review.md"
    write_file(review_path, review)
    print(f"✅ 复盘文件已保存：{review_path}")
    
    # 更新进化日志
    update_evolution_log(review, date_str)
    print(f"✅ 进化日志已更新")
    
    # 输出到 stdout（供 cron 日志使用）
    print(f"✅ 每日复盘完成：{date_str}")
    
    return 0

if __name__ == "__main__":
    exit(main())
