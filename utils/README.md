# OpenClaw 文件安全写入系统 - 使用指南

**版本**: 1.0.0  
**创建时间**: 2026-03-13  
**创建者**: 大娃 (SF-0001)

---

## 📦 系统组成

```
utils/
├── __init__.py              # 包初始化
├── file_lock.py             # 文件锁管理器
├── atomic_writer.py         # 原子写入器
├── write_logger.py          # 写入日志器
└── safe_write_service.py    # 安全写入服务（总控制器）
```

---

## 🚀 快速开始

### 1. 导入模块

```python
from utils import SafeWriteService

# 初始化（指定操作者 ID）
writer = SafeWriteService(owner_id='SF-0001')
```

### 2. 写入文件

```python
# 简单写入
success = writer.write_file('/path/to/file.txt', '文件内容')

# 带参数写入
success = writer.write_file(
    '/path/to/file.txt',
    '文件内容',
    encoding='utf-8',
    timeout=30,
    make_backup=True
)
```

### 3. 读取文件

```python
content = writer.read_file('/path/to/file.txt')
if content:
    print(f'文件内容：{content}')
else:
    print('读取失败')
```

### 4. 编辑文件

```python
success = writer.edit_file(
    '/path/to/file.txt',
    '要替换的旧文本',
    '新文本'
)
```

### 5. 删除文件

```python
success = writer.delete_file('/path/to/file.txt')
```

### 6. 清理资源

```python
# 释放所有锁
writer.cleanup()
```

---

## 📋 完整示例

### 示例 1：大娃写入任务文件

```python
from utils import SafeWriteService

# 初始化
writer = SafeWriteService(owner_id='SF-0001')

try:
    # 写入任务文件
    success = writer.write_file(
        '/home/admin/.openclaw/workspace/tasks/task-0001.md',
        '# 任务记录\n\n这是大娃写的任务内容'
    )
    
    if success:
        print('✅ 任务文件写入成功')
    else:
        print('❌ 任务文件写入失败')
    
    # 编辑任务文件
    success = writer.edit_file(
        '/home/admin/.openclaw/workspace/tasks/task-0001.md',
        '这是大娃写的任务内容',
        '这是大娃修改后的任务内容'
    )
    
finally:
    # 清理资源
    writer.cleanup()
```

### 示例 2：多娃协作（避免冲突）

```python
from utils import SafeWriteService

# 大娃
writer1 = SafeWriteService(owner_id='SF-0001')

# 二娃
writer2 = SafeWriteService(owner_id='SF-0002')

# 三娃
writer3 = SafeWriteService(owner_id='SF-0003')

# 大娃写入任务文件
writer1.write_file('/workspace/task-0001.md', '大娃的内容')

# 二娃同时写入同一文件（会等待或超时）
writer2.write_file('/workspace/task-0001.md', '二娃的内容', timeout=10)

# 三娃写入不同文件（不冲突）
writer3.write_file('/workspace/task-0002.md', '三娃的内容')

# 清理
writer1.cleanup()
writer2.cleanup()
writer3.cleanup()
```

### 示例 3：查看写入历史

```python
from utils import SafeWriteService

writer = SafeWriteService(owner_id='SF-0001')

# 获取写入历史
history = writer.get_write_history(limit=100)
for entry in history:
    print(f"{entry['datetime']} - {entry['operation']} - {entry['file_path']} - {entry['status']}")

# 获取统计信息
stats = writer.get_statistics(days=7)
print(f"总操作数：{stats['total_operations']}")
print(f"成功：{stats['success_count']}")
print(f"失败：{stats['failed_count']}")
```

---

## 🔧 高级用法

### 1. 自定义锁超时时间

```python
writer = SafeWriteService(owner_id='SF-0001')

# 设置锁超时时间为 10 分钟（默认 5 分钟）
writer.lock_manager.lock_timeout = 600

# 写入时设置获取锁超时为 60 秒（默认 30 秒）
writer.write_file('/path/to/file.txt', '内容', timeout=60)
```

### 2. 自定义备份数量

```python
from utils import AtomicWriter, SafeWriteService

# 保留 5 个备份（默认 3 个）
writer = SafeWriteService(owner_id='SF-0001')
writer.atomic_writer.max_backups = 5
```

### 3. 不创建备份

```python
# 对于临时文件，可以不创建备份
writer.write_file('/tmp/temp.txt', '内容', make_backup=False)
```

### 4. 带重试的写入

```python
from utils import AtomicWriter

writer = AtomicWriter()

# 自动重试 3 次
success = writer.write_with_retry('/path/to/file.txt', '内容', max_retries=3)
```

---

## 📊 日志管理

### 查看日志文件

```bash
# 日志文件位置
cat /home/admin/.openclaw/workspace/logs/write_operations.jsonl

# 查看最近的日志
tail -20 /home/admin/.openclaw/workspace/logs/write_operations.jsonl

# 查看失败的写入
grep '"status": "failed"' /home/admin/.openclaw/workspace/logs/write_operations.jsonl
```

### 清理旧日志

```python
from utils import WriteLogger

logger = WriteLogger()

# 清理 30 天前的日志
logger.cleanup_old_logs(days=30)
```

---

## ⚠️ 注意事项

### 1. 锁超时

- 默认锁超时时间为 5 分钟
- 如果进程崩溃，锁会自动释放
- 建议总是使用 `try...finally` 确保锁被释放

### 2. 备份文件

- 默认保留最新 3 个备份
- 备份文件会占用磁盘空间
- 定期清理旧备份

### 3. 日志文件

- 日志文件会不断增长
- 建议定期清理（每月一次）
- 可以设置日志轮转

### 4. 性能影响

- 文件锁会增加少量开销
- 原子写入比直接写入慢约 10-20%
- 但对于大多数场景影响可忽略

---

## 🐛 故障排查

### 问题 1：获取锁超时

**现象**：
```
❌ SF-0001 获取锁超时：/path/to/file.txt (当前持有者：SF-0002)
```

**原因**：
- 另一个进程/娃正在写入该文件
- 锁持有者崩溃，锁未释放

**解决**：
1. 等待锁持有者完成
2. 检查是否有崩溃的进程
3. 手动清理锁文件：`rm /tmp/openclaw_locks/*.lock`

### 问题 2：写入失败

**现象**：
```
❌ 原子写入失败：Permission denied
```

**原因**：
- 文件权限不足
- 磁盘空间不足

**解决**：
1. 检查文件权限：`ls -la /path/to/file.txt`
2. 检查磁盘空间：`df -h`

### 问题 3：备份文件过多

**现象**：
```
/workspace/file.txt.bak.20260313_100000
/workspace/file.txt.bak.20260313_100100
/workspace/file.txt.bak.20260313_100200
...
```

**原因**：
- 备份清理未正常执行

**解决**：
1. 手动清理：`rm /workspace/file.txt.bak.*`
2. 检查 `max_backups` 设置
3. 确保 `cleanup_old_backups` 正常执行

---

## 📈 最佳实践

### 1. 总是使用 try...finally

```python
writer = SafeWriteService(owner_id='SF-0001')
try:
    writer.write_file('/path/to/file.txt', '内容')
finally:
    writer.cleanup()  # 确保锁被释放
```

### 2. 合理设置超时时间

```python
# 小文件：10-30 秒
writer.write_file('/path/to/small.txt', '内容', timeout=10)

# 大文件：30-60 秒
writer.write_file('/path/to/large.txt', '大内容', timeout=60)
```

### 3. 定期检查日志

```python
# 每周检查一次失败操作
failed = writer.logger.get_failed_operations(limit=50)
if failed:
    print(f'发现 {len(failed)} 次失败操作')
    for entry in failed:
        print(f"  - {entry['file_path']}: {entry['error']}")
```

### 4. 多娃协作时的命名规范

```python
# 每个娃使用唯一的 ID
writer1 = SafeWriteService(owner_id='SF-0001')  # 大娃
writer2 = SafeWriteService(owner_id='SF-0002')  # 二娃
writer3 = SafeWriteService(owner_id='SF-0003')  # 三娃
```

---

## 📝 更新日志

### v1.0.0 (2026-03-13)
- ✅ 初始版本
- ✅ 文件锁管理器
- ✅ 原子写入器
- ✅ 写入日志器
- ✅ 安全写入服务
- ✅ 完整测试验证

---

**维护者**: 大娃 (SF-0001)  
**联系方式**: 钉钉群 "大娃｜智能龙虾【红】"
