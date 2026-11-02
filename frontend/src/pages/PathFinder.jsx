import { useState } from 'react'
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
        <h2 className="text-2xl font-bold text-gray-900">Path Finder</h2>
        <p className="text-gray-500 mt-1">
          Find the shortest connection between two users
        </p>
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-6 mb-6 max-w-lg">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              User ID 1
            </label>
            <input
              type="number"
              value={userId1}
              onChange={e => setUserId1(e.target.value)}
              placeholder="e.g. 1"
              className="w-full border border-gray-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              User ID 2
            </label>
            <input
              type="number"
              value={userId2}
              onChange={e => setUserId2(e.target.value)}
              placeholder="e.g. 100"
              className="w-full border border-gray-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {error && <p className="text-red-500 text-sm">{error}</p>}

          <button
            onClick={handleFind}
            disabled={loading}
            className="w-full bg-blue-600 text-white py-2 rounded-lg text-sm font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
          >
            {loading ? 'Finding path...' : 'Find Connection'}
          </button>
        </div>
      </div>

      {result && (
        <div className="bg-white border border-gray-200 rounded-xl p-6 max-w-lg">
          {result.connected ? (
            <>
              <div className="flex items-center gap-2 mb-4">
                <span className="bg-green-100 text-green-700 text-xs font-medium px-2 py-1 rounded-full">
                  Connected
                </span>
                <span className="text-sm text-gray-500">
                  {result.degrees} degree{result.degrees !== 1 ? 's' : ''} of separation
                </span>
              </div>

              <div className="flex items-center gap-2 flex-wrap mb-4">
                {result.path.map((user, index) => (
                  <div key={user.user_id} className="flex items-center gap-2">
                    <div className="bg-blue-50 border border-blue-200 rounded-lg px-3 py-2 text-center">
                      <p className="text-xs text-blue-400">ID: {user.user_id}</p>
                      <p className="text-sm font-medium text-blue-700">{user.name}</p>
                    </div>
                    {index < result.path.length - 1 && (
                      <span className="text-gray-400">→</span>
                    )}
                  </div>
                ))}
              </div>

              <p className="text-sm text-gray-500 bg-gray-50 rounded-lg px-4 py-3">
                {result.explanation}
              </p>
            </>
          ) : (
            <div className="text-center py-4">
              <p className="text-gray-500">No connection found between these users.</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}