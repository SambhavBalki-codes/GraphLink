import { NavLink, useNavigate } from 'react-router-dom'
import { ArrowLeft, BarChart3, GitBranch, Network, Users } from 'lucide-react'

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: BarChart3 },
  { to: '/users', label: 'Users', icon: Users },
  { to: '/path', label: 'Path Finder', icon: GitBranch },
  { to: '/graph', label: 'Network Graph', icon: Network },
]

export default function Sidebar() {
  const navigate = useNavigate()

  return (
    <aside className="w-64 min-h-screen bg-white border-r border-slate-200 text-slate-900 flex flex-col">
      <div className="px-6 py-6 border-b border-slate-100">
        <button onClick={() => navigate('/')} className="flex items-center gap-2 text-left group">
          <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center shadow-sm">
            <Network size={16} className="text-white" />
          </div>
          <div>
            <h1 className="text-lg font-bold text-slate-950">GraphLink</h1>
            <p className="text-slate-500 text-xs mt-0.5">Friend network explorer</p>
          </div>
        </button>
        <button
          onClick={() => navigate('/')}
          className="mt-5 flex items-center gap-2 text-xs font-medium text-slate-500 hover:text-blue-700 transition-colors"
        >
          <ArrowLeft size={14} />
          Back to landing page
        </button>
      </div>

      <nav className="flex-1 px-4 py-6 space-y-1">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-slate-600 hover:bg-slate-50 hover:text-slate-950'
              }`
            }
          >
            <link.icon size={17} />
            <span>{link.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="px-6 py-5 border-t border-slate-100">
        <p className="text-slate-500 text-xs">Stanford SNAP Dataset</p>
        <p className="text-slate-400 text-xs mt-1">4,039 users · 88,234 friendships</p>
      </div>
    </aside>
  )
}