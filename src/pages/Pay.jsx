import { useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

export default function Pay() {
  const { testId } = useParams()
  const navigate = useNavigate()
  const [paid, setPaid] = useState(false)

  const handlePay = () => {
    // 简化处理，实际应该接入支付
    setPaid(true)
    setTimeout(() => {
      navigate(`/result/${testId}?paid=true`)
    }, 2000)
  }

  return (
    <div className="container mx-auto px-4 py-8 max-w-md">
      <div className="bg-white rounded-xl shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center text-gray-800 mb-6">
          {paid ? '🎉 支付成功' : '💳 确认支付'}
        </h1>

        {paid ? (
          <div className="text-center">
            <div className="text-6xl mb-4">✅</div>
            <p className="text-gray-700 mb-4">支付成功！正在生成报告...</p>
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600 mx-auto"></div>
          </div>
        ) : (
          <>
            {/* Order Info */}
            <div className="bg-gray-50 rounded-lg p-4 mb-6">
              <h3 className="font-bold text-gray-800 mb-2">订单详情</h3>
              <div className="space-y-2 text-sm text-gray-700">
                <div className="flex justify-between">
                  <span>商品</span>
                  <span>心理测试深度报告</span>
                </div>
                <div className="flex justify-between">
                  <span>原价</span>
                  <span className="line-through text-gray-400">¥19.9</span>
                </div>
                <div className="flex justify-between font-bold text-lg">
                  <span>实付</span>
                  <span className="text-purple-600">¥9.9</span>
                </div>
              </div>
            </div>

            {/* Payment Method */}
            <div className="mb-6">
              <h3 className="font-bold text-gray-800 mb-3">支付方式</h3>
              <div className="space-y-2">
                <label className="flex items-center p-3 border-2 border-purple-600 rounded-lg bg-purple-50">
                  <input type="radio" name="payment" className="mr-3" defaultChecked />
                  <span className="text-gray-800">微信支付</span>
                </label>
                <label className="flex items-center p-3 border-2 border-gray-200 rounded-lg">
                  <input type="radio" name="payment" className="mr-3" />
                  <span className="text-gray-800">支付宝</span>
                </label>
              </div>
            </div>

            {/* Pay Button */}
            <button
              onClick={handlePay}
              className="w-full bg-purple-600 text-white py-3 rounded-lg font-bold text-lg hover:bg-purple-700 transition-colors"
            >
              立即支付 ¥9.9
            </button>

            {/* Guarantee */}
            <div className="mt-6 text-center text-xs text-gray-500">
              <p>🔒 安全支付保障</p>
              <p className="mt-1">⚠️ 虚拟商品，一经生成不支持退款</p>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
