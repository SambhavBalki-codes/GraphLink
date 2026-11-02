import { useNavigate } from 'react-router-dom'

export default function UserCard({ user }) {
  const navigate = useNavigate()

  return (
    <div
      onClick={() => navigate(`/users/${user.id}`)}
      className="bg-white border border-slate-200 rounded-2xl p-5 cursor-pointer hover:shadow-md hover:border-blue-300 transition-all"
    >
      <div className="flex items-center gap-3">
        <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-700 font-bold text-sm">
          {user.name.charAt(0).toUpperCase()}
        </div>
        <div>
          <p className="font-semibold text-slate-900 text-sm">{user.name}</p>
          <p className="text-slate-400 text-xs">{user.email}</p>
        </div>
      </div>
      {(user.company || user.location) && (
        <div className="mt-3 flex gap-3 text-xs text-slate-500">
          {user.company && <span>🏢 {user.company}</span>}
          {user.location && <span>📍 {user.location}</span>}
        </div>
      )}
    </div>
  )
}