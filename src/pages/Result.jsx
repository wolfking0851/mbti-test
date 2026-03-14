import { useNavigate, useParams, useLocation } from 'react-router-dom'

export default function Result() {
  const navigate = useNavigate()
  const { testId } = useParams()
  const location = useLocation()
  
  // 简化处理，实际应该根据答案计算类型
  const resultType = 'INTJ - 建筑师型'
  
  return (
    <div className="container mx-auto px-4 py-8 max-w-3xl">
      <div className="bg-white rounded-xl shadow-lg p-8">
        {/* Result Header */}
        <div className="text-center mb-8">
          <div className="text-6xl mb-4">🏗️</div>
          <h1 className="text-3xl font-bold text-purple-600 mb-2">{resultType}</h1>
          <p className="text-gray-600">你的性格类型是</p>
        </div>

        {/* Free Content */}
        <div className="prose max-w-none mb-8">
          <h2 className="text-xl font-bold text-gray-800 mb-4">🎯 核心特征</h2>
          <ul className="space-y-2 text-gray-700">
            <li>✅ 战略思维，长远规划</li>
            <li>✅ 独立自信，有主见</li>
            <li>✅ 追求效率和能力</li>
            <li>✅ 学习能力强</li>
          </ul>

          <h2 className="text-xl font-bold text-gray-800 mt-6 mb-4">✅ 你的优势</h2>
          <ul className="space-y-2 text-gray-700">
            <li>• 能看到长远趋势，制定有效计划</li>
            <li>• 快速掌握复杂概念和系统</li>
            <li>• 独立自主，能独立完成任务</li>
          </ul>
        </div>

        {/* Paywall */}
        <div className="bg-gradient-to-r from-purple-50 to-blue-50 rounded-xl p-6 text-center">
          <h3 className="text-xl font-bold text-gray-800 mb-4">🔓 解锁深度解读报告</h3>
          <ul className="text-left text-gray-700 space-y-2 mb-6">
            <li>✅ 详细性格分析（1000 字+）</li>
            <li>✅ 优势与盲点深度解析</li>
            <li>✅ 10 条专属发展建议</li>
            <li>✅ 适合职业匹配（10 个）</li>
            <li>✅ 亲密关系指南</li>
            <li>✅ 专属 PDF 报告下载</li>
          </ul>
          <button
            onClick={() => navigate(`/pay/${testId}`)}
            className="bg-purple-600 text-white px-8 py-3 rounded-lg font-bold text-lg hover:bg-purple-700 transition-colors"
          >
            立即解锁 ¥9.9
          </button>
          <p className="text-xs text-gray-500 mt-4">
            ⚠️ 本结果由 AI 生成，仅供娱乐参考，不构成专业心理诊断
          </p>
        </div>

        {/* Share */}
        <div className="mt-8 text-center">
          <button className="text-purple-600 font-medium hover:underline">
            分享结果到朋友圈
          </button>
        </div>
      </div>
    </div>
  )
}
