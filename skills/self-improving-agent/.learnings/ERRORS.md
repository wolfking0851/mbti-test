# Errors Log

Command failures, exceptions, and unexpected behaviors.

---

## 2026-03-03 - 六娃重复通知问题（两次修复）

### 错误描述
六娃的 Heartbeat 每小时发送重复的完成通知，用户收到多次相同的消息：
```
🎉 Notebook-Local 开发完成！
✅ 所有 8 个任务已完成
⏰ 2026-03-03 19:05:02
```

**重复时间：** 19:05, 20:05, 21:05, 22:05（每小时重复）

### 错误原因

#### 第一次修复（不彻底）
**原因：** 脚本逻辑问题
- 代码没有检查 `completionNotified` 标记
- 每次 Heartbeat 触发都重新发送通知

**修复：** 添加 `completionNotified` 标记检查
```python
if progress.get("completionNotified", False):
    log(f"✅ 任务已完成且已通知，跳过 ({completed}/{total_tasks})")
    return
```

#### 第二次修复（根本原因）
**原因：** cron 配置重复
```bash
5 * * * * python3 /home/admin/.openclaw/workspace/scripts/liuwa-developer.py  # ❌ 重复
5 * * * * python3 /home/admin/.openclaw/workspace/scripts/liuwa-developer.py  # ❌ 重复
```

**导致：**
1. ⏰ 每小时 5 分，两个进程同时启动
2. 🔍 都检查 `completionNotified`（都是 false，因为还没保存）
3. 📤 都发送通知
4. 💾 都设置 `completionNotified=true`

**结果：** 每次都发送两次相同的通知！

### 解决过程

#### 第一次修复（13:38）
1. ✅ 添加 `completionNotified` 检查逻辑
2. ✅ 发送通知后标记状态
3. ❌ **未检查 cron 配置**

#### 第二次修复（22:05 后）
1. ✅ 检查 crontab 配置
2. ✅ 发现重复的 cron 任务
3. ✅ 删除重复任务，只保留一个
4. ✅ 验证 crontab 配置

### 根本原因
1. **代码层面：** 没有状态标记检查
2. **配置层面：** cron 任务重复添加
3. **流程层面：** 修复不彻底，没有检查所有可能的原因

### 影响
- ❌ 用户收到 4 次重复通知（19:05, 20:05, 21:05, 22:05）
- ❌ 每次发送 2 条相同消息（cron 重复导致）
- ❌ 总共 8 条重复消息
- ❌ 影响用户体验
- ❌ 浪费系统资源

---

## 2026-03-03 - 响应速度变慢问题

### 错误描述
用户反馈响应速度明显变慢，从正常的 2-5 秒变为 3-8 分钟。

### 错误原因
1. **上下文积累** - 长对话导致上下文 token 增加（约 100 条消息）
2. **工具调用过多** - 复杂任务涉及大量 exec 调用（30-50 次）
3. **Gateway 长时间运行** - 未重启，内存累积（628MB）
4. **消息去重机制失效** - 导致同一条消息发送两次

### 解决过程
1. ✅ 分析系统资源（CPU、内存、磁盘 I/O）
2. ✅ 检查 OpenClaw 日志（查看响应时间）
3. ✅ 发现响应时间确实异常（226 秒、509 秒）
4. ✅ 重启 Gateway
5. ✅ 内存恢复到 474MB
6. ✅ 响应速度恢复到 2-5 秒

### 根本原因
- Gateway 长时间运行未重启
- 上下文积累未清理
- 消息队列积压

### 影响
- ❌ 用户体验差（等待 3-8 分钟）
- ❌ 资源浪费（双倍的 API 调用）
- ❌ 消息混乱（收到重复消息）

---

## 2026-02-28 - 邮件发送失败问题

### 错误描述
用户报告邮件发送失败，但之前可以成功发送多封邮件。

### 错误原因
1. **脚本路径混淆**
   - 邮件脚本位于 `reports/send_email.py`
   - 但检查时错误地查找 `scripts/send_email.py`
   - 导致误判为"脚本不存在"

2. **目录结构不清晰**
   - 邮件相关脚本分散在多个目录：
     - `reports/send_email.py` - 通用邮件发送
     - `reports/send-task-summary-email.py` - 任务总结邮件
     - `scripts/send-skill-check-email.py` - 技能检查邮件
   - 没有统一的邮件脚本目录

### 解决过程
1. ✅ 使用 `find` 命令搜索所有邮件相关脚本
2. ✅ 定位到正确的脚本位置（reports/send_email.py）
3. ✅ 测试脚本执行：`python3 reports/send_email.py`
4. ✅ 确认邮件发送成功

### 根本原因
- 脚本存放位置不统一（reports vs scripts）
- 没有建立脚本索引或配置文件
- AI 对脚本路径记忆不准确

### 影响
- 用户困惑（明明之前可以发送）
- 排查时间增加（约 5 分钟）
- 影响用户体验

---
