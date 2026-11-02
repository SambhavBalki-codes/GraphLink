import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Dashboard from './pages/Dashboard'
import Users from './pages/Users'
import Profile from './pages/Profile'
import PathFinder from './pages/PathFinder'
import NetworkGraph from './pages/NetworkGraph'

export default function App() {
  return (
    <BrowserRouter>
      <div className="flex min-h-screen bg-gray-50">
        <Sidebar />
        <main className="flex-1 p-8 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/users" element={<Users />} />
            <Route path="/users/:userId" element={<Profile />} />
            <Route path="/path" element={<PathFinder />} />
            <Route path="/graph" element={<NetworkGraph />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}