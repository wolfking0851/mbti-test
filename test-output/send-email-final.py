#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件发送测试脚本 - 最终修复版
修复附件 MIME 类型问题
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

def get_mime_type(file_path):
    """根据文件扩展名获取正确的 MIME 类型"""
    mime_types = {
        '.pdf': 'application/pdf',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.doc': 'application/msword',
        '.pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        '.ppt': 'application/vnd.ms-powerpoint',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.xls': 'application/vnd.ms-excel',
        '.txt': 'text/plain',
        '.jpg': 'image/jpeg',
        '.png': 'image/png',
        '.zip': 'application/zip',
    }
    ext = Path(file_path).suffix.lower()
    return mime_types.get(ext, 'application/octet-stream')

def send_email(subject, body, attachments=None):
    """发送邮件"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject
    
    # 添加正文
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    # 添加附件
    if attachments:
        for i, file_path in enumerate(attachments):
            path = Path(file_path)
            if path.exists():
                mime_type = get_mime_type(file_path)
                print(f'[{i+1}/{len(attachments)}] 添加附件：{path.name}')
                print(f'      MIME 类型：{mime_type}')
                
                with open(file_path, 'rb') as f:
                    # 使用正确的 MIME 类型创建附件
                    maintype, subtype = mime_type.split('/', 1) if '/' in mime_type else ('application', 'octet-stream')
                    part = MIMEBase(maintype, subtype)
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    
                    # 设置文件名
                    filename = path.name
                    part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
                    msg.attach(part)
            else:
                print(f'⚠️ 文件不存在：{file_path}')
    
    # 发送邮件
    try:
        print(f'\n🔗 连接 SMTP: {SMTP_SERVER}:{SMTP_PORT}')
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=30)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        
        print(f'✅ 发送成功！')
        print(f'📧 收件人：{RECEIVER_EMAIL}')
        print(f'📦 附件：{len(attachments)} 个')
        return True
    except Exception as e:
        print(f'❌ 发送失败：{e}')
        return False

if __name__ == '__main__':
    subject = "🦞 智能龙虾 - 邮件测试 (Word+PPT+PDF)"
    
    body = """
    <html><body>
    <h2>🦞 智能龙虾 - 邮件发送测试</h2>
    <p><strong>老板好！</strong></p>
    <h3>📊 附件列表：</h3>
    <ul>
        <li>测试文档-Word.docx (Word 文档)</li>
        <li>测试演示-PPT.pptx (PowerPoint)</li>
        <li>测试文档-PDF-修复版.pdf (PDF 文档)</li>
    </ul>
    <p>请确认收到 3 个正常格式的附件！</p>
    <hr><p style="color:gray;font-size:12px;">智能龙虾 | 2026-03-13</p>
    </body></html>
    """
    
    attachments = [
        '/home/admin/.openclaw/workspace/test-output/测试文档-Word.docx',
        '/home/admin/.openclaw/workspace/test-output/测试演示-PPT.pptx',
        '/home/admin/.openclaw/workspace/test-output/测试文档-PDF-修复版.pdf'
    ]
    
    send_email(subject, body, attachments)
