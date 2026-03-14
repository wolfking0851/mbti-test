# 团队协作快速使用指南

## 🚀 5 分钟快速开始

### 场景 1：大型项目（完整协作）

```bash
# 1. 复制模板
cd /workspace/skills/team-collaboration/templates/

# 2. 创建开发任务（Builder - 五娃）
cat > /workspace/team-tasks/task-0005-001.json << 'EOF'
{
  "id": "task-0005-001",
  "assignedTo": "身份 -0005",
  "role": "builder",
  "task": "T001 - 创建项目目录",
  "status": "pending"
}
EOF

# 3. 创建审查任务（Reviewer - 四娃）
cat > /workspace/team-tasks/task-0004-001.json << 'EOF'
{
  "id": "task-0004-001",
  "assignedTo": "身份 -0004",
  "role": "reviewer",
  "task": "审查阶段 1",
  "status": "pending",
  "dependencies": ["task-0005-001"]
}
EOF

# 4. 创建汇报任务（Reporter - 七娃）
cat > /workspace/team-tasks/task-0007-002.json << 'EOF'
{
  "id": "task-0007-002",
  "assignedTo": "身份 -0007",
  "role": "reporter",
  "task": "汇报阶段 1",
  "status": "pending",
  "dependencies": ["task-0004-001"]
}
EOF

# 5. 触发执行
python3 /workspace/scripts/heartbeat-checker.py
```

---

### 场景 2：中型项目（简化协作）

```bash
# 只使用 Builder + Reporter，跳过审查

# 1. 创建开发任务
cat > /workspace/team-tasks/task-0005-001.json << 'EOF'
{
  "id": "task-0005-001",
  "assignedTo": "身份 -0005",
  "role": "builder",
  "task": "T001 - 开发功能",
  "status": "pending"
}
EOF

# 2. 创建汇报任务（直接依赖开发）
cat > /workspace/team-tasks/task-0007-002.json << 'EOF'
{
  "id": "task-0007-002",
  "assignedTo": "身份 -0007",
  "role": "reporter",
  "task": "汇报完成",
  "status": "pending",
  "dependencies": ["task-0005-001"]
}
EOF

# 3. 触发执行
python3 /workspace/scripts/heartbeat-checker.py
```

---

### 场景 3：小型任务（独立开发）

```bash
# 使用六娃独立开发脚本
python3 /workspace/scripts/liuwa-developer.py
```

---

## 📋 任务编号规则

| 身份 | 任务前缀 | 示例 |
|------|---------|------|
| **大娃** | task-0001-XXX | task-0001-001 |
| **二娃** | task-0002-XXX | task-0002-001 |
| **三娃** | task-0003-XXX | task-0003-001 |
| **四娃**（Reviewer） | task-0004-XXX | task-0004-001 |
| **五娃**（Builder） | task-0005-XXX | task-0005-001 |
| **六娃**（独立） | task-0006-XXX | task-0006-001 |
| **七娃**（Reporter） | task-0007-XXX | task-0007-001 |

---

## 🔧 常用命令

### 查看任务状态

```bash
# 查看所有任务
ls -la /workspace/team-tasks/*.json

# 查看特定任务
cat /workspace/team-tasks/task-0005-001.json

# 查看任务进度
python3 -c "
import json
for f in ['/workspace/team-tasks/task-0005-001.json']:
    with open(f) as fp:
        t = json.load(fp)
        print(f'{t[\"id\"]}: {t[\"status\"]}')"
```

### 查看日志

```bash
# 五娃日志（Builder）
tail -20 /workspace/logs/wawa-0005.log

# 七娃日志（Reporter）
tail -20 /workspace/logs/qiwai-task-executor.log

# 六娃日志（独立）
tail -20 /workspace/notebook/logs/liuwa-developer.log
```

### 手动触发

```bash
# 触发 Heartbeat 检查
python3 /workspace/scripts/heartbeat-checker.py

# 触发特定身份
python3 /workspace/scripts/wawa-0005.py
python3 /workspace/scripts/qiwai-task-executor.py
python3 /workspace/scripts/liuwa-developer.py
```

---

## 📊 监控进度

### 实时查看

```bash
# 查看五娃进度
watch -n 2 'cat /workspace/team-tasks/task-0005-*.json | grep status'

# 查看日志实时更新
tail -f /workspace/logs/wawa-0005.log
```

### 完成检查

```bash
python3 << 'EOF'
import json
from pathlib import Path

tasks_dir = Path("/workspace/team-tasks")
completed = 0
total = 0

for task_file in tasks_dir.glob("task-*.json"):
    with open(task_file) as f:
        task = json.load(f)
        total += 1
        if task.get('status') == 'completed':
            completed += 1

print(f"进度：{completed}/{total} 完成 ({completed*100//total}%)")
EOF
```

---

## 🎯 最佳实践

### ✅ 推荐做法

1. **任务细分** - 每个任务<10 分钟
2. **依赖明确** - 清晰标注 dependencies
3. **及时汇报** - 每个阶段完成后立即汇报
4. **日志完整** - 保留所有执行日志

### ❌ 避免做法

1. **任务过大** - 超过 1 小时的任务
2. **依赖循环** - A 依赖 B，B 依赖 A
3. **跳过审查** - 大型项目跳过 Reviewer
4. **无日志** - 不记录执行过程

---

## 📞 求助方式

如果遇到问题：

```bash
# 创建求助任务
cat > /workspace/team-tasks/task-0007-001.json << 'EOF'
{
  "id": "task-0007-001",
  "assignedTo": "身份 -0007",
  "role": "reporter",
  "task": "🆘 求助",
  "status": "pending",
  "helpRequest": {
    "from": "身份 -XXXX",
    "problem": "问题描述",
    "error": "错误信息"
  }
}
EOF

# 触发汇报
python3 /workspace/scripts/qiwai-task-executor.py
```

---

## 📚 参考案例

**成功案例：** Notebook-Local 开发（2026-03-03）
- ⏱️ 51 分钟完成
- ✅ 0 问题
- 📊 91.8 分

**查看报告：**
```bash
cat /workspace/reports/notebook-local-comparison-test-2026-03-03.md
```

---

## 🔗 相关文档

- [SKILL.md](./SKILL.md) - 完整技能文档
- [任务模板](./templates/) - 可复用模板
- [对比报告](/workspace/reports/notebook-local-comparison-test-2026-03-03.md)

---

**最后更新：** 2026-03-03  
**维护者：** 大娃（身份 -0001）
