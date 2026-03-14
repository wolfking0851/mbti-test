---
name: team-collaboration
description: 多角色协作开发框架（builder + reviewer + reporter）
metadata: {"openclaw": {"emoji": "🤝"}}
---

# Team-Collaboration - 多角色协作开发框架

基于 Notebook-Local 开发经验总结的团队协作框架。

## 🎯 核心理念

**三人协作模式：**
- **Builder（五娃）** - 开发工程师，负责执行开发任务
- **Reviewer（四娃）** - 质量审查，负责代码审查和质量把关
- **Reporter（七娃）** - 汇报协调，负责进度汇报和跨身份协调

## 📊 对比数据

| 指标 | 独立开发 | 团队协作 | 提升 |
|------|---------|---------|------|
| 开发时间 | 6 小时 | 51 分钟 | 7 倍快 |
| 问题数量 | 6 条 ERROR | 2 条 ERROR | 67% 减少 |
| 质量审查 | ❌ 无 | ✅ 3 阶段 | 流程保障 |
| 总分 | 85.2 | 91.8 | +6.5 分 |

## 🚀 使用方式

### 模式 1：完整协作（推荐大型项目）

```bash
# 1. 创建任务目录
mkdir -p /workspace/team-tasks/

# 2. 创建开发任务（Builder）
cat > /workspace/team-tasks/task-0005-001.json << 'EOF'
{
  "id": "task-0005-001",
  "assignedTo": "身份 -0005",
  "role": "builder",
  "task": "T001 - 创建目录结构",
  "status": "pending",
  "dependencies": [],
  "createdAt": "2026-03-03T14:00:00"
}
EOF

# 3. 创建审查任务（Reviewer）
cat > /workspace/team-tasks/task-0004-001.json << 'EOF'
{
  "id": "task-0004-001",
  "assignedTo": "身份 -0004",
  "role": "reviewer",
  "task": "审查阶段 1 - 基础搭建",
  "status": "pending",
  "dependencies": ["task-0005-001"],
  "createdAt": "2026-03-03T14:00:00"
}
EOF

# 4. 创建汇报任务（Reporter）
cat > /workspace/team-tasks/task-0007-002.json << 'EOF'
{
  "id": "task-0007-002",
  "assignedTo": "身份 -0007",
  "role": "reporter",
  "task": "汇报阶段 1 - 基础搭建完成",
  "status": "pending",
  "dependencies": ["task-0004-001"],
  "createdAt": "2026-03-03T14:00:00"
}
EOF

# 5. 触发 Heartbeat 执行
python3 /workspace/scripts/heartbeat-checker.py
```

### 模式 2：简化协作（中型项目）

```bash
# 只使用 Builder + Reporter
# 跳过 Reviewer 审查环节

# 1. 创建开发任务
# 2. 创建汇报任务（依赖开发完成）
# 3. 触发执行
```

### 模式 3：独立开发（小型任务）

```bash
# 使用六娃独立开发脚本
python3 /workspace/scripts/liuwa-developer.py
```

## 📁 文件结构

```
/workspace/skills/team-collaboration/
├── SKILL.md              # 本文件
├── builder.py            # Builder 执行脚本（五娃）
├── reporter.py           # Reporter 汇报脚本（七娃）
├── templates/            # 任务模板
│   ├── builder-task.json
│   ├── reviewer-task.json
│   └── reporter-task.json
└── examples/             # 示例任务
    └── notebook-local/
```

## 🔧 配置说明

### Builder 配置

```python
# /workspace/scripts/wawa-0005.py
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
TASKS_DIR = "/workspace/team-tasks/"
LOGS_DIR = "/workspace/logs/"
```

### Reporter 配置

```python
# /workspace/scripts/qiwai-task-executor.py
DINGTALK_WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=xxx"
ALIBABA_API_KEY = "sk-xxx"
TASKS_DIR = "/workspace/team-tasks/"
```

## 📋 任务模板

### Builder 任务模板

```json
{
  "id": "task-0005-XXX",
  "assignedTo": "身份 -0005",
  "role": "builder",
  "task": "T001 - 任务描述",
  "status": "pending",
  "claimedBy": null,
  "claimedAt": null,
  "completedAt": null,
  "dependencies": [],
  "retryCount": 0,
  "maxRetries": 3,
  "timeout": 300,
  "createdAt": "2026-03-03T14:00:00"
}
```

### Reviewer 任务模板

```json
{
  "id": "task-0004-XXX",
  "assignedTo": "身份 -0004",
  "role": "reviewer",
  "task": "审查阶段 X - 审查描述",
  "status": "pending",
  "dependencies": ["task-0005-XXX"],
  "reviewCriteria": [
    "代码语法正确",
    "目录结构完整",
    "文档齐全"
  ],
  "createdAt": "2026-03-03T14:00:00"
}
```

### Reporter 任务模板

```json
{
  "id": "task-0007-XXX",
  "assignedTo": "身份 -0007",
  "role": "reporter",
  "task": "汇报阶段 X - 汇报描述",
  "status": "pending",
  "dependencies": ["task-0004-XXX"],
  "reportTemplate": "阶段汇报模板",
  "createdAt": "2026-03-03T14:00:00"
}
```

## 🎯 适用场景

| 项目规模 | 推荐模式 | 身份配置 | 理由 |
|---------|---------|---------|------|
| **大型项目** | 完整协作 | Builder + Reviewer + Reporter | 质量第一 |
| **中型项目** | 简化协作 | Builder + Reporter | 效率优先 |
| **小型任务** | 独立开发 | 六娃 | 快速完成 |
| **概念验证** | 独立开发 | 六娃 | 快速迭代 |
| **生产环境** | 完整协作 | Builder + Reviewer + Reporter | 审查必须 |

## 📊 成功案例

### Notebook-Local 开发（2026-03-03）

**任务：** 开发本地版 NotebookLM 技能

**配置：**
- Builder: 五娃（身份 -0005）
- Reviewer: 四娃（身份 -0004）
- Reporter: 七娃（身份 -0007）

**结果：**
- ⏱️ 开发时间：51 分钟
- ✅ 问题数量：0 个
- 📝 审查阶段：3 个
- 📊 最终评分：91.8 分

**对比：** 六娃独立开发耗时 6 小时，出现 2 个问题

---

## 🔄 任务状态机

```
pending → claimed → completed
   ↓         ↓
   └──── blocked
```

**状态说明：**
- `pending`: 等待执行
- `claimed`: 已领取（防止重复执行）
- `completed`: 已完成
- `blocked`: 被依赖阻塞

**文件锁定机制：**
```python
# 防止多个身份同时执行同一任务
def claim_task(task_file):
    with open(lock_file, 'x') as f:
        f.write(str(pid))
    # 如果文件已存在，说明其他进程正在执行
```

---

## 🛠️ 工具脚本

### 创建任务

```bash
python3 /workspace/scripts/create-task.py \
  --role builder \
  --task "T001 - 创建目录结构" \
  --assigned-to "身份 -0005"
```

### 查看进度

```bash
python3 /workspace/scripts/check-progress.py \
  --project "notebook-local"
```

### 触发执行

```bash
python3 /workspace/scripts/heartbeat-checker.py
```

---

## 📚 参考文档

- [对比测试报告](/workspace/reports/notebook-local-comparison-test-2026-03-03.md)
- [六娃独立开发脚本](/workspace/scripts/liuwa-developer.py)
- [五娃 Builder 脚本](/workspace/scripts/wawa-0005.py)
- [七娃 Reporter 脚本](/workspace/scripts/qiwai-task-executor.py)
- [Heartbeat 配置](/workspace/memory/2026-03-03.md)

---

**技能版本：** v1.0  
**创建时间：** 2026-03-03  
**维护者：** 大娃（身份 -0001）
