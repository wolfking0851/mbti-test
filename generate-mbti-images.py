#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成 MBTI 测试图片（24 张）
风格：中国风 + 3D 渲染
"""

import requests
import json
from pathlib import Path
import time

# 配置
API_URL = "http://localhost:8000/v1/images/generations"
SESSION_ID = "7b0a5827a36c46bdf896ec87f864da9e"
OUTPUT_DIR = Path("/home/admin/.openclaw/workspace/mbti-images/images")

# 确保输出目录存在
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 24 张图片的提示词
PROMPTS = [
    # E/I 维度（6 张）
    {"file": "round1_optionA.jpg", "prompt": "3D 渲染，中国风，热闹的古代宴会场景，灯火通明，宾客满座，欢声笑语，暖色调，精细渲染，8K 高清，Blender 渲染，皮克斯风格"},
    {"file": "round1_optionB.jpg", "prompt": "3D 渲染，中国风，安静的书房场景，一人独坐窗前，月光洒落，茶香袅袅，冷色调，精细渲染，8K 高清，Blender 渲染，皮克斯风格"},
    {"file": "round2_optionA.jpg", "prompt": "3D 渲染，中国风，热闹的庙会场景，舞龙舞狮，人群聚集，色彩鲜艳，动态感强，精细渲染，8K 高清，Blender 渲染"},
    {"file": "round2_optionB.jpg", "prompt": "3D 渲染，中国风，幽静的竹林小院，一人品茶看书，竹叶婆娑，宁静致远，精细渲染，8K 高清，Blender 渲染"},
    {"file": "round3_optionA.jpg", "prompt": "3D 渲染，中国风，热闹的集市，主动与人交谈，笑容满面，阳光明媚，精细渲染，8K 高清，Blender 渲染"},
    {"file": "round3_optionB.jpg", "prompt": "3D 渲染，中国风，安静的庭院角落，静静观察周围，若有所思，光影柔和，精细渲染，8K 高清，Blender 渲染"},
    
    # S/N 维度（6 张）
    {"file": "round4_optionA.jpg", "prompt": "3D 渲染，中国风，古代工匠手把手教学，具体操作步骤，工具摆放整齐，细节清晰，精细渲染，8K 高清"},
    {"file": "round4_optionB.jpg", "prompt": "3D 渲染，中国风，智者仰望星空，思考宇宙哲理，星光璀璨，抽象概念，精细渲染，8K 高清"},
    {"file": "round5_optionA.jpg", "prompt": "3D 渲染，中国风，详细的账本记录，数字清晰，物品清单，具体实在，精细渲染，8K 高清"},
    {"file": "round5_optionB.jpg", "prompt": "3D 渲染，中国风，水墨山水画，意境深远，留白想象空间，抽象艺术，精细渲染，8K 高清"},
    {"file": "round6_optionA.jpg", "prompt": "3D 渲染，中国风，古老的石狮子，历史建筑，实实在在的证据，精细渲染，8K 高清"},
    {"file": "round6_optionB.jpg", "prompt": "3D 渲染，中国风，飘渺的仙境，云雾缭绕，神秘感，直觉指引，精细渲染，8K 高清"},
    
    # T/F 维度（6 张）
    {"file": "round7_optionA.jpg", "prompt": "3D 渲染，中国风，古代判官断案，逻辑分析，天平称量，理性公正，精细渲染，8K 高清"},
    {"file": "round7_optionB.jpg", "prompt": "3D 渲染，中国风，家人团聚场景，温情脉脉，情感交流，暖色调，精细渲染，8K 高清"},
    {"file": "round8_optionA.jpg", "prompt": "3D 渲染，中国风，直言进谏的臣子，严肃表情，指出问题，理性态度，精细渲染，8K 高清"},
    {"file": "round8_optionB.jpg", "prompt": "3D 渲染，中国风，温柔安慰的场景，轻拍肩膀，关怀眼神，暖色调，精细渲染，8K 高清"},
    {"file": "round9_optionA.jpg", "prompt": "3D 渲染，中国风，谋士运筹帷幄，冷静分析，智慧光芒，理性气质，精细渲染，8K 高清"},
    {"file": "round9_optionB.jpg", "prompt": "3D 渲染，中国风，医者仁心，温柔关怀，救助他人，暖色调，精细渲染，8K 高清"},
    
    # J/P 维度（6 张）
    {"file": "round10_optionA.jpg", "prompt": "3D 渲染，中国风，详细的行程卷轴，时间规划，路线清晰，井井有条，精细渲染，8K 高清"},
    {"file": "round10_optionB.jpg", "prompt": "3D 渲染，中国风，侠客仗剑天涯，随性而行，云游四方，自由自在，精细渲染，8K 高清"},
    {"file": "round11_optionA.jpg", "prompt": "3D 渲染，中国风，古代官府办公，文书整齐，流程规范，秩序井然，精细渲染，8K 高清"},
    {"file": "round11_optionB.jpg", "prompt": "3D 渲染，中国风，文人随性创作，灵感迸发，不拘一格，自由挥洒，精细渲染，8K 高清"},
    {"file": "round12_optionA.jpg", "prompt": "3D 渲染，中国风，提前完成任务，从容不迫，时间充裕，精细渲染，8K 高清"},
    {"file": "round12_optionB.jpg", "prompt": "3D 渲染，中国风，最后一刻赶工，紧张但完成，压线完成，精细渲染，8K 高清"},
]

def generate_image(prompt, output_file):
    """生成单张图片"""
    try:
        headers = {
            "Authorization": f"Bearer {SESSION_ID}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "jimeng-5.0-preview",
            "prompt": prompt,
            "n": 1,
            "ratio": "1:1",
            "resolution": "2k"
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        data = response.json()
        
        if 'data' in data and len(data['data']) > 0:
            image_url = data['data'][0]['url']
            
            # 下载图片
            img_response = requests.get(image_url, timeout=60)
            with open(output_file, 'wb') as f:
                f.write(img_response.content)
            
            return True, "成功"
        else:
            return False, f"API 返回错误：{data}"
    
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 60)
    print("开始生成 MBTI 测试图片（24 张）")
    print("风格：中国风 + 3D 渲染")
    print("=" * 60)
    print()
    
    success_count = 0
    fail_count = 0
    
    for i, item in enumerate(PROMPTS, 1):
        output_file = OUTPUT_DIR / item["file"]
        
        # 如果文件已存在，跳过
        if output_file.exists():
            print(f"[{i}/24] ⏭️  跳过：{item['file']}（已存在）")
            success_count += 1
            continue
        
        print(f"[{i}/24] 生成：{item['file']}")
        print(f"      提示词：{item['prompt'][:50]}...")
        
        success, message = generate_image(item["prompt"], output_file)
        
        if success:
            file_size = output_file.stat().st_size / 1024
            print(f"      ✅ 成功！文件大小：{file_size:.0f}KB")
            success_count += 1
        else:
            print(f"      ❌ 失败：{message}")
            fail_count += 1
        
        # 避免限流，等待 2 秒
        time.sleep(2)
    
    print()
    print("=" * 60)
    print(f"生成完成！")
    print(f"成功：{success_count}/24")
    print(f"失败：{fail_count}/24")
    print("=" * 60)

if __name__ == "__main__":
    main()
