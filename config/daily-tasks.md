# 📅 每日自动任务配置

**配置时间**: 2026-03-13  
**配置者**: 大娃 (SF-0001)  
**状态**: ✅ 已激活

---

## 📋 任务清单

### 1. 夜间记忆整合 (03:00)

**脚本**: `/workspace/scripts/nightly-integration.py`  
**执行时间**: 每天 03:00  
**功能**: 
- 读取昨日的日记文件
- 提取"提取到知识图谱"章节的内容
- 更新知识图谱索引和关系图谱

**日志**: `/workspace/logs/nightly-integration.log`  
**邮件**: 不发送（仅后台执行）

**依赖**:
- 日记文件：`/workspace/life/daily/YYYY-MM/YYYY-MM-DD.md`
- 知识图谱：`/workspace/life/graph/`

---

### 2. 每日复盘报告 (05:00)

**脚本**: `/workspace/scripts/daily-review-pdf.py`  
**执行时间**: 每天 05:00  
**功能**:
- 生成每日复盘 PDF 报告
- 通过 QQ 邮箱发送邮件（带 PDF 附件）

**日志**: `/workspace/logs/daily-review.log`  
**邮件**: ✅ 发送到 38132579@qq.com

**PDF 内容**:
- 今日完成任务
- 系统状态
- 明日计划

**输出**: `/workspace/reviews/daily/每日复盘报告-YYYY-MM-DD.pdf`

---

### 3. 每日技能检查 (06:00)

**脚本**: `/workspace/scripts/daily-skill-check.py`  
**执行时间**: 每天 06:00  
**功能**:
- 扫描 `/workspace/skills/` 目录
- 统计技能数量和文档完整率
- 生成 Word 报告（Markdown 格式）
- 通过 QQ 邮箱发送邮件（带附件）

**日志**: `/workspace/logs/skill-check.log`  
**邮件**: ✅ 发送到 38132579@qq.com

**报告内容**:
- 技能总数统计
- SKILL.md 完整率
- 技能清单表格
- 检查结论

**输出**: `/workspace/output/skill-reports/技能检查日报-YYYY-MM-DD.md`

---

## 🔧 Cron 配置

```bash
# 查看当前 cron 任务
crontab -l

# 编辑 cron 任务
crontab -e
```

**当前配置**:
```
# 每日自动任务 - 智能龙虾
# 夜间记忆整合 - 每天 03:00
0 3 * * * /usr/bin/python3 /home/admin/.openclaw/workspace/scripts/nightly-integration.py >> /home/admin/.openclaw/workspace/logs/nightly-integration.log 2>&1

# 每日复盘报告 - 每天 05:00
0 5 * * * /usr/bin/python3 /home/admin/.openclaw/workspace/scripts/daily-review-pdf.py >> /home/admin/.openclaw/workspace/logs/daily-review.log 2>&1

# 每日技能检查 - 每天 06:00
0 6 * * * /usr/bin/python3 /home/admin/.openclaw/workspace/scripts/daily-skill-check.py >> /home/admin/.openclaw/workspace/logs/skill-check.log 2>&1
```

---

## 📧 邮件配置

**SMTP 服务器**: smtp.qq.com:465 (SSL)  
**发件邮箱**: 38132579@qq.com  
**收件邮箱**: 38132579@qq.com  
**授权码**: 已配置

**中文附件编码**: 使用 `email.header.Header` 编码

---

## 📊 日志查看

```bash
# 查看最新日志
tail -f /workspace/logs/daily-review.log
tail -f /workspace/logs/skill-check.log
tail -f /workspace/logs/nightly-integration.log

# 查看今日日志
cat /workspace/logs/daily-review.log
cat /workspace/logs/skill-check.log
```

---

## ✅ 测试记录

**2026-03-13 配置测试**:
- ✅ 技能检查脚本执行成功
- ✅ 技能检查邮件发送成功
- ✅ 复盘报告 PDF 生成成功
- ✅ 复盘报告邮件发送成功
- ✅ 夜间整合脚本执行成功（无昨日日记）
- ✅ Cron 任务配置成功

---

## 🔔 注意事项

1. **日记文件**: 夜间整合需要日记文件存在
   - 路径：`/workspace/life/daily/YYYY-MM/YYYY-MM-DD.md`
   - 需要包含"## 🔗 提取到知识图谱"章节

2. **中文字体**: PDF 生成需要文泉驿微米黑字体
   - 路径：`/usr/share/fonts/wqy-microhei/wqy-microhei.ttc`
   - 如果缺失，PDF 会降级为英文

3. **邮件发送**: 需要 QQ 邮箱授权码
   - 如果授权码过期，需要重新获取
   - 授权码获取：QQ 邮箱 → 设置 → 账户 → POP3/SMTP 服务

4. **日志轮转**: 日志文件会不断增长
   - 建议每月清理一次旧日志
   - 或使用 logrotate 自动管理

---

**最后更新**: 2026-03-13  
**维护者**: 大娃 (SF-0001)
