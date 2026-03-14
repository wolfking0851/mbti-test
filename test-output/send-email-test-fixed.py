#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送测试脚本 - 修复版
QQ 邮箱 SMTP 配置
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# QQ 邮箱 SMTP 配置
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "38132579@qq.com"
SENDER_PASSWORD = "cfuyxscchrfdcaid"  # 授权码
RECEIVER_EMAIL = "38132579@qq.com"

def send_email(subject, body, attachments=None):
    """
    发送邮件
    
    Args:
        subject: 邮件主题
        body: 邮件正文（HTML 格式）
        attachments: 附件文件路径列表
    """
    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    
    # 添加正文（HTML 格式）
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    # 添加附件
    if attachments:
        for i, file_path in enumerate(attachments):
            path = Path(file_path)
            if path.exists():
                print(f'[{i+1}/{len(attachments)}] 添加附件：{path.name} ({path.stat().st_size} bytes)')
                with open(file_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    
                    # 设置附件文件名（使用 UTF-8 编码）
                    filename = path.name
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename="{filename}"'
                    )
                    msg.attach(part)
            else:
                print(f'⚠️ 文件不存在：{file_path}')
    
    # 连接 SMTP 服务器并发送
    try:
        print(f'\n🔗 正在连接 SMTP 服务器：{SMTP_SERVER}:{SMTP_PORT}...')
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print(f'📤 正在发送邮件...')
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        print(f'✅ 连接关闭')
        
        print(f'\n✅ 邮件发送成功！')
        print(f'📧 收件人：{RECEIVER_EMAIL}')
        print(f'📝 主题：{subject}')
        print(f'📦 附件：{len(attachments)} 个')
        
        return True
    except Exception as e:
        print(f'\n❌ 邮件发送失败：{e}')
        return False

if __name__ == '__main__':
    # 测试邮件
    subject = "🦞 智能龙虾 - 邮件发送测试（3 个附件）"
    
    body = """
    <html>
    <body>
        <h2>🦞 智能龙虾 - 邮件发送测试</h2>
        <p><strong>老板好！</strong></p>
        <p>这是邮件发送功能测试。</p>
        
        <h3>✅ 测试内容</h3>
        <ul>
            <li>QQ 邮箱 SMTP 连接</li>
            <li>HTML 格式正文</li>
            <li>附件发送（Word/PPT/PDF）</li>
        </ul>
        
        <h3>📊 附件列表</h3>
        <table border="1" cellpadding="5">
            <tr>
                <th>序号</th>
                <th>文件名</th>
                <th>类型</th>
            </tr>
            <tr>
                <td>1</td>
                <td>测试文档-Word.docx</td>
                <td>Word 文档</td>
            </tr>
            <tr>
                <td>2</td>
                <td>测试演示-PPT.pptx</td>
                <td>PowerPoint</td>
            </tr>
            <tr>
                <td>3</td>
                <td>测试文档-PDF-修复版.pdf</td>
                <td>PDF 文档</td>
            </tr>
        </table>
        
        <p>请确认收到 3 个附件，谢谢！</p>
        
        <hr>
        <p style="color: gray; font-size: 12px;">
            此邮件由智能龙虾自动生成<br>
            发送时间：2026-03-13
        </p>
    </body>
    </html>
    """
    
    # 附件路径（确保路径正确，无空格）
    attachments = [
        '/home/admin/.openclaw/workspace/test-output/测试文档-Word.docx',
        '/home/admin/.openclaw/workspace/test-output/测试演示-PPT.pptx',
        '/home/admin/.openclaw/workspace/test-output/测试文档-PDF-修复版.pdf'
    ]
    
    # 发送邮件
    send_email(subject, body, attachments)
