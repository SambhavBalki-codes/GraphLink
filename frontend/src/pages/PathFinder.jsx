import { useState } from 'react'
import { ArrowRight, GitBranch, Search } from 'lucide-react'
import { getConnectionPath } from '../services/api'

export default function PathFinder() {
  const [userId1, setUserId1] = useState('')
  const [userId2, setUserId2] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFind = () => {
    if (!userId1 || !userId2) {
      setError('Please enter both user IDs')
      return
    }
    setError('')
    setResult(null)
    setLoading(true)
    getConnectionPath(userId1, userId2)
      .then(res => setResult(res.data))
      .catch(() => setError('Could not find path. Check user IDs.'))
      .finally(() => setLoading(false))
  }

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm font-medium text-blue-700 mb-2">Explore connections</p>
        <h2 className="text-3xl font-bold tracking-tight text-slate-950">Path Finder</h2>
        <p className="text-slate-500 mt-1">
          Find the shortest connection between two users.
        </p>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-6 mb-6 max-w-3xl shadow-sm">
        <div className="flex items-center gap-3 mb-6">
          <div className="w-10 h-10 rounded-xl bg-blue-50 flex items-center justify-center">
            <GitBranch size={19} className="text-blue-700" />
          </div>
          <div>
            <h3 className="font-semibold text-slate-950">Find a connection</h3>
            <p className="text-sm text-slate-500">Enter two user IDs to trace their shortest path.</p>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-[1fr_auto_1fr] items-end gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Starting user
            </label>
            <input
              type="number"
              value={userId1}
              onChange={e => setUserId1(e.target.value)}
              placeholder="e.g. 1"
              className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
            />
          </div>
          <ArrowRight size={18} className="hidden md:block text-slate-300 mb-3" />
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Destination user
            </label>
            <input
              type="number"
              value={userId2}
              onChange={e => setUserId2(e.target.value)}
              placeholder="e.g. 100"
              className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
            />
          </div>
        </div>
        {error && <p className="mt-4 text-red-600 text-sm">{error}</p>}
        <button
          onClick={handleFind}
          disabled={loading}
          className="mt-5 inline-flex items-center justify-center gap-2 bg-blue-600 text-white px-5 py-3 rounded-xl text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors shadow-sm"
        >
          <Search size={16} />
          {loading ? 'Finding path...' : 'Find connection'}
        </button>
      </div>

      {result && (
        <div className="bg-white border border-slate-200 rounded-2xl p-6 max-w-3xl shadow-sm">
          {result.connected ? (
            <>
              <div className="flex items-center gap-2 mb-4">
                <span className="bg-emerald-50 text-emerald-700 text-xs font-medium px-2 py-1 rounded-full">
                  Connected
                </span>
                <span className="text-sm text-slate-500">
                  {result.degrees} degree{result.degrees !== 1 ? 's' : ''} of separation
                </span>
              </div>

              <div className="flex items-center gap-2 flex-wrap mb-5">
                {result.path.map((user, index) => (
                  <div key={user.user_id} className="flex items-center gap-2">
                    <div className="bg-slate-50 border border-slate-200 rounded-xl px-4 py-3 text-center">
                      <p className="text-xs text-slate-400">ID: {user.user_id}</p>
                      <p className="text-sm font-medium text-slate-800">{user.name}</p>
                    </div>
                    {index < result.path.length - 1 && (
                      <ArrowRight size={16} className="text-slate-300" />
                    )}
                  </div>
                ))}
              </div>

              <p className="text-sm text-slate-600 bg-slate-50 rounded-xl px-4 py-3">
                {result.explanation}
              </p>
            </>
          ) : (
            <div className="text-center py-4">
              <p className="text-slate-500">No connection found between these users.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}