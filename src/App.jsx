import { Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import Test from './pages/Test'
import Result from './pages/Result'
import Pay from './pages/Pay'

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 to-blue-50">
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/test/:testId" element={<Test />} />
        <Route path="/result/:testId" element={<Result />} />
        <Route path="/pay/:testId" element={<Pay />} />
      </Routes>
    </div>
  )
}

export default App
