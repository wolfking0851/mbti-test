#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
塔罗牌图片压缩优化脚本
目标：减小 50% 体积，保持清晰度
"""

from PIL import Image
import os
from pathlib import Path

def optimize_image(input_path, output_path, quality=85, max_size=2000):
    """优化单张图片"""
    try:
        img = Image.open(input_path)
        
        # 调整尺寸（如果太大）
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        
        # 保存为优化后的 JPG
        img.save(
            output_path,
            'JPEG',
            quality=quality,
            optimize=True,
            progressive=True
        )
        
        # 计算压缩率
        original_size = os.path.getsize(input_path)
        optimized_size = os.path.getsize(output_path)
        reduction = (1 - optimized_size / original_size) * 100
        
        return {
            'success': True,
            'original': original_size / 1024 / 1024,
            'optimized': optimized_size / 1024 / 1024,
            'reduction': reduction
        }
    except Exception as e:
        return {'success': False, 'error': str(e)}

def main():
    base_dir = Path('/home/admin/.openclaw/workspace/tarot/images')
    
    # 创建优化目录
    optimized_dir = base_dir / 'optimized'
    optimized_dir.mkdir(exist_ok=True)
    
    # 复制背面和边框
    (optimized_dir / 'back').mkdir(exist_ok=True)
    (optimized_dir / 'border').mkdir(exist_ok=True)
    (optimized_dir / 'cards' / 'major').mkdir(parents=True, exist_ok=True)
    (optimized_dir / 'cards' / 'minor').mkdir(parents=True, exist_ok=True)
    
    print("🔮 开始优化塔罗牌图片...\n")
    
    total = 0
    success = 0
    total_reduction = 0
    
    # 优化所有图片
    for subdir in ['back', 'border', 'cards/major', 'cards/minor']:
        src_dir = base_dir / subdir
        dst_dir = optimized_dir / subdir
        
        if not src_dir.exists():
            continue
        
        for src_file in src_dir.glob('*.jpg'):
            total += 1
            dst_file = dst_dir / src_file.name
            
            result = optimize_image(src_file, dst_file)
            
            if result['success']:
                success += 1
                total_reduction += result['reduction']
                print(f"✅ {src_file.name}: {result['original']:.1f}MB → {result['optimized']:.1f}MB (-{result['reduction']:.1f}%)")
            else:
                print(f"❌ {src_file.name}: {result['error']}")
    
    avg_reduction = total_reduction / success if success > 0 else 0
    
    print(f"\n📊 优化完成！")
    print(f"   成功：{success}/{total} 张")
    print(f"   平均压缩率：-{avg_reduction:.1f}%")
    
    # 计算总大小
    original_total = sum(f.stat().st_size for f in base_dir.rglob('*.jpg'))
    optimized_total = sum(f.stat().st_size for f in optimized_dir.rglob('*.jpg'))
    
    print(f"\n💾 总体积：{original_total/1024/1024:.1f}MB → {optimized_total/1024/1024:.1f}MB (-{(1-optimized_total/original_total)*100:.1f}%)")

if __name__ == "__main__":
    main()
