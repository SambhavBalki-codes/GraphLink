import { NavLink } from 'react-router-dom'

const links = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/users', label: 'Users', icon: '👥' },
  { to: '/path', label: 'Path Finder', icon: '🔗' },
  { to: '/graph', label: 'Network Graph', icon: '🕸️' },
]

export default function Sidebar() {
  return (
    <aside className="w-64 min-h-screen bg-gray-900 text-white flex flex-col">
      <div className="px-6 py-8 border-b border-gray-700">
        <h1 className="text-xl font-bold text-white">GraphLink</h1>
        <p className="text-gray-400 text-sm mt-1">Friend Recommendations</p>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-1">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            end={link.to === '/'}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-400 hover:bg-gray-800 hover:text-white'
              }`
            }
          >
            <span>{link.icon}</span>
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-4 border-t border-gray-700">
        <p className="text-gray-500 text-xs">Stanford SNAP Dataset</p>
        <p className="text-gray-500 text-xs">4,039 users · 88,234 friendships</p>
      </div>
    </aside>
  )
}