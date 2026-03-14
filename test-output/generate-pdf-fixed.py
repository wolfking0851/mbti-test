#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PDF 生成 - 修复表格中文字体显示问题
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

def create_pdf():
    output_path = '/home/admin/.openclaw/workspace/test-output/测试文档-PDF-修复版.pdf'
    
    # 创建文档
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    story = []
    styles = getSampleStyleSheet()
    
    # 注册文泉驿微米黑字体
    font_path = '/usr/share/fonts/wqy-microhei/wqy-microhei.ttc'
    pdfmetrics.registerFont(TTFont('WenQuanYi', font_path))
    print(f'✅ 已注册字体：{font_path}')
    
    # 定义样式 - 所有样式都使用 WenQuanYi 字体
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName='WenQuanYi',
        fontSize=20,
        alignment=1,
        spaceAfter=20
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontName='WenQuanYi',
        fontSize=12,
        leading=18
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontName='WenQuanYi',
        fontSize=14,
        spaceBefore=15,
        spaceAfter=8
    )
    
    # 标题
    story.append(Paragraph('智能龙虾 - PDF 测试文档', title_style))
    story.append(Paragraph(f'生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', normal_style))
    story.append(Paragraph('生成者：大娃 (SF-0001)', normal_style))
    story.append(Paragraph('地点：贵阳', normal_style))
    story.append(Spacer(1, 15))
    
    # 功能列表
    story.append(Paragraph('1. 功能列表', heading_style))
    story.append(Paragraph('• PDF 文档生成', normal_style))
    story.append(Paragraph('• 中文字体支持', normal_style))
    story.append(Paragraph('• 表格生成', normal_style))
    story.append(Paragraph('• 样式定制', normal_style))
    story.append(Spacer(1, 15))
    
    # 表格 - 关键修复：表格内容使用 Paragraph 包裹，确保字体正确
    story.append(Paragraph('2. 表格示例', heading_style))
    
    # 表格数据 - 每个单元格都用 Paragraph 包裹，指定字体
    table_data = [
        [Paragraph('功能', normal_style), Paragraph('状态', normal_style), Paragraph('备注', normal_style)],
        [Paragraph('PDF 生成', normal_style), Paragraph('正常', normal_style), Paragraph('reportlab', normal_style)],
        [Paragraph('中文支持', normal_style), Paragraph('正常', normal_style), Paragraph('文泉驿微米黑', normal_style)],
        [Paragraph('表格显示', normal_style), Paragraph('正常', normal_style), Paragraph('已修复字体', normal_style)]
    ]
    
    table = Table(table_data, colWidths=[100, 80, 120])
    table.setStyle(TableStyle([
        # 表头
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'WenQuanYi'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        
        # 数据行
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, 1), (-1, -1), 'WenQuanYi'),
        ('FONTSIZE', (0, 1), (-1, -1), 11),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 20))
    
    # 结束
    story.append(Paragraph('—' * 30, ParagraphStyle('Divider', parent=normal_style, alignment=1)))
    story.append(Paragraph('测试完成！', ParagraphStyle('End', parent=normal_style, alignment=1, fontSize=14)))
    
    # 构建 PDF
    doc.build(story)
    print(f'✅ PDF 已生成：{output_path}')
    return output_path

if __name__ == '__main__':
    create_pdf()
