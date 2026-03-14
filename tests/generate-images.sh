#!/bin/bash
# MBTI 测试图片批量生成脚本

SESSION_ID="7b0a5827a36c46bdf896ec87f864da9e"
API_URL="http://localhost:8000/v1/images/generations"
OUTPUT_DIR="/home/admin/.openclaw/workspace/web-mvp/images"

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

echo "🎨 开始生成 MBTI 测试图片..."
echo "输出目录：$OUTPUT_DIR"
echo ""

# 定义提示词数组（22 个）
declare -a prompts=(
  # 第 1 轮：E/I 维度
  "阳光洒满房间，窗外传来热闹的早市声音，手机收到朋友聚餐邀请，兴奋期待的表情，温馨家庭场景，手绘插画风格，明亮暖色调"
  "窗外下着小雨，房间安静温馨，裹紧被子享受独处，手边有书和热茶，放松满足的表情，室内场景，手绘插画风格，柔和冷色调"
  "手机不断收到消息提醒，朋友们在群里讨论下午活动，犹豫要不要参加，内心倾向去人多热闹，现代卧室场景，手绘插画风格，明亮色调"
  "手机调成静音，想着今天可以不社交，内心感到轻松，计划一个人看电影打游戏，舒适卧室场景，手绘插画风格，柔和色调"
  
  # 第 2 轮：E/I 维度
  "大家围成一圈玩破冰游戏，主动举手当队长，和陌生人聊天兴奋，活动结束想继续聚餐，团队活动场景，手绘插画风格，热闹氛围"
  "坐在角落安静观察，希望不要点名发言，活动结束松了口气，想快点回家休息，团队活动场景，手绘插画风格，安静氛围"
  "和熟悉的几个朋友一起玩，不主动但也不拒绝，有人邀请就参与，看心情决定，团队活动场景，手绘插画风格，中性氛围"
  
  # 第 3 轮：S/N 维度
  "老师给出详细操作步骤，每一步都有明确说明，跟着步骤一步步做，看到具体成果有成就感，学习场景，手绘插画风格，实用主义"
  "老师先讲整体框架和原理，喜欢问为什么是这样，步骤可以跳理解逻辑更重要，喜欢探索新方法，学习场景，手绘插画风格，理论主义"
  "看重实际案例，这个技能能用来做什么，喜欢动手实践，理论太多会走神，学习场景，手绘插画风格，实践导向"
  "思考这个技能的未来应用，喜欢联想其他领域，这个原理能不能用在别处，实践可以少概念要清晰，学习场景，手绘插画风格，概念导向"
  
  # 第 4 轮：S/N 维度
  "讨论剧情细节，那个场景拍得真美，演员表演很到位，记住具体的台词和画面，电影院场景，手绘插画风格，细节导向"
  "思考电影想表达的主题，这个隐喻是什么意思，联想到其他电影或书籍，讨论导演的创作意图，电影院场景，手绘插画风格，概念导向"
  
  # 第 5 轮：T/F 维度
  "直接指出问题所在，这里不对应该这样改，对事不对人，认为诚实最重要，对话场景，手绘插画风格，理性氛围"
  "先考虑朋友的感受，委婉地提醒或不说，Ta 可能已经很难过了，认为关系和谐最重要，对话场景，手绘插画风格，感性氛围"
  "分析错误的原因，给出改进建议，即使可能得罪人也要说，认为这是为朋友好，对话场景，手绘插画风格，分析氛围"
  "安慰朋友的情绪，等 Ta 主动问再说，用提问引导 Ta 自己发现，认为时机很重要，对话场景，手绘插画风格，关怀氛围"
  
  # 第 6 轮：J/P 维度
  "提前一周做好详细攻略，每天去哪里吃什么住哪里，精确到小时，不喜欢计划被打乱，计划场景，手绘插画风格，有序氛围"
  "只订机票和第一晚酒店，到了再说看心情，喜欢随性探索，计划赶不上变化，计划场景，手绘插画风格，随性氛围"
  "列好行李清单，提前查好天气，准备备用方案，讨厌丢三落四，计划场景，手绘插画风格，准备充分"
  "出发前随便收拾一下，缺什么当地买，喜欢意外惊喜，清单太麻烦，计划场景，手绘插画风格，随意氛围"
)

# 文件名数组
declare -a filenames=(
  "round1_optionA" "round1_optionB" "round1_optionC" "round1_optionD"
  "round2_optionA" "round2_optionB" "round2_optionC"
  "round3_optionA" "round3_optionB" "round3_optionC" "round3_optionD"
  "round4_optionA" "round4_optionB"
  "round5_optionA" "round5_optionB" "round5_optionC" "round5_optionD"
  "round6_optionA" "round6_optionB" "round6_optionC" "round6_optionD"
)

# 循环生成
for i in "${!prompts[@]}"; do
  filename="${filenames[$i]}"
  prompt="${prompts[$i]}"
  
  echo "[$((i+1))/22] 生成 $filename.png..."
  
  # 调用 API 生成图片
  response=$(curl -s -X POST "$API_URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $SESSION_ID" \
    -d "{\"model\":\"jimeng-5.0-preview\",\"prompt\":\"$prompt\",\"ratio\":\"1:1\",\"resolution\":\"2k\"}")
  
  # 检查是否成功
  if echo "$response" | grep -q '"url"'; then
    # 提取图片 URL
    image_url=$(echo "$response" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['data'][0]['url'])" 2>/dev/null)
    
    if [ -n "$image_url" ]; then
      # 下载图片
      curl -sL "$image_url" -o "$OUTPUT_DIR/$filename.png"
      
      # 检查下载是否成功
      if [ -f "$OUTPUT_DIR/$filename.png" ] && [ -s "$OUTPUT_DIR/$filename.png" ]; then
        echo "  ✅ $filename.png 完成！"
      else
        echo "  ❌ $filename.png 下载失败"
      fi
    else
      echo "  ❌ $filename.png URL 提取失败"
    fi
  else
    echo "  ❌ $filename.png 生成失败：$response"
  fi
  
  # 等待 2 秒避免限流
  sleep 2
done

echo ""
echo "🎉 批量生成完成！"
echo "输出目录：$OUTPUT_DIR"
echo ""
echo "生成的文件："
ls -lh "$OUTPUT_DIR"/*.png 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
