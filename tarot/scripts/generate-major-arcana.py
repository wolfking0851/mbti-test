#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
塔罗牌大阿卡纳 22 张批量生成脚本
每张牌都明确：牌名 + 边框描述 + 牌面内容
"""

import json
import subprocess
import time
from pathlib import Path

# 配置
API_URL = "http://localhost:8000/v1/images/generations"
API_KEY = "7b0a5827a36c46bdf896ec87f864da9e"
OUTPUT_DIR = Path("/home/admin/.openclaw/workspace/tarot/images/cards/major")

# 大阿卡纳 22 张 - 完整提示词
major_arcana = [
    ("00_fool", "0 号牌 - 愚人", "一个年轻人站在悬崖边，穿着彩色衣服，背着行囊，手持白玫瑰，仰望天空，脚边有一只小白狗，远方是雪山，充满希望和冒险精神"),
    ("01_magician", "1 号牌 - 魔术师", "一个人站在桌前，穿着红色长袍，桌上有四种元素符号：权杖、圣杯、宝剑、星币，一只手手指天空，另一只手指向大地，头顶有无限符号"),
    ("02_high_priestess", "2 号牌 - 女祭司", "一位女性坐在月亮前的宝座上，穿着蓝色长袍，手持卷轴，身后是黑白柱子，脚下有新月"),
    ("03_empress", "3 号牌 - 皇后", "一位怀孕的女性坐在森林中的宝座上，穿着红色长裙，头戴十二星冠，手持权杖，周围是麦田和流水"),
    ("04_emperor", "4 号牌 - 皇帝", "一位国王坐在石制宝座上，穿着盔甲，手持权杖和宝球，背景是荒凉的山脉"),
    ("05_hierophant", "5 号牌 - 教皇", "一位宗教领袖坐在教堂宝座上，穿着三层冠冕，手持三重权杖，面前有两个信徒"),
    ("06_lovers", "6 号牌 - 恋人", "一个男人和一个女人站在伊甸园中，上方有天使祝福，背后有智慧树和生命树"),
    ("07_chariot", "7 号牌 - 战车", "一位战士站在战车上，穿着盔甲，战车由两只狮身人面兽拉动，一手握缰绳，一手持权杖"),
    ("08_strength", "8 号牌 - 力量", "一位女性温柔地抚摸狮子的嘴，穿着白色长袍，头顶有无限符号"),
    ("09_hermit", "9 号牌 - 隐士", "一位老人在雪山上独行，手持灯笼（内有六角星），另一手持手杖"),
    ("10_wheel", "10 号牌 - 命运之轮", "一个巨大的轮子，上面有各种符号，轮子周围有四个生物：人、鹰、牛、狮"),
    ("11_justice", "11 号牌 - 正义", "一位女性坐在石柱之间，一手持剑，一手持天平"),
    ("12_hanged_man", "12 号牌 - 倒吊人", "一个人倒吊在树上，双脚被绑，双手放在背后，头部有光环"),
    ("13_death", "13 号牌 - 死神", "一个骷髅骑士骑着白马，手持黑色旗帜，地上有倒下的人，远方太阳升起"),
    ("14_temperance", "14 号牌 - 节制", "一位天使站在地上，一只脚在水中，手持两个杯子互相倒水"),
    ("15_devil", "15 号牌 - 恶魔", "一个有翅膀的恶魔站在石台上，下方有一男一女被锁链束缚"),
    ("16_tower", "16 号牌 - 高塔", "一座高塔被闪电击中，塔顶掉落，有人从塔中坠落"),
    ("17_star", "17 号牌 - 星星", "一位女性在星空下倒水，一个水壶倒向大地，一个倒向河流，天空有八颗星星"),
    ("18_moon", "18 号牌 - 月亮", "夜空中有巨大的月亮，地上有一只狗和一只狼对着月亮吠叫，池塘里有龙虾爬出"),
    ("19_sun", "19 号牌 - 太阳", "一个小孩骑着白马，手持红旗，背景是巨大的太阳和向日葵"),
    ("20_judgement", "20 号牌 - 审判", "天使在云端吹响号角，人们从棺材中复活，举起双手"),
    ("21_world", "21 号牌 - 世界", "一个舞者在花环中舞蹈，手持两根权杖，四周有四个生物"),
]

def generate_card(filename, card_name, description):
    """生成单张牌"""
    # 构建提示词 - 明确牌号 + 边框描述 + 牌面内容
    prompt = f"塔罗牌牌面【{card_name}】，深蓝色底色，银色装饰花纹边框，四角有精美装饰，星空元素点缀，神秘学风格，2K 高清。牌面内容：{description}"
    
    print(f"🃏 生成：{card_name}")
    
    # 调用 API
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
        "-o", "/tmp/card_raw.json"
    ]
    
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # 解析 JSON 获取 URL
    try:
        with open("/tmp/card_raw.json", 'r') as f:
            data = json.load(f)
            img_url = data['data'][0]['url']
        
        # 下载图片
        output_path = OUTPUT_DIR / f"{filename}.jpg"
        download_cmd = ["curl", "-L", img_url, "-o", str(output_path)]
        subprocess.run(download_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # 检查文件大小
        size = output_path.stat().st_size / 1024 / 1024
        if size > 1:  # 大于 1MB 才算成功
            print(f"✅ 成功 ({size:.1f}MB)")
            return True
        else:
            print(f"❌ 文件太小 ({size:.1f}MB)，可能失败")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🔮 开始生成大阿卡纳 22 张牌面...\n")
    
    for i, (filename, card_name, description) in enumerate(major_arcana):
        output_path = OUTPUT_DIR / f"{filename}.jpg"
        
        # 跳过已存在的
        if output_path.exists() and output_path.stat().st_size > 1024*1024:
            print(f"⏭️  跳过已存在：{card_name}")
            continue
        
        print(f"\n[{i+1}/22] ", end="")
        success = generate_card(filename, card_name, description)
        
        if not success:
            print(f"⚠️  {card_name} 生成失败，稍后重试")
        
        # 避免请求过快，等待 3 秒
        time.sleep(3)
    
    print("\n✅ 大阿卡纳生成完成！")
    
    # 统计
    files = list(OUTPUT_DIR.glob("*.jpg"))
    print(f"📊 共生成 {len(files)} 张牌")

if __name__ == "__main__":
    main()
