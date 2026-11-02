import { useEffect, useState } from 'react'
import { getUsers } from '../services/api'
import UserCard from '../components/UserCard'

export default function Users() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [skip, setSkip] = useState(0)
  const limit = 20

  useEffect(() => {
    setLoading(true)
    getUsers(skip, limit)
      .then(res => setUsers(res.data))
      .finally(() => setLoading(false))
  }, [skip])

  const filtered = users.filter(u =>
    u.name.toLowerCase().includes(search.toLowerCase()) ||
    u.email.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm font-medium text-blue-700 mb-2">Directory</p>
        <h2 className="text-3xl font-bold tracking-tight text-slate-950">Users</h2>
        <p className="text-slate-500 mt-1">Browse people in the friendship network.</p>
      </div>

      <div className="mb-6">
        <input
          type="text"
          placeholder="Search by name or email..."
          value={search}
          onChange={e => setSearch(e.target.value)}
          className="w-full max-w-md bg-white border border-slate-200 rounded-xl px-4 py-3 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
        />
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <p className="text-gray-400">Loading users...</p>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {filtered.map(user => (
              <UserCard key={user.id} user={user} />
            ))}
          </div>

          <div className="flex gap-3">
            <button
              onClick={() => setSkip(Math.max(0, skip - limit))}
              disabled={skip === 0}
              className="px-4 py-2 text-sm border border-slate-200 bg-white rounded-lg disabled:opacity-40 hover:bg-slate-50"
            >
              Previous
            </button>
            <button
              onClick={() => setSkip(skip + limit)}
              disabled={users.length < limit}
              className="px-4 py-2 text-sm border border-slate-200 bg-white rounded-lg disabled:opacity-40 hover:bg-slate-50"
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  )
}