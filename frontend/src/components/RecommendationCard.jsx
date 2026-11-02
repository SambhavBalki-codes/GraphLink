import { ChevronDown, ChevronUp, GitBranch, Users, Zap } from 'lucide-react'
import { useState } from 'react'

export default function RecommendationCard({ rec }) {
  const [expanded, setExpanded] = useState(false)
  const signals = rec.signals || {}
  const components = [
    { key: 'mutual_component', label: 'Mutual friends', value: signals.mutual_component, icon: Users },
    { key: 'adamic_adar_component', label: 'Adamic-Adar', value: signals.adamic_adar_component, icon: Zap },
    { key: 'distance_component', label: 'Network distance', value: signals.distance_component, icon: GitBranch },
  ].filter(item => typeof item.value === 'number')
  const isBaseline = typeof signals.mutual_count === 'number'

  return (
    <div className="bg-white border border-slate-200 rounded-2xl p-5 hover:shadow-md transition-all">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-blue-700 font-bold text-sm">
            {rec.name.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="font-semibold text-slate-900 text-sm">{rec.name}</p>
            <p className="text-slate-400 text-xs">{rec.reason}</p>
          </div>
        </div>
        <div className="text-right">
          <span className="bg-blue-50 text-blue-700 text-xs font-medium px-2 py-1 rounded-full">
            Score: {typeof rec.score === 'number' ? rec.score.toFixed(2) : '—'}
          </span>
        </div>
      </div>

      <div className="mt-4">
        <p className="text-xs text-slate-500 font-medium mb-2">Mutual Friends</p>
        <div className="flex flex-wrap gap-2">
          {rec.mutual_friends.map((mf) => (
            <span
              key={mf.user_id}
              className="bg-slate-100 text-slate-600 text-xs px-2 py-1 rounded-full"
            >
              {mf.name}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-slate-100">
        <div className="flex items-center justify-between gap-3">
          <p className="text-xs text-slate-400">
            🔗 {rec.distance ?? '—'} degree connection
          </p>
          {(components.length > 0 || isBaseline) && (
            <button
              onClick={() => setExpanded(value => !value)}
              className="inline-flex items-center gap-1 text-xs font-medium text-blue-700 hover:text-blue-900"
            >
              Why this match?
              {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
            </button>
          )}
        </div>
      </div>

      {expanded && (
        <div className="mt-4 pt-4 border-t border-slate-100">
          <div className="flex items-center justify-between mb-3">
            <div>
              <p className="text-sm font-semibold text-slate-900">Score breakdown</p>
              <p className="text-xs text-slate-500">
                {isBaseline
                  ? 'Ranked by the number of shared friends.'
                  : 'Signals combined into the final recommendation score.'}
              </p>
            </div>
            <span className="text-sm font-semibold text-blue-700">{rec.score?.toFixed(4)}</span>
          </div>
          {isBaseline && (
            <div className="flex items-center justify-between rounded-xl bg-slate-50 px-3 py-2 text-sm">
              <span className="text-slate-600">Shared friends</span>
              <span className="font-semibold text-slate-900">{signals.mutual_count}</span>
            </div>
          )}
          <div className="space-y-3">
            {components.map(({ key, label, value, icon: Icon }) => (
              <div key={key}>
                <div className="flex items-center justify-between text-xs mb-1">
                  <span className="flex items-center gap-1.5 text-slate-600">
                    <Icon size={13} className="text-blue-600" />
                    {label}
                  </span>
                  <span className="font-medium text-slate-700">{value.toFixed(4)}</span>
                </div>
                <div className="h-1.5 rounded-full bg-slate-100 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-blue-600 transition-all"
                    style={{ width: `${Math.min(value * 100, 100)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
          {typeof signals.adamic_adar === 'number' && (
            <p className="text-xs text-slate-400 mt-3">
              Adamic-Adar raw signal: {signals.adamic_adar.toFixed(4)}
            </p>
          )}
        </div>
      )}
    </div>
  )
}