#!/bin/bash
#
# complete-task.sh - 任务完成后立即更新进度
#
# 用法：
#   ./complete-task.sh 1 MBTI
#   ./complete-task.sh 1 大五人格
#   ./complete-task.sh 2 抖音 Top20
#

if [ $# -lt 2 ]; then
    echo "用法：$0 <阶段 ID> <任务名称>"
    echo "示例：$0 1 MBTI"
    exit 1
fi

STAGE_ID=$1
TASK_NAME=$2

cd "$(dirname "$0")"

echo "✅ 任务完成：第${STAGE_ID}阶段 - ${TASK_NAME}"
python3 -c "
import sys
sys.path.insert(0, '.')
from learning_bot import complete_task
complete_task($STAGE_ID, '$TASK_NAME')
"

echo "📝 进度已更新"
