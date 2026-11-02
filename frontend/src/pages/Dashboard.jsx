import { useEffect, useState } from 'react'
import { getNetworkStats, getCacheStats, getMetrics } from '../services/api'
import StatCard from '../components/StatCard'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [cache, setCache] = useState(null)
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([getNetworkStats(), getCacheStats(), getMetrics()])
      .then(([statsRes, cacheRes, metricsRes]) => {
        setStats(statsRes.data)
        setCache(cacheRes.data)
        setMetrics(metricsRes.data)
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
        <p className="text-sm font-medium text-blue-700 mb-2">Overview</p>
        <h2 className="text-3xl font-bold tracking-tight text-slate-950">Dashboard</h2>
        <p className="text-slate-500 mt-1">A quick look at the GraphLink friendship network.</p>
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
          label="Recommendation latency"
          value={`${metrics?.recommendations?.average_ms ?? 0} ms`}
          sub={`${metrics?.recommendations?.cache_hits ?? 0} cache hits`}
        />
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-6 mb-8 shadow-sm">
        <div className="flex items-start justify-between gap-4 mb-5">
          <div>
            <h3 className="font-semibold text-slate-950">System health</h3>
            <p className="text-sm text-slate-500 mt-1">Live cache and request performance.</p>
          </div>
          <span className="bg-emerald-50 text-emerald-700 text-xs font-medium px-2.5 py-1 rounded-full">
            Operational
          </span>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <p className="text-xs text-slate-400">Cache entries</p>
            <p className="text-xl font-semibold text-slate-900 mt-1">{cache?.cached_entries ?? 0}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400">Evictions</p>
            <p className="text-xl font-semibold text-slate-900 mt-1">{cache?.evictions ?? 0}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400">Graph build</p>
            <p className="text-xl font-semibold text-slate-900 mt-1">{cache?.graph_snapshot?.last_build_ms ?? 0} ms</p>
          </div>
          <div>
            <p className="text-xs text-slate-400">Recent API latency</p>
            <p className="text-xl font-semibold text-slate-900 mt-1">{metrics?.recent_average_ms ?? 0} ms</p>
          </div>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm">
        <h3 className="font-semibold text-slate-950 mb-4">About GraphLink</h3>
        <div className="space-y-3 text-sm text-slate-600">
          <p>
            GraphLink is a friend recommendation engine that uses graph algorithms
            to suggest connections based on mutual friends and network proximity.
          </p>
          <p>
            The multi-signal V2 algorithm combines mutual friend scoring,
            Adamic-Adar weighting, and BFS-based network distance to rank candidates.
          </p>
          <div className="grid grid-cols-2 gap-4 mt-5 pt-5 border-t border-slate-100">
            <div>
              <p className="font-medium text-slate-700">V1 Precision@10</p>
              <p className="text-2xl font-bold text-slate-950 mt-1">35.5%</p>
              <p className="text-xs text-slate-400">Mutual friends only</p>
            </div>
            <div>
              <p className="font-medium text-slate-700">V2 Precision@10</p>
              <p className="text-2xl font-bold text-blue-700 mt-1">36.3%</p>
              <p className="text-xs text-slate-400">Multi-signal ranking</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}