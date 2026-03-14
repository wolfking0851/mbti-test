#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
发送心理测试 HTML 文件到邮箱
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

# 配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "38132579@qq.com"
SENDER_PASSWORD = "cfuyxscchrfdcaid"  # QQ 邮箱授权码
RECEIVER_EMAIL = "38132579@qq.com"

# 创建邮件
msg = MIMEMultipart()
msg['From'] = SENDER_EMAIL
msg['To'] = RECEIVER_EMAIL
msg['Subject'] = "🧠 心理测试馆 - 测试文件（可直接打开）"

# 邮件正文
body = """
<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
<h2>🧠 心理测试馆 - 测试文件</h2>

<p><strong>老板，附件是心理测试馆的演示版 HTML 文件！</strong></p>

<h3>📱 测试方法：</h3>
<ol>
  <li>下载下方附件</li>
  <li>用浏览器打开（手机/电脑都可以）</li>
  <li>开始测试体验（MBTI 12 题）</li>
</ol>

<h3>✅ 包含功能：</h3>
<ul>
  <li>首页（3 个测试展示）</li>
  <li>MBTI 测试流程（12 道题）</li>
  <li>结果展示（免费内容）</li>
  <li>付费墙演示（解锁深度报告）</li>
</ul>

<h3>⚠️ 说明：</h3>
<ul>
  <li>这是演示版（单文件，无需服务器）</li>
  <li>支付功能暂未接入（仅演示）</li>
  <li>双击即可打开，无需联网</li>
</ul>

<h3>🎯 下一步：</h3>
<p>测试完后告诉我体验如何，我可以立即优化！</p>

<hr style="border: none; border-top: 1px solid #ddd; margin: 20px 0;">
<p style="color: #666; font-size: 12px;">
⚠️ 温馨提示：本测试基于心理学理论，由 AI 生成解读，仅供娱乐和自我探索参考，不构成专业心理诊断。
</p>

<p><strong>大娃（SF-0001）</strong><br>
智能龙虾 AI 助手</p>
</body>
</html>
"""

msg.attach(MIMEText(body, 'html', 'utf-8'))

# 添加附件
html_file = Path("/home/admin/.openclaw/workspace/web-mvp/demo.html")
with open(html_file, 'rb') as f:
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment', filename="心理测试馆 - 演示版.html")
    msg.attach(part)

# 发送邮件
try:
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
    print(f"📧 已发送到：{RECEIVER_EMAIL}")
except Exception as e:
    print(f"❌ 邮件发送失败：{e}")
    import traceback
    traceback.print_exc()
