#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
塔罗牌小阿卡纳 56 张批量生成脚本
四组：权杖/圣杯/宝剑/星币，每组 14 张（Ace-10 + 宫廷牌）
"""

import json
import subprocess
import time
from pathlib import Path

# 配置
API_URL = "http://localhost:8000/v1/images/generations"
API_KEY = "7b0a5827a36c46bdf896ec87f864da9e"
OUTPUT_DIR = Path("/home/admin/.openclaw/workspace/tarot/images/cards/minor")

# 小阿卡纳 56 张
minor_arcana = {
    # 权杖组 (Wands) - 火元素
    "wands": [
        ("wands_ace", "权杖 Ace", "一只手从云中伸出，握着一根发芽的权杖，深蓝色背景，银色边框"),
        ("wands_02", "权杖 2", "一个人站在城墙上，手持地球仪眺望远方，身边有一根权杖，深蓝色背景，银色边框"),
        ("wands_03", "权杖 3", "一个人站在高处，手持一根权杖，眺望远方的船，深蓝色背景，银色边框"),
        ("wands_04", "权杖 4", "四个人在庆祝，头顶花环，背景是城堡，四根权杖在周围，深蓝色背景，银色边框"),
        ("wands_05", "权杖 5", "五个人拿着权杖互相争斗，深蓝色背景，银色边框"),
        ("wands_06", "权杖 6", "一个人骑着白马，手持挂有花环的权杖，人群欢呼，深蓝色背景，银色边框"),
        ("wands_07", "权杖 7", "一个人站在高处，手持权杖对抗下方的六根权杖，深蓝色背景，银色边框"),
        ("wands_08", "权杖 8", "八根权杖在空中飞行，背景是天空，深蓝色背景，银色边框"),
        ("wands_09", "权杖 9", "一个人受伤但依然站立，手持权杖，背后有八根权杖，深蓝色背景，银色边框"),
        ("wands_10", "权杖 10", "一个人抱着十根权杖艰难前行，背景是城镇，深蓝色背景，银色边框"),
        ("wands_page", "权杖侍从", "一个年轻人手持权杖，眺望远方，深蓝色背景，银色边框"),
        ("wands_knight", "权杖骑士", "一个骑士骑着马，手持权杖奔驰，深蓝色背景，银色边框"),
        ("wands_queen", "权杖王后", "一位王后坐在宝座上，手持权杖，脚边有黑猫，深蓝色背景，银色边框"),
        ("wands_king", "权杖国王", "一位国王坐在宝座上，手持权杖，背景是沙漠，深蓝色背景，银色边框"),
    ],
    
    # 圣杯组 (Cups) - 水元素
    "cups": [
        ("cups_ace", "圣杯 Ace", "一只手从云中伸出，握着一个溢出水的圣杯，深蓝色背景，银色边框"),
        ("cups_02", "圣杯 2", "一男一女互相举杯，中间有赫尔墨斯之杖，深蓝色背景，银色边框"),
        ("cups_03", "圣杯 3", "三个女性举杯庆祝，背景是丰收的田野，深蓝色背景，银色边框"),
        ("cups_04", "圣杯 4", "一个人坐在树下，面前有三个圣杯，云中伸出一只手递来第四个，深蓝色背景，银色边框"),
        ("cups_05", "圣杯 5", "一个人低头看着地上倒下的三个圣杯，背后有两个立着的，深蓝色背景，银色边框"),
        ("cups_06", "圣杯 6", "两个孩子在院子里，一个孩子递出装满花的圣杯，深蓝色背景，银色边框"),
        ("cups_07", "圣杯 7", "一个人面对云中的七个圣杯，每个杯中有不同幻象，深蓝色背景，银色边框"),
        ("cups_08", "圣杯 8", "一个人离开八个圣杯，走向远方的山脉，深蓝色背景，银色边框"),
        ("cups_09", "圣杯 9", "一个人坐在桌前，面前排列着九个圣杯，表情满足，深蓝色背景，银色边框"),
        ("cups_10", "圣杯 10", "一家人在彩虹下，十个圣杯在空中排列，深蓝色背景，银色边框"),
        ("cups_page", "圣杯侍从", "一个年轻人手持圣杯，凝视杯中，深蓝色背景，银色边框"),
        ("cups_knight", "圣杯骑士", "一个骑士骑着马，手持圣杯缓缓前行，深蓝色背景，银色边框"),
        ("cups_queen", "圣杯王后", "一位王后坐在宝座上，手持圣杯，脚边有河流，深蓝色背景，银色边框"),
        ("cups_king", "圣杯国王", "一位国王坐在宝座上，手持圣杯和权杖，深蓝色背景，银色边框"),
    ],
    
    # 宝剑组 (Swords) - 风元素
    "swords": [
        ("swords_ace", "宝剑 Ace", "一只手从云中伸出，握着一把宝剑，剑尖有王冠，深蓝色背景，银色边框"),
        ("swords_02", "宝剑 2", "一个蒙眼女性交叉手持两把宝剑，背景是海洋，深蓝色背景，银色边框"),
        ("swords_03", "宝剑 3", "三把宝剑刺穿一颗心，背景是乌云和雨，深蓝色背景，银色边框"),
        ("swords_04", "宝剑 4", "一个骑士躺在教堂里，墙上挂着三把宝剑，手边有一把，深蓝色背景，银色边框"),
        ("swords_05", "宝剑 5", "五个人拿着宝剑，地上有两把倒下的宝剑，背景是乌云，深蓝色背景，银色边框"),
        ("swords_06", "宝剑 6", "一个人划船，船上有六把宝剑，驶向远方，深蓝色背景，银色边框"),
        ("swords_07", "宝剑 7", "一个人偷偷拿走五把宝剑中的四把，背景是军营，深蓝色背景，银色边框"),
        ("swords_08", "宝剑 8", "一个被蒙眼的人被八把宝剑包围，深蓝色背景，银色边框"),
        ("swords_09", "宝剑 9", "一个人从噩梦中惊醒，墙上挂着九把宝剑，深蓝色背景，银色边框"),
        ("swords_10", "宝剑 10", "一个人趴在地上，背上插着十把宝剑，远方是黎明，深蓝色背景，银色边框"),
        ("swords_page", "宝剑侍从", "一个年轻人手持宝剑，眺望远方，深蓝色背景，银色边框"),
        ("swords_knight", "宝剑骑士", "一个骑士骑着马，手持宝剑冲锋，深蓝色背景，银色边框"),
        ("swords_queen", "宝剑王后", "一位王后坐在宝座上，手持宝剑，背景是乌云，深蓝色背景，银色边框"),
        ("swords_king", "宝剑国王", "一位国王坐在宝座上，手持宝剑和权杖，深蓝色背景，银色边框"),
    ],
    
    # 星币组 (Pentacles) - 土元素
    "pentacles": [
        ("pentacles_ace", "星币 Ace", "一只手从云中伸出，握着一枚大星币，深蓝色背景，银色边框"),
        ("pentacles_02", "星币 2", "一个人玩弄两枚星币，形成无限符号，背景是海洋，深蓝色背景，银色边框"),
        ("pentacles_03", "星币 3", "一个工匠在教堂里工作，另外两人观看，深蓝色背景，银色边框"),
        ("pentacles_04", "星币 4", "一个人紧紧抱住四枚星币，不愿放手，深蓝色背景，银色边框"),
        ("pentacles_05", "星币 5", "两个乞丐在雪地里行走，路过教堂的彩色玻璃窗，深蓝色背景，银色边框"),
        ("pentacles_06", "星币 6", "一个商人分发星币给乞丐，手持天平，深蓝色背景，银色边框"),
        ("pentacles_07", "星币 7", "一个人靠在锄头上，看着六枚星币生长在藤蔓上，深蓝色背景，银色边框"),
        ("pentacles_08", "星币 8", "一个工匠专注地雕刻星币，桌上有七枚，深蓝色背景，银色边框"),
        ("pentacles_09", "星币 9", "一位女性在花园中，手持猎鹰，周围有九枚星币，深蓝色背景，银色边框"),
        ("pentacles_10", "星币 10", "一个家族场景，老人、夫妻、孩子，十枚星币排列，深蓝色背景，银色边框"),
        ("pentacles_page", "星币侍从", "一个年轻人手持星币，凝视，深蓝色背景，银色边框"),
        ("pentacles_knight", "星币骑士", "一个骑士骑着马，手持星币缓缓前行，深蓝色背景，银色边框"),
        ("pentacles_queen", "星币王后", "一位王后坐在宝座上，手持星币，脚边有兔子，深蓝色背景，银色边框"),
        ("pentacles_king", "星币国王", "一位国王坐在宝座上，手持星币和权杖，深蓝色背景，银色边框"),
    ],
}

def generate_card(filename, card_name, description):
    """生成单张牌"""
    # 构建提示词
    prompt = f"塔罗牌牌面【{card_name}】，深蓝色底色，银色装饰花纹边框，四角有精美装饰，星空元素点缀，神秘学风格，2K 高清。牌面内容：{description}"
    
    print(f"🃏 生成：{card_name}", end=" ")
    
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
            print(f"✅ ({size:.1f}MB)")
            return True
        else:
            print(f"❌ 文件太小 ({size:.1f}MB)")
            return False
    except Exception as e:
        print(f"❌ 错误：{e}")
        return False

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    print("🔮 开始生成小阿卡纳 56 张牌面...\n")
    
    total = 0
    success = 0
    
    for suit_name, cards in minor_arcana.items():
        print(f"\n=== {suit_name.upper()} 组 ===\n")
        
        for filename, card_name, description in cards:
            output_path = OUTPUT_DIR / f"{filename}.jpg"
            
            # 跳过已存在的
            if output_path.exists() and output_path.stat().st_size > 1024*1024:
                print(f"⏭️  跳过：{card_name}")
                success += 1
                total += 1
                continue
            
            total += 1
            result = generate_card(filename, card_name, description)
            if result:
                success += 1
            
            # 避免请求过快，等待 3 秒
            time.sleep(3)
    
    print(f"\n✅ 小阿卡纳生成完成！")
    print(f"📊 成功：{success}/{total} 张")

if __name__ == "__main__":
    main()
