import { useEffect, useState } from 'react'
import { getNetworkStats, getCacheStats } from '../services/api'
import StatCard from '../components/StatCard'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [cache, setCache] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getNetworkStats(), getCacheStats()])
      .then(([statsRes, cacheRes]) => {
        setStats(statsRes.data)
        setCache(cacheRes.data)
      })
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <p className="text-gray-400">Loading...</p>
    </div>
  )

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-500 mt-1">GraphLink network overview</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatCard
          label="Total Users"
          value={stats?.total_users?.toLocaleString()}
          sub="Stanford SNAP dataset"
        />
        <StatCard
          label="Total Friendships"
          value={stats?.total_friendships?.toLocaleString()}
          sub="Undirected edges"
        />
        <StatCard
          label="Cache Hit Rate"
          value={`${cache?.hit_rate_percent ?? 0}%`}
          sub={`${cache?.hits ?? 0} hits / ${cache?.misses ?? 0} misses`}
        />
        <StatCard
          label="Cached Users"
          value={cache?.cached_users ?? 0}
          sub={`Max size: ${cache?.max_size ?? 100}`}
        />
      </div>

      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <h3 className="font-semibold text-gray-900 mb-4">About GraphLink</h3>
        <div className="space-y-3 text-sm text-gray-600">
          <p>
            GraphLink is a friend recommendation engine that uses graph algorithms
            to suggest connections based on mutual friends and network proximity.
          </p>
          <p>
            The multi-signal V2 algorithm combines mutual friend scoring,
            Adamic-Adar weighting, and BFS-based network distance to rank candidates.
          </p>
          <div className="grid grid-cols-2 gap-4 mt-4 pt-4 border-t border-gray-100">
            <div>
              <p className="font-medium text-gray-700">V1 Precision@10</p>
              <p className="text-2xl font-bold text-gray-900">35.5%</p>
              <p className="text-xs text-gray-400">Mutual friends only</p>
            </div>
            <div>
              <p className="font-medium text-gray-700">V2 Precision@10</p>
              <p className="text-2xl font-bold text-blue-600">36.3%</p>
              <p className="text-xs text-gray-400">Multi-signal ranking</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}