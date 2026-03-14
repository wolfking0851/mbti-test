# 错误记录

记录所有命令失败、异常和意外行为。

---

## 条目格式

```markdown
## [ERR-YYYYMMDD-XXX] skill_or_command_name

**Logged**: ISO-8601 时间戳
**Priority**: high
**Status**: pending | resolved
**Area**: frontend | backend | infra | tests | docs | config

### Summary
简要描述什么失败了

### Error
```
实际错误消息或输出
```

### Context
- 尝试的命令/操作
- 使用的输入或参数
- 相关的环境细节

### Suggested Fix
如果可以识别，什么可能解决这个问题

### Metadata
- Reproducible: yes | no | unknown
- Related Files: 路径/to/文件.ext

---
```

---

[待添加错误记录]
