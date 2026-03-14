#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日技能检查脚本
执行时间：每日 06:00
执行者：大娃 (SF-0001)
功能：扫描技能、生成 PDF 报告、邮件发送
"""

import os
import sys
import smtplib
from datetime import datetime
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from email.header import Header
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# 配置
WORKSPACE = Path("/home/admin/.openclaw/workspace")
SKILLS_DIR = WORKSPACE / "skills"
REPORTS_DIR = WORKSPACE / "output" / "skill-reports"
SMTP_SERVER = "smtp.qq.com"
SMTP_PORT = 465
SENDER_EMAIL = "38132579@qq.com"
SENDER_PASSWORD = "cfuyxscchrfdcaid"
RECEIVER_EMAIL = "38132579@qq.com"

def ensure_dirs():
    """确保目录存在"""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def scan_skills():
    """扫描已安装技能"""
    skills = []
    if SKILLS_DIR.exists():
        for item in SKILLS_DIR.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skill_info = {
                    'name': item.name,
                    'path': str(item),
                    'has_skill_md': (item / 'SKILL.md').exists()
                }
                skills.append(skill_info)
    return skills

def generate_report_content(skills):
    """生成报告内容"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    total = len(skills)
    has_doc = sum(1 for s in skills if s['has_skill_md'])
    missing_doc = total - has_doc
    complete_rate = (has_doc / total * 100) if total > 0 else 0
    
    content = {
        'date': date_str,
        'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'total': total,
        'has_doc': has_doc,
        'missing_doc': missing_doc,
        'complete_rate': complete_rate,
        'skills': skills,
        'status': '正常' if missing_doc == 0 else f'部分技能缺少文档 ({missing_doc}个)'
    }
    return content

def create_pdf(content):
    """创建 PDF 报告"""
    pdf_path = REPORTS_DIR / f"技能检查日报-{content['date']}.pdf"
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # 注册中文字体
    font_path = Path('/usr/share/fonts/wqy-microhei/wqy-microhei.ttc')
    if font_path.exists():
        pdfmetrics.registerFont(TTFont('WenQuanYi', str(font_path)))
        font_name = 'WenQuanYi'
    else:
        font_name = 'Helvetica'
    
    # 样式
    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontName=font_name, fontSize=18, alignment=1, spaceAfter=15)
    normal_style = ParagraphStyle('Normal', parent=styles['Normal'], fontName=font_name, fontSize=11, leading=16)
    heading_style = ParagraphStyle('Heading', parent=styles['Heading2'], fontName=font_name, fontSize=13, spaceBefore=12, spaceAfter=6)
    
    # 标题
    story.append(Paragraph('每日技能检查报告', title_style))
    story.append(Paragraph(f"检查时间：{content['datetime']}", normal_style))
    story.append(Paragraph(f"执行者：大娃 (SF-0001)", normal_style))
    story.append(Spacer(1, 15))
    
    # 统计表格
    story.append(Paragraph('技能统计', heading_style))
    stats_data = [
        ['项目', '数值'],
        ['技能总数', str(content['total'])],
        ['文档完整', str(content['has_doc'])],
        ['缺少文档', str(content['missing_doc'])],
        ['完整率', f"{content['complete_rate']:.1f}%"],
        ['系统状态', content['status']]
    ]
    stats_table = Table(stats_data, colWidths=[120, 120])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), font_name),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(stats_table)
    story.append(Spacer(1, 15))
    
    # 技能清单
    story.append(Paragraph('技能清单', heading_style))
    skills_data = [['序号', '技能名称', 'SKILL.md', '状态']]
    for i, skill in enumerate(content['skills'], 1):
        status = '有' if skill['has_skill_md'] else '无'
        state = '正常' if skill['has_skill_md'] else '缺少文档'
        skills_data.append([str(i), skill['name'], status, state])
    
    skills_table = Table(skills_data, colWidths=[40, 200, 50, 80])
    skills_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), font_name),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('FONTNAME', (0, 1), (-1, -1), font_name),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(skills_table)
    story.append(Spacer(1, 15))
    
    # 检查结论
    story.append(Paragraph('检查结论', heading_style))
    conclusion = f"""
    1. 技能总数：{content['total']} 个
    2. 文档完整率：{content['complete_rate']:.1f}%
    3. 系统状态：{content['status']}
    4. 下次检查：明日 06:00
    """
    story.append(Paragraph(conclusion.strip(), normal_style))
    story.append(Spacer(1, 20))
    
    # 结束
    story.append(Paragraph('智能龙虾 - 技能检查系统', ParagraphStyle('End', parent=normal_style, alignment=1, fontSize=9)))
    
    # 构建 PDF
    doc.build(story)
    return pdf_path

def send_email(pdf_path, content):
    """发送邮件"""
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = Header(f'每日技能检查报告-{content["date"]}', 'utf-8')
    
    # 正文
    body = f"""
<html><body>
<h2>每日技能检查报告</h2>
<p><strong>检查时间</strong>: {content['datetime']}</p>
<p><strong>技能总数</strong>: {content['total']} 个</p>
<p><strong>文档完整率</strong>: {content['complete_rate']:.1f}%</p>
<p><strong>系统状态</strong>: {content['status']}</p>
<p>请查看附件中的 PDF 报告。</p>
<hr>
<p style="color:gray;font-size:12px;">智能龙虾自动发送 | {content['date']}</p>
</body></html>
"""
    msg.attach(MIMEText(body, 'html', 'utf-8'))
    
    # 附件
    with open(pdf_path, 'rb') as f:
        part = MIMEBase('application', 'pdf')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = pdf_path.name
        part.add_header('Content-Disposition', 'attachment', filename=Header(filename, 'utf-8').encode())
        msg.attach(part)
    
    # 发送
    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, [RECEIVER_EMAIL], msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"邮件发送失败：{e}")
        return False

def main():
    print(f"[{datetime.now().isoformat()}] 开始执行每日技能检查...")
    
    # 确保目录存在
    ensure_dirs()
    
    # 扫描技能
    skills = scan_skills()
    print(f"已扫描 {len(skills)} 个技能")
    
    # 生成内容
    content = generate_report_content(skills)
    print(f"已生成报告内容")
    
    # 创建 PDF
    pdf_path = create_pdf(content)
    print(f"PDF 已生成：{pdf_path}")
    
    # 发送邮件
    if send_email(pdf_path, content):
        print(f"邮件已发送：{RECEIVER_EMAIL}")
    else:
        print(f"邮件发送失败")
    
    print(f"每日技能检查完成：{content['date']}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
