# 🚀 Vercel 部署指南

## 📋 快速部署（5 分钟）

### 第 1 步：注册 Vercel
1. 访问 https://vercel.com
2. 点击 "Sign Up"
3. 使用 GitHub 账号登录（推荐）或邮箱注册
4. 完成注册

### 第 2 步：创建项目
1. 登录后点击 "Add New Project"
2. 选择 "Upload Folder"（上传文件夹）
3. 选择项目文件夹：`/home/admin/.openclaw/workspace/`
4. 输入项目名称：`mbti-test`
5. 点击 "Deploy"

### 第 3 步：等待部署
- Vercel 会自动构建和部署
- 约 1-2 分钟完成
- 成功后会显示绿色对勾 ✅

### 第 4 步：获取域名
- 部署成功后获得域名：`https://mbti-test.vercel.app`
- 点击 "Visit" 即可访问

### 第 5 步：测试访问
- 在浏览器打开域名
- 测试完整流程
- 手机和电脑都测试一下

---

## 📁 需要上传的文件

```
workspace/
├── mbti-12-professional.html（主文件）
├── mbti-images/
│   └── images/
│       ├── round1_optionA.jpg
│       ├── round1_optionB.jpg
│       └── ... (24 张图片)
└── DEPLOYMENT-GUIDE.md（本文件）
```

**注意**：
- 确保图片在 `mbti-images/images/` 目录
- H5 文件中的图片路径需要正确

---

## 🔧 自定义域名（可选）

### 购买域名
推荐域名：
- `mbti-test.com`
- `16typestest.cn`
- `性格测试.com`
- `人格测试.cn`

购买平台：
- 阿里云（wanwang.aliyun.com）
- 腾讯云（cloud.tencent.com/product/domain）
- Namecheap（namecheap.com）

### 绑定到 Vercel
1. Vercel 项目设置 → Domains
2. 输入你的域名
3. 按照提示配置 DNS
4. 等待 DNS 生效（约 10 分钟）

---

## 📊 数据统计

Vercel 免费提供：
- 访问量统计
- 地域分布
- 设备类型
- 引荐来源

查看方式：
1. Vercel 项目页面 → Analytics
2. 开启分析功能
3. 实时查看数据

---

## ⚡ 性能优化

### 图片优化
- 使用 WebP 格式（比 JPG 小 30%）
- 压缩到单张 < 200KB
- 分辨率 800x800 足够

### 加载优化
- 启用 CDN（Vercel 自动）
- 启用 Gzip 压缩（Vercel 自动）
- 图片懒加载（可选）

---

## 🆘 常见问题

### Q: 部署失败怎么办？
A: 检查文件路径是否正确，特别是图片路径

### Q: 图片无法显示？
A: 检查图片路径是否为 `mbti-images/images/xxx.jpg`

### Q: 访问速度慢？
A: Vercel 自动使用 CDN，国内访问应该很快

### Q: 流量超了怎么办？
A: 免费版 100GB/月，足够支撑日活 1 万+

---

## 📞 技术支持

Vercel 文档：https://vercel.com/docs
Vercel 社区：https://github.com/vercel/vercel/discussions

---

## ✅ 部署检查清单
- [ ] 注册 Vercel 账号
- [ ] 创建项目
- [ ] 上传文件
- [ ] 等待部署完成
- [ ] 测试访问
- [ ] 手机测试
- [ ] 电脑测试
- [ ] 检查图片加载
- [ ] 检查测试流程
- [ ] 检查结果展示

---

**祝部署顺利！** 🎉
