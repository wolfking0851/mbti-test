import { Link } from 'react-router-dom'

const tests = [
  { id: 'mbti', name: 'MBTI 性格测试', desc: '16 型人格，发现你的真实性格', price: '9.9', popular: true },
  { id: 'big-five', name: '大五人格测试', desc: '心理学界公认的人格理论', price: '19.9' },
  { id: 'holland', name: '霍兰德职业测试', desc: '找到适合你的职业方向', price: '9.9' },
  { id: 'disc', name: 'DISC 性格测试', desc: '了解你的行为风格', price: '9.9' },
  { id: 'attachment', name: '依恋类型测试', desc: '探索你的亲密关系模式', price: '9.9' },
]

export default function Home() {
  return (
    <div className="container mx-auto px-4 py-8">
      {/* Header */}
      <header className="text-center mb-12">
        <h1 className="text-4xl font-bold text-purple-600 mb-4">🧠 心理测试馆</h1>
        <p className="text-gray-600 text-lg">AI 深度解读，发现真实的自己</p>
      </header>

      {/* Test List */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
        {tests.map((test) => (
          <Link
            key={test.id}
            to={`/test/${test.id}`}
            className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow relative"
          >
            {test.popular && (
              <span className="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded text-xs">
                🔥 热门
              </span>
            )}
            <h3 className="text-xl font-bold text-gray-800 mb-2">{test.name}</h3>
            <p className="text-gray-600 mb-4">{test.desc}</p>
            <div className="flex items-center justify-between">
              <span className="text-purple-600 font-bold text-lg">¥{test.price}</span>
              <span className="text-purple-600 font-medium">开始测试 →</span>
            </div>
          </Link>
        ))}
      </div>

      {/* Features */}
      <div className="mt-16 max-w-4xl mx-auto">
        <h2 className="text-2xl font-bold text-center text-gray-800 mb-8">为什么选择我们？</h2>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center">
            <div className="text-4xl mb-4">🎯</div>
            <h3 className="font-bold text-gray-800 mb-2">专业理论</h3>
            <p className="text-gray-600">基于 MBTI、大五人格等经典心理学理论</p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-4">🤖</div>
            <h3 className="font-bold text-gray-800 mb-2">AI 深度解读</h3>
            <p className="text-gray-600">千人千面，不是标准答案</p>
          </div>
          <div className="text-center">
            <div className="text-4xl mb-4">📊</div>
            <h3 className="font-bold text-gray-800 mb-2">详细报告</h3>
            <p className="text-gray-600">2000 字 + 深度解读，可下载 PDF</p>
          </div>
        </div>
      </div>

      {/* Disclaimer */}
      <footer className="mt-16 text-center text-gray-500 text-sm">
        <p>⚠️ 温馨提示：本测试基于心理学理论，由 AI 生成解读，仅供娱乐和自我探索参考</p>
        <p className="mt-2">不构成专业心理诊断，如有心理困扰请咨询专业心理咨询师</p>
      </footer>
    </div>
  )
}
