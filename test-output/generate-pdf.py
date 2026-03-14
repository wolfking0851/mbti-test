#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试文件生成 - PDF 文档
使用 reportlab 生成
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

def create_test_pdf():
    output_path = '/home/admin/.openclaw/workspace/test-output/测试文档-PDF.pdf'
    
    # 创建文档
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 故事列表
    story = []
    styles = getSampleStyleSheet()
    
    # 注册中文字体（使用系统字体）
    font_paths = [
        '/usr/share/fonts/wqy-microhei/wqy-microhei.ttc',
        '/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc',
        '/usr/share/fonts/google-noto-sans-cjk/NotoSansCJK-Regular.ttc',
    ]
    
    font_registered = False
    font_name = None
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                font_registered = True
                font_name = 'ChineseFont'
                print(f'✅ 使用中文字体：{font_path}')
                break
            except Exception as e:
                print(f'⚠️ 字体加载失败 {font_path}: {e}')
                continue
    
    # 定义样式
    if font_registered:
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontName=font_name,
            fontSize=24,
            alignment=1,  # 居中
            spaceAfter=30
        )
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=12,
            leading=18
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName=font_name,
            fontSize=16,
            spaceBefore=20,
            spaceAfter=10
        )
    else:
        # 降级方案：使用英文
        title_style = styles['Heading1']
        normal_style = styles['Normal']
        heading_style = styles['Heading2']
    
    # 标题
    if font_registered:
        story.append(Paragraph("🦞 智能龙虾 - PDF 测试文档", title_style))
        story.append(Paragraph("能力验证测试文件", ParagraphStyle('Subtitle', parent=normal_style, alignment=1, fontSize=14)))
    else:
        story.append(Paragraph("Smart Lobster - PDF Test Document", title_style))
        story.append(Paragraph("Capability Verification Test", normal_style))
    
    story.append(Spacer(1, 0.5*inch))
    
    # 基本信息
    story.append(Paragraph("1️⃣ 基本信息", heading_style))
    info_text = f"""
    生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}<br/>
    生成者：大娃 (SF-0001)<br/>
    测试地点：贵阳<br/>
    PDF 库：reportlab
    """
    story.append(Paragraph(info_text, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # 功能列表
    story.append(Paragraph("2️⃣ 支持的 PDF 功能", heading_style))
    features = """
    • 多页面支持<br/>
    • 标题和段落样式<br/>
    • 表格生成<br/>
    • 中文字体支持<br/>
    • 自定义颜色<br/>
    • 图形绘制（线条、矩形、圆形）
    """
    story.append(Paragraph(features, normal_style))
    story.append(Spacer(1, 0.3*inch))
    
    # 表格示例
    story.append(Paragraph("3️⃣ 表格示例", heading_style))
    
    table_data = [
        ['功能', '状态', '备注'],
        ['PDF 生成', '✅ 正常', 'reportlab'],
        ['表格支持', '✅ 正常', '3 列 4 行'],
        ['中文支持', '✅ 正常' if font_registered else '⚠️ 英文', 'Noto Sans CJK' if font_registered else 'Fallback']
    ]
    
    table = Table(table_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 0.5*inch))
    
    # 结束
    story.append(Paragraph("—" * 40, ParagraphStyle('Divider', parent=normal_style, alignment=1)))
    story.append(Paragraph("测试完成！✅", ParagraphStyle('Final', parent=normal_style, alignment=1, fontSize=16)))
    
    # 构建 PDF
    doc.build(story)
    print(f'✅ PDF 文档已生成：{output_path}')
    return output_path

if __name__ == '__main__':
    create_test_pdf()
