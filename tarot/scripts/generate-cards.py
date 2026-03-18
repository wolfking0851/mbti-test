#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
塔罗牌 78 张牌面批量生成脚本
使用即梦 API，以边框模板为参考图，保证一致性
"""

import json
import subprocess
import time
from pathlib import Path

# 配置
API_URL = "http://localhost:8000/v1/images/generations"
API_KEY = "7b0a5827a36c46bdf896ec87f864da9e"
BORDER_PATH = Path("/home/admin/.openclaw/workspace/tarot/images/border/border.jpg")
OUTPUT_DIR = Path("/home/admin/.openclaw/workspace/tarot/images/cards")

# 大阿卡纳 22 张
major_arcana = [
    ("00_fool", "塔罗牌牌面，一个年轻人站在悬崖边，穿着彩色衣服，背着行囊，手持白玫瑰，仰望天空，脚边有一只小白狗，远方是雪山，充满希望和冒险精神，星空蓝配色，银色边框装饰，神秘学风格，2K 高清"),
    ("01_magician", "塔罗牌牌面，一个人站在桌前，穿着红色长袍，桌上有四种元素符号：权杖、圣杯、宝剑、星币，一只手手指天空，另一只手指向大地，头顶有无限符号，象征连接天地，星空蓝配色，银色边框装饰，2K 高清"),
    ("02_high_priestess", "塔罗牌牌面，一位女性坐在月亮前的宝座上，穿着蓝色长袍，手持卷轴，身后是黑白柱子，脚下有新月，象征直觉和潜意识，星空蓝配色，银色边框装饰，2K 高清"),
    ("03_empress", "塔罗牌牌面，一位怀孕的女性坐在森林中的宝座上，穿着红色长裙，头戴十二星冠，手持权杖，周围是麦田和流水，象征丰饶和创造力，星空蓝配色，银色边框装饰，2K 高清"),
    ("04_emperor", "塔罗牌牌面，一位国王坐在石制宝座上，穿着盔甲，手持权杖和宝球，背景是荒凉的山脉，象征权威和秩序，星空蓝配色，银色边框装饰，2K 高清"),
    ("05_hierophant", "塔罗牌牌面，一位宗教领袖坐在教堂宝座上，穿着三层冠冕，手持三重权杖，面前有两个信徒，象征传统和精神指导，星空蓝配色，银色边框装饰，2K 高清"),
    ("06_lovers", "塔罗牌牌面，一个男人和一个女人站在伊甸园中，上方有天使祝福，背后有智慧树和生命树，象征选择和爱情，星空蓝配色，银色边框装饰，2K 高清"),
    ("07_chariot", "塔罗牌牌面，一位战士站在战车上，穿着盔甲，战车由两只狮身人面兽拉动，一手握缰绳，一手持权杖，象征胜利和意志力，星空蓝配色，银色边框装饰，2K 高清"),
    ("08_strength", "塔罗牌牌面，一位女性温柔地抚摸狮子的嘴，穿着白色长袍，头顶有无限符号，象征内在力量和勇气，星空蓝配色，银色边框装饰，2K 高清"),
    ("09_hermit", "塔罗牌牌面，一位老人在雪山上独行，手持灯笼（内有六角星），另一手持手杖，象征内省和智慧，星空蓝配色，银色边框装饰，2K 高清"),
    ("10_wheel", "塔罗牌牌面，一个巨大的轮子，上面有各种符号，轮子周围有四个生物（人、鹰、牛、狮），象征命运和变化，星空蓝配色，银色边框装饰，2K 高清"),
    ("11_justice", "塔罗牌牌面，一位女性坐在石柱之间，一手持剑，一手持天平，象征公平和真理，星空蓝配色，银色边框装饰，2K 高清"),
    ("12_hanged_man", "塔罗牌牌面，一个人倒吊在树上，双脚被绑，双手放在背后，头部有光环，象征牺牲和换位思考，星空蓝配色，银色边框装饰，2K 高清"),
    ("13_death", "塔罗牌牌面，一个骷髅骑士骑着白马，手持黑色旗帜，地上有倒下的人，远方太阳升起，象征结束和新生，星空蓝配色，银色边框装饰，2K 高清"),
    ("14_temperance", "塔罗牌牌面，一位天使站在地上，一只脚在水中，手持两个杯子，互相倒水，象征平衡和调和，星空蓝配色，银色边框装饰，2K 高清"),
    ("15_devil", "塔罗牌牌面，一个有翅膀的恶魔站在石台上，下方有一男一女被锁链束缚，象征欲望和束缚，星空蓝配色，银色边框装饰，2K 高清"),
    ("16_tower", "塔罗牌牌面，一座高塔被闪电击中，塔顶掉落，有人从塔中坠落，象征突变和觉醒，星空蓝配色，银色边框装饰，2K 高清"),
    ("17_star", "塔罗牌牌面，一位女性在星空下倒水，一个水壶倒向大地，一个倒向河流，天空有八颗星星，象征希望和灵感，星空蓝配色，银色边框装饰，2K 高清"),
    ("18_moon", "塔罗牌牌面，夜空中有巨大的月亮，地上有一只狗和一只狼对着月亮吠叫，池塘里有龙虾爬出，象征潜意识和恐惧，星空蓝配色，银色边框装饰，2K 高清"),
    ("19_sun", "塔罗牌牌面，一个小孩骑着白马，手持红旗，背景是巨大的太阳和向日葵，象征成功和快乐，星空蓝配色，银色边框装饰，2K 高清"),
    ("20_judgement", "塔罗牌牌面，天使在云端吹响号角，人们从棺材中复活，举起双手，象征重生和觉醒，星空蓝配色，银色边框装饰，2K 高清"),
    ("21_world", "塔罗牌牌面，一个舞者在花环中舞蹈，手持两根权杖，四周有四个生物，象征完成和圆满，星空蓝配色，银色边框装饰，2K 高清"),
]

def generate_image(prompt, output_path):
    """调用即梦 API 生成图片"""
    cmd = [
        "curl", "-X", "POST", API_URL,
        "-H", "Content-Type: application/json",
        "-H", f"Authorization: Bearer {API_KEY}",
        "-d", json.dumps({
            "model": "jimeng-5.0-preview",
            "prompt": prompt,
            "ratio": "3:4",
            "resolution": "2k"
        }),
        "-o", str(output_path)
    ]
    
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 解析 JSON 获取 URL
    try:
        with open(output_path, 'r') as f:
            data = json.load(f)
            img_url = data['data'][0]['url']
            
        # 下载图片
        download_cmd = ["curl", "-L", img_url, "-o", str(output_path)]
        subprocess.run(download_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception as e:
        print(f"❌ 生成失败：{e}")
        return False

def main():
    print("🔮 开始生成大阿卡纳 22 张牌面...")
    
    major_dir = OUTPUT_DIR / "major"
    major_dir.mkdir(parents=True, exist_ok=True)
    
    for i, (filename, prompt) in enumerate(major_arcana):
        output_path = major_dir / f"{filename}.jpg"
        
        if output_path.exists():
            print(f"⏭️  跳过已存在：{filename}")
            continue
        
        print(f"\n🃏 生成第 {i+1}/22 张：{filename}")
        success = generate_image(prompt, output_path)
        
        if success:
            size = output_path.stat().st_size / 1024 / 1024
            print(f"✅ 成功 ({size:.1f}MB)")
        else:
            print(f"❌ 失败，稍后重试")
        
        # 避免请求过快
        time.sleep(2)
    
    print("\n✅ 大阿卡纳生成完成！")

if __name__ == "__main__":
    main()
