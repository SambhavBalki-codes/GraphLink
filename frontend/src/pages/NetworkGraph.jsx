import { useEffect, useState, useRef, useCallback } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { getUsers, getUserFriends } from '../services/api'

export default function NetworkGraph() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] })
  const [loading, setLoading] = useState(true)
  const [selectedNode, setSelectedNode] = useState(null)
  const [userCount, setUserCount] = useState(50)
  const [graphWidth, setGraphWidth] = useState(0)
  const graphRef = useRef()
  const graphContainerRef = useRef()

  const loadGraph = useCallback(async () => {
    setLoading(true)
    try {
      const usersRes = await getUsers(0, userCount)
      const users = usersRes.data

      const nodes = users.map(u => ({
        id: u.id,
        name: u.name,
        email: u.email
      }))

      const nodeIds = new Set(nodes.map(n => n.id))
      const links = []
      const seen = new Set()

      await Promise.all(
        users.slice(0, 30).map(async (user) => {
          try {
            const friendsRes = await getUserFriends(user.id)
            friendsRes.data.forEach(friend => {
              if (nodeIds.has(friend.id)) {
                const key = `${Math.min(user.id, friend.id)}-${Math.max(user.id, friend.id)}`
                if (!seen.has(key)) {
                  seen.add(key)
                  links.push({ source: user.id, target: friend.id })
                }
              }
            })
          } catch (error) {
            console.warn(`Could not load friends for user ${user.id}`, error)
          }
        })
      )

      setGraphData({ nodes, links })
    } finally {
      setLoading(false)
    }
  }, [userCount])

  useEffect(() => {
    loadGraph()
  }, [loadGraph])

  useEffect(() => {
    const container = graphContainerRef.current
    if (!container) return

    const observer = new ResizeObserver(([entry]) => {
      setGraphWidth(entry.contentRect.width)
    })
    observer.observe(container)
    return () => observer.disconnect()
  }, [])

  return (
    <div>
      <div className="mb-8">
        <p className="text-sm font-medium text-blue-700 mb-2">Visual explorer</p>
        <h2 className="text-3xl font-bold tracking-tight text-slate-950">Network Graph</h2>
        <p className="text-slate-500 mt-1">Explore connections across a focused sample of the friendship network.</p>
      </div>

      <div className="bg-white border border-slate-200 rounded-2xl p-4 mb-4 shadow-sm flex flex-wrap items-center gap-4">
        <label className="text-sm font-medium text-slate-700">Users to display</label>
        <select
          value={userCount}
          onChange={e => setUserCount(Number(e.target.value))}
          className="text-sm border border-slate-200 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500/30 focus:border-blue-400"
        >
          <option value={30}>30 users</option>
          <option value={50}>50 users</option>
          <option value={100}>100 users</option>
        </select>

        <span className="text-xs text-slate-400">Click a node to inspect it</span>
      </div>

      <div ref={graphContainerRef} className="bg-white border border-slate-200 rounded-2xl overflow-hidden shadow-sm">
        {loading ? (
          <div className="flex items-center justify-center h-[28rem]">
            <div className="text-center">
              <div className="w-8 h-8 border-2 border-blue-200 border-t-blue-600 rounded-full animate-spin mx-auto mb-3" />
              <p className="text-slate-500 text-sm">Building network graph...</p>
            </div>
          </div>
        ) : (
          <ForceGraph2D
            ref={graphRef}
            graphData={graphData}
            width={graphWidth || 700}
            height={500}
            nodeLabel={node => `${node.name} (ID: ${node.id})`}
            nodeColor={() => '#2563eb'}
            nodeRelSize={4}
            linkColor={() => '#cbd5e1'}
            linkWidth={0.8}
            onNodeClick={node => setSelectedNode(node)}
            backgroundColor="#ffffff"
            nodeCanvasObject={(node, ctx, globalScale) => {
              const label = node.name
              const fontSize = 9 / globalScale
              ctx.font = `${fontSize}px Sans-Serif`
              ctx.fillStyle = '#2563eb'
              ctx.beginPath()
              ctx.arc(node.x, node.y, 4, 0, 2 * Math.PI)
              ctx.fill()
              if (globalScale > 1.5) {
                ctx.fillStyle = '#334155'
                ctx.textAlign = 'center'
                ctx.fillText(label, node.x, node.y + 8)
              }
            }}
          />
        )}
      </div>

      {selectedNode && (
        <div className="mt-4 bg-blue-50 border border-blue-100 rounded-xl px-4 py-3 flex items-center justify-between gap-4">
          <div>
            <p className="text-sm font-semibold text-slate-900">{selectedNode.name}</p>
            <p className="text-xs text-slate-500">User ID: {selectedNode.id} · {selectedNode.email}</p>
          </div>
          <button onClick={() => setSelectedNode(null)} className="text-xs font-medium text-blue-700 hover:text-blue-900">
            Clear
          </button>
        </div>
      )}

      <div className="mt-4 text-sm text-slate-400">
        {graphData.nodes.length} nodes · {graphData.links.length} edges
      </div>
    </div>
  )
}