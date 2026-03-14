import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

const tests = {
  mbti: {
    name: 'MBTI 性格测试',
    questions: [
      { id: 1, text: '在社交聚会中，你通常？', options: [{ text: '主动与很多人交流', score: 'E' }, { text: '只与熟悉的人交流', score: 'I' }] },
      { id: 2, text: '你更倾向于？', options: [{ text: '成为关注的焦点', score: 'E' }, { text: '保持低调', score: 'I' }] },
      { id: 3, text: '经过一周工作，你更喜欢？', options: [{ text: '和朋友出去', score: 'E' }, { text: '在家安静休息', score: 'I' }] },
      { id: 4, text: '你更相信？', options: [{ text: '经验和事实', score: 'S' }, { text: '直觉和灵感', score: 'N' }] },
      { id: 5, text: '学习新知识时，你更喜欢？', options: [{ text: '具体例子', score: 'S' }, { text: '理论框架', score: 'N' }] },
      { id: 6, text: '你更擅长？', options: [{ text: '记住细节', score: 'S' }, { text: '理解概念', score: 'N' }] },
      { id: 7, text: '做决定时，你更看重？', options: [{ text: '逻辑分析', score: 'T' }, { text: '他人感受', score: 'F' }] },
      { id: 8, text: '朋友犯错时，你倾向于？', options: [{ text: '直接指出', score: 'T' }, { text: '考虑感受', score: 'F' }] },
      { id: 9, text: '你的工作风格？', options: [{ text: '按计划执行', score: 'J' }, { text: '灵活调整', score: 'P' }] },
      { id: 10, text: '对于截止日期，你通常？', options: [{ text: '提前完成', score: 'J' }, { text: '最后一刻', score: 'P' }] },
      { id: 11, text: '你更喜欢？', options: [{ text: '明确的结果', score: 'J' }, { text: '保持开放', score: 'P' }] },
      { id: 12, text: '认识新朋友时，你？', options: [{ text: '主动介绍', score: 'E' }, { text: '等别人介绍', score: 'I' }] },
    ],
  },
  'big-five': { name: '大五人格测试', questions: Array(20).fill({ text: '示例题目', options: [{ text: '非常不同意', score: 1 }, { text: '不同意', score: 2 }, { text: '中立', score: 3 }, { text: '同意', score: 4 }, { text: '非常同意', score: 5 }] }) },
  holland: { name: '霍兰德职业测试', questions: Array(12).fill({ text: '示例题目', options: [{ text: '喜欢', score: 1 }, { text: '不喜欢', score: 0 }] }) },
  disc: { name: 'DISC 性格测试', questions: Array(12).fill({ text: '示例题目', options: [{ text: '非常符合', score: 4 }, { text: '符合', score: 3 }, { text: '一般', score: 2 }, { text: '不符合', score: 1 }] }) },
  attachment: { name: '依恋类型测试', questions: Array(12).fill({ text: '示例题目', options: [{ text: '非常符合', score: 5 }, { text: '符合', score: 4 }, { text: '一般', score: 3 }, { text: '不符合', score: 2 }, { text: '非常不符合', score: 1 }] }) },
}

export default function Test() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const [current, setCurrent] = useState(0)
  const [answers, setAnswers] = useState([])

  const test = tests[testId] || tests.mbti
  const question = test.questions[current]
  const progress = ((current + 1) / test.questions.length) * 100

  const handleAnswer = (option) => {
    const newAnswers = [...answers, option]
    if (current < test.questions.length - 1) {
      setAnswers(newAnswers)
      setCurrent(current + 1)
    } else {
      // 完成测试，跳转到结果页
      navigate(`/result/${testId}`, { state: { answers: newAnswers } })
    }
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-2xl">
      {/* Progress */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>进度</span>
          <span>{current + 1} / {test.questions.length}</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div className="bg-purple-600 h-2 rounded-full transition-all" style={{ width: `${progress}%` }}></div>
        </div>
      </div>

      {/* Question */}
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">{question.text}</h2>
        <div className="space-y-4">
          {question.options.map((option, idx) => (
            <button
              key={idx}
              onClick={() => handleAnswer(option)}
              className="w-full p-4 text-left border-2 border-gray-200 rounded-lg hover:border-purple-600 hover:bg-purple-50 transition-colors"
            >
              {option.text}
            </button>
          ))}
        </div>
      </div>

      {/* Tips */}
      <p className="text-center text-gray-500 text-sm mt-8">
        💡 提示：凭直觉选择，没有对错之分
      </p>
    </div>
  )
}
