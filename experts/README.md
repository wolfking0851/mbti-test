# 🎯 专家知识库

这是大娃的专业知识参考库，来自 [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) 项目。

## 📚 核心专家

### 🛠️ 工程部

| 专家 | 文件 | 专长 |
|------|------|------|
| 前端开发者 | `engineering/frontend-developer.md` | React/Vue、UI 实现、性能优化 |
| 后端架构师 | `engineering/backend-architect.md` | API 设计、数据库架构、微服务 |
| AI 工程师 | `engineering/ai-engineer.md` | 机器学习、模型部署、AI 集成 |

### 📱 营销部

| 专家 | 文件 | 专长 |
|------|------|------|
| 小红书运营 | `marketing/xiaohongshu-operator.md` | 种草笔记、达人合作、爆款内容 |
| 抖音策略师 | `marketing/douyin-strategist.md` | 短视频策划、算法优化、直播带货 |
| 微信公众号运营 | `marketing/wechat-operator.md` | 公众号内容、社群运营、裂变增长 |

### 🎨 设计部

| 专家 | 文件 | 专长 |
|------|------|------|
| UI 设计师 | `design/ui-designer.md` | 视觉设计、组件库、设计系统 |

## 📋 完整专家列表

完整 146 个专家位于 `../agency-agents-zh/` 目录：

```
agency-agents-zh/
├── engineering/          # 工程部（22 个专家）
├── marketing/           # 营销部（17 个专家）
├── design/              # 设计部（8 个专家）
├── sales/               # 销售部（8 个专家）
├── product/             # 产品部（4 个专家）
├── project-management/  # 项目管理部（6 个专家）
├── testing/             # 测试部（8 个专家）
├── support/             # 支持部（8 个专家）
├── paid-media/          # 付费媒体部（7 个专家）
├── strategy/            # 战略部
├── game-development/    # 游戏开发部
├── spatial-computing/   # 空间计算部
└── specialized/         # 专业领域
```

## 🎯 使用方式

**大娃保持统一人格**，这些专家文件作为知识参考：

1. 遇到专业问题时，识别需要的专家领域
2. 参考对应专家的 `.md` 文件中的专业知识
3. 以"大娃"的风格和人格回答，不切换人格

**示例**：
```
用户：帮我优化这个 React 组件的性能

大娃：好的老板！我参考前端开发专家的建议来帮你优化...
      [参考 frontend-developer.md 中的性能优化技巧]
      1. 使用 useMemo 缓存计算结果
      2. 实现虚拟列表减少渲染
      3. 代码分割和懒加载...
```

## 📝 添加新专家

需要添加新专家时：

```bash
# 从原始仓库复制
cp ../agency-agents-zh/engineering/engineering-xxx.md \
   engineering/xxx.md

# 更新本索引文件
```

## ⚠️ 重要说明

- ✅ **这是参考知识库**，不是独立代理
- ✅ **大娃保持统一人格**，不切换为专家人格
- ✅ **按需参考**，保持回答的一致性
- ❌ **不要创建 146 个独立代理**（避免网关配置混乱）

---

*最后更新：2026-03-14*
