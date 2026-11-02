import { useNavigate } from 'react-router-dom'
import {
  GitBranch, Database, BarChart3,
  ArrowRight, Network, Search, ChevronRight, ExternalLink
} from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

function useCountUp(target, duration = 2000, start = false) {
  const [count, setCount] = useState(0)
  useEffect(() => {
    if (!start) return
    let startTime = null
    const step = (timestamp) => {
      if (!startTime) startTime = timestamp
      const progress = Math.min((timestamp - startTime) / duration, 1)
      setCount(Math.floor(progress * target))
      if (progress < 1) requestAnimationFrame(step)
    }
    requestAnimationFrame(step)
  }, [target, duration, start])
  return count
}

function StatCounter({ value, label, sub, start }) {
  const count = useCountUp(value, 1800, start)
  return (
    <div className="text-center">
      <p className="text-4xl font-bold text-slate-900 tabular-nums">
        {count.toLocaleString()}{typeof value === 'number' && value < 100 ? '%' : ''}
      </p>
      <p className="text-slate-700 text-sm font-medium mt-1">{label}</p>
      <p className="text-slate-500 text-xs mt-0.5">{sub}</p>
    </div>
  )
}

export default function Landing() {
  const navigate = useNavigate()
  const statsRef = useRef(null)
  const [statsVisible, setStatsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setStatsVisible(true) },
      { threshold: 0.3 }
    )
    if (statsRef.current) observer.observe(statsRef.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 overflow-x-hidden">

      {/* NAV */}
      <nav className="fixed top-0 left-0 right-0 z-50 border-b border-slate-200/80 bg-white/90 backdrop-blur-md">
        <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 bg-blue-600 rounded-lg flex items-center justify-center shadow-sm">
              <Network size={14} className="text-white" />
            </div>
            <span className="font-semibold text-slate-900 text-sm">GraphLink</span>
          </div>
          <div className="flex items-center gap-3">
            <a
              href="https://github.com/SambhavBalki-codes/GraphLink"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 text-slate-600 hover:text-slate-900 text-sm transition-colors"
            >
              <ExternalLink size={16} />
              <span>GitHub</span>
            </a>
            <button
              onClick={() => navigate('/dashboard')}
              className="bg-blue-600 hover:bg-blue-700 text-white text-sm px-4 py-2 rounded-lg transition-colors shadow-sm"
            >
              Open App
            </button>
          </div>
        </div>
      </nav>

      {/* HERO */}
      <section className="relative min-h-[720px] flex items-center justify-center px-6 pt-16">
        <div
          className="absolute inset-0 opacity-70"
          style={{
            backgroundImage: 'radial-gradient(circle at 50% 0%, #dbeafe 0%, transparent 55%)'
          }}
        />

        <div className="relative max-w-4xl mx-auto text-center">
          <div className="inline-flex items-center gap-2 border border-blue-200 bg-blue-50 text-blue-700 text-xs px-3 py-1.5 rounded-full mb-8">
            <div className="w-1.5 h-1.5 bg-blue-600 rounded-full" />
            Validated on Stanford SNAP Facebook Dataset
          </div>

          <h1 className="text-5xl md:text-7xl font-bold leading-[1.1] tracking-tight text-slate-950 mb-6">
            Friend recommendations
            <br />
            <span className="text-blue-700">
              powered by graphs
            </span>
          </h1>

          <p className="text-slate-600 text-xl leading-relaxed max-w-2xl mx-auto mb-10">
            GraphLink analyzes social networks using graph traversal algorithms
            to surface meaningful connections — the same idea behind LinkedIn's
            People You May Know.
          </p>

          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="group flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-all shadow-sm"
            >
              Explore the network
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <a
              href="https://github.com/SambhavBalki-codes/GraphLink"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 border border-slate-300 hover:border-slate-400 bg-white text-slate-700 hover:text-slate-950 px-6 py-3 rounded-lg font-medium transition-all shadow-sm"
            >
              <ExternalLink size={16} />
              Source code
            </a>
          </div>
        </div>
      </section>

      {/* STATS */}
      <section ref={statsRef} className="border-y border-slate-200 bg-white py-16 px-6">
        <div className="max-w-4xl mx-auto grid grid-cols-2 md:grid-cols-4 gap-8">
          <StatCounter value={4039} label="Real users" sub="Stanford SNAP" start={statsVisible} />
          <StatCounter value={88234} label="Friendships" sub="Undirected edges" start={statsVisible} />
          <StatCounter value={36} label="Precision@10" sub="V2 multi-signal" start={statsVisible} />
          <StatCounter value={30} label="Tests passing" sub="Unit + integration" start={statsVisible} />
        </div>
      </section>

      {/* HOW IT WORKS */}
      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="mb-16">
            <p className="text-blue-700 text-sm font-medium mb-3">How it works</p>
            <h2 className="text-4xl font-bold text-slate-950">From data to recommendations</h2>
            <p className="text-slate-600 mt-3 max-w-xl">
              Three stages transform raw friendship records into ranked, explainable suggestions.
            </p>
          </div>

          <div className="space-y-4">
            {[
              {
                step: '01',
                title: 'Graph Construction',
                description: 'Friendship records from PostgreSQL are loaded and transformed into an in-memory adjacency list. Each user maps to a set of their neighbors. A friendship between users A and B is stored once as (min(A,B), max(A,B)) — enforced by a database CHECK constraint.',
                code: 'adjacency[alice] = {bob, charlie}\nadjacency[bob]   = {alice, david}\nadjacency[david] = {bob, charlie}',
                icon: Database,
                color: 'blue'
              },
              {
                step: '02',
                title: 'Candidate Discovery',
                description: 'For each direct friend of the target user, we traverse their neighbors. Any user who is not the target and not already a direct friend becomes a candidate. We track which mutual friends connect each candidate to the target.',
                code: 'for friend in neighbors(target):\n  for candidate in neighbors(friend):\n    if candidate ≠ target and candidate ∉ direct_friends:\n      mutual_map[candidate].add(friend)',
                icon: Search,
                color: 'violet'
              },
              {
                step: '03',
                title: 'Multi-Signal Scoring',
                description: 'Each candidate receives a composite score from three graph-based signals. Candidates are sorted descending by score, with user ID as a deterministic tiebreaker. The top K results are returned with full explanations.',
                code: 'score = 0.40 × mutual_ratio\n      + 0.40 × adamic_adar\n      + 0.20 × (1 / bfs_distance)',
                icon: BarChart3,
                color: 'emerald'
              },
            ].map((item, i) => (
              <div
                key={i}
                className="group grid grid-cols-1 md:grid-cols-2 gap-6 bg-white hover:bg-slate-50 border border-slate-200 rounded-2xl p-8 transition-all shadow-sm"
              >
                <div>
                  <div className="flex items-center gap-3 mb-4">
                    <span className="text-slate-400 text-sm font-mono">{item.step}</span>
                    <div className={`w-8 h-8 rounded-lg flex items-center justify-center
                      ${item.color === 'blue' ? 'bg-blue-50' : ''}
                      ${item.color === 'violet' ? 'bg-slate-100' : ''}
                      ${item.color === 'emerald' ? 'bg-slate-100' : ''}
                    `}>
                      <item.icon size={16} className={`
                        ${item.color === 'blue' ? 'text-blue-700' : ''}
                        ${item.color === 'violet' ? 'text-slate-700' : ''}
                        ${item.color === 'emerald' ? 'text-slate-700' : ''}
                      `} />
                    </div>
                    <h3 className="font-semibold text-slate-900">{item.title}</h3>
                  </div>
                  <p className="text-slate-600 text-sm leading-relaxed">{item.description}</p>
                </div>
                <div className="bg-slate-50 rounded-xl p-4 border border-slate-200">
                  <pre className="text-xs text-slate-700 font-mono leading-relaxed whitespace-pre-wrap">
                    {item.code}
                  </pre>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ALGORITHMS */}
      <section className="py-24 px-6 bg-white border-y border-slate-200">
        <div className="max-w-5xl mx-auto">
          <div className="mb-16">
            <p className="text-blue-700 text-sm font-medium mb-3">Algorithms</p>
            <h2 className="text-4xl font-bold text-slate-950">Two scoring strategies</h2>
            <p className="text-slate-600 mt-3 max-w-xl">
              Both evaluated using Precision@K with edge-removal methodology on 100 sampled users from the Stanford dataset.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
            <div className="bg-slate-50 border border-slate-200 rounded-2xl p-7 shadow-sm">
              <div className="flex items-center justify-between mb-5">
                <span className="text-xs font-medium bg-slate-200 text-slate-700 px-2.5 py-1 rounded-full">V1 — Baseline</span>
                <span className="text-2xl font-bold text-slate-700">35.5%</span>
              </div>
              <h3 className="font-semibold text-slate-900 text-lg mb-2">Mutual Friend Count</h3>
              <p className="text-slate-600 text-sm mb-5 leading-relaxed">
                Ranks candidates purely by the number of shared friends. Fast and interpretable, but treats all mutual friends as equally valuable regardless of their network position.
              </p>
              <div className="bg-white rounded-lg p-4 border border-slate-200">
                <p className="text-xs text-slate-500 mb-2 font-mono">formula</p>
                <p className="text-sm font-mono text-slate-700">
                  score(u, v) = |N(u) ∩ N(v)|
                </p>
                <p className="text-xs text-slate-500 mt-2">
                  where N(x) = set of neighbors of x
                </p>
              </div>
            </div>

            <div className="bg-blue-50/60 border border-blue-200 rounded-2xl p-7 relative overflow-hidden shadow-sm">
              <div className="absolute top-4 right-4 text-xs font-medium bg-blue-100 text-blue-700 px-2.5 py-1 rounded-full">
                Active
              </div>
              <div className="flex items-center justify-between mb-5">
                <span className="text-xs font-medium bg-blue-100 text-blue-700 px-2.5 py-1 rounded-full">V2 — Multi-signal</span>
                <span className="text-2xl font-bold text-blue-700">36.3%</span>
              </div>
              <h3 className="font-semibold text-slate-900 text-lg mb-2">Weighted Graph Signals</h3>
              <p className="text-slate-600 text-sm mb-5 leading-relaxed">
                Combines three graph-derived signals. Adamic-Adar penalizes high-degree mutual friends — a shared contact with 500 connections is less meaningful than one with 5.
              </p>
              <div className="bg-white rounded-lg p-4 border border-blue-100 space-y-2">
                <p className="text-xs text-slate-500 mb-3 font-mono">composite score</p>
                <div className="flex items-center gap-2">
                  <span className="text-blue-700 font-mono text-sm font-bold">0.40</span>
                  <span className="text-slate-500 text-xs">×</span>
                  <span className="text-slate-700 text-sm font-mono">mutual_ratio</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-blue-700 font-mono text-sm font-bold">0.40</span>
                  <span className="text-slate-500 text-xs">×</span>
                  <span className="text-slate-700 text-sm font-mono">Σ 1/log(deg(w))</span>
                  <span className="text-slate-600 text-xs">adamic-adar</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-blue-700 font-mono text-sm font-bold">0.20</span>
                  <span className="text-slate-500 text-xs">×</span>
                  <span className="text-slate-700 text-sm font-mono">1 / bfs_distance</span>
                </div>
              </div>
            </div>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-7 shadow-sm">
            <div className="flex items-start gap-4 mb-6">
              <div className="w-9 h-9 bg-blue-50 rounded-lg flex items-center justify-center shrink-0">
                <GitBranch size={16} className="text-blue-700" />
              </div>
              <div>
                <h3 className="font-semibold text-slate-900 mb-1">BFS Path Reconstruction</h3>
                <p className="text-slate-600 text-sm leading-relaxed">
                  Beyond scoring, GraphLink uses Breadth-First Search to find the shortest connection path between any two users. The path is returned as an ordered list with a human-readable explanation — similar to LinkedIn's 2nd/3rd degree indicators.
                </p>
              </div>
            </div>
            <div className="bg-white rounded-xl p-5 border border-slate-200">
              <p className="text-xs text-slate-500 mb-4 font-mono">example response — GET /users/1/path/4</p>
              <div className="flex items-center gap-3 flex-wrap">
                {['Alice (1)', 'Bob (2)', 'David (4)'].map((name, i) => (
                  <div key={name} className="flex items-center gap-3">
                    <div className="bg-blue-50 border border-blue-200 text-blue-800 text-sm px-3 py-2 rounded-lg font-mono">
                      {name}
                    </div>
                    {i < 2 && <ChevronRight size={14} className="text-slate-400" />}
                  </div>
                ))}
                <span className="text-slate-500 text-sm ml-2">· 2 degrees of separation</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* TECH STACK */}
      <section className="py-24 px-6">
        <div className="max-w-5xl mx-auto">
          <div className="mb-16">
            <p className="text-blue-700 text-sm font-medium mb-3">Stack</p>
            <h2 className="text-4xl font-bold text-slate-950">Built with the right tools</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white border border-slate-200 rounded-2xl p-7 shadow-sm">
              <p className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-5">Backend</p>
              <div className="space-y-4">
                {[
                  { name: 'Python 3.12 + FastAPI', desc: 'REST API with automatic OpenAPI docs' },
                  { name: 'PostgreSQL 16', desc: 'Relational DB with CHECK constraints and foreign keys' },
                  { name: 'SQLAlchemy 2.x + Alembic', desc: 'ORM with tracked schema migrations' },
                  { name: 'Pytest', desc: '30 tests — unit + integration + API' },
                ].map(item => (
                  <div key={item.name} className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-2 shrink-0" />
                    <div>
                      <p className="text-slate-900 text-sm font-medium">{item.name}</p>
                      <p className="text-slate-500 text-xs mt-0.5">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white border border-slate-200 rounded-2xl p-7 shadow-sm">
              <p className="text-slate-400 text-xs font-medium uppercase tracking-wider mb-5">Frontend</p>
              <div className="space-y-4">
                {[
                  { name: 'React 18 + Vite', desc: 'Fast SPA with file-based routing' },
                  { name: 'Tailwind CSS', desc: 'Utility-first styling' },
                  { name: 'react-force-graph-2d', desc: 'Interactive network visualization' },
                  { name: 'Axios + React Router', desc: 'API layer and client-side routing' },
                ].map(item => (
                  <div key={item.name} className="flex items-start gap-3">
                    <div className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-2 shrink-0" />
                    <div>
                      <p className="text-slate-900 text-sm font-medium">{item.name}</p>
                      <p className="text-slate-500 text-xs mt-0.5">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-24 px-6 border-t border-slate-200 bg-white">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-slate-950 mb-4">
            See it in action
          </h2>
          <p className="text-slate-600 mb-8 leading-relaxed">
            Browse 4,039 real users from the Stanford Facebook dataset,
            find shortest connection paths, and explore multi-signal recommendations.
          </p>
          <div className="flex items-center justify-center gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="group flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition-all shadow-sm"
            >
              Open the app
              <ArrowRight size={16} className="group-hover:translate-x-1 transition-transform" />
            </button>
            <a
              href="https://github.com/SambhavBalki-codes/GraphLink"
              target="_blank"
              rel="noreferrer"
              className="flex items-center gap-2 border border-slate-300 hover:border-slate-400 bg-white text-slate-700 hover:text-slate-950 px-6 py-3 rounded-lg font-medium transition-all"
            >
              <ExternalLink size={16} />
              GitHub
            </a>
          </div>
        </div>
      </section>

      <footer className="border-t border-slate-200 px-6 py-6 bg-slate-50">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-5 h-5 bg-blue-600 rounded flex items-center justify-center">
              <Network size={10} className="text-white" />
            </div>
            <span className="text-slate-600 text-sm">GraphLink</span>
          </div>
          <p className="text-slate-500 text-xs">
            Built with FastAPI · PostgreSQL · React
          </p>
        </div>
      </footer>
    </div>
  )
}