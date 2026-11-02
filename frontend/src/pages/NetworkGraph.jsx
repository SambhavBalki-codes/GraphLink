import { useEffect, useState, useRef } from 'react'
import ForceGraph2D from 'react-force-graph-2d'
import { getUsers, getUserFriends } from '../services/api'

export default function NetworkGraph() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] })
  const [loading, setLoading] = useState(true)
  const [selectedNode, setSelectedNode] = useState(null)
  const [userCount, setUserCount] = useState(50)
  const graphRef = useRef()

  useEffect(() => {
    loadGraph()
  }, [userCount])

  const loadGraph = async () => {
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
          } catch (e) {}
        })
      )

      setGraphData({ nodes, links })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Network Graph</h2>
        <p className="text-gray-500 mt-1">Visual representation of the friendship network</p>
      </div>

      <div className="flex items-center gap-4 mb-4">
        <label className="text-sm font-medium text-gray-700">Users to display:</label>
        <select
          value={userCount}
          onChange={e => setUserCount(Number(e.target.value))}
          className="text-sm border border-gray-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value={30}>30 users</option>
          <option value={50}>50 users</option>
          <option value={100}>100 users</option>
        </select>

        {selectedNode && (
          <div className="ml-4 bg-blue-50 border border-blue-200 rounded-lg px-4 py-2 text-sm">
            <span className="text-blue-600 font-medium">{selectedNode.name}</span>
            <span className="text-blue-400 ml-2">ID: {selectedNode.id}</span>
          </div>
        )}
      </div>

      <div className="bg-white border border-gray-200 rounded-xl overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center h-96">
            <p className="text-gray-400">Building network graph...</p>
          </div>
        ) : (
          <ForceGraph2D
            ref={graphRef}
            graphData={graphData}
            width={900}
            height={500}
            nodeLabel={node => `${node.name} (ID: ${node.id})`}
            nodeColor={() => '#3b82f6'}
            nodeRelSize={5}
            linkColor={() => '#e5e7eb'}
            linkWidth={1}
            onNodeClick={node => setSelectedNode(node)}
            backgroundColor="#ffffff"
            nodeCanvasObject={(node, ctx, globalScale) => {
              const label = node.name
              const fontSize = 10 / globalScale
              ctx.font = `${fontSize}px Sans-Serif`
              ctx.fillStyle = '#3b82f6'
              ctx.beginPath()
              ctx.arc(node.x, node.y, 4, 0, 2 * Math.PI)
              ctx.fill()
              if (globalScale > 1.5) {
                ctx.fillStyle = '#374151'
                ctx.textAlign = 'center'
                ctx.fillText(label, node.x, node.y + 8)
              }
            }}
          />
        )}
      </div>

      <div className="mt-4 text-sm text-gray-400">
        {graphData.nodes.length} nodes · {graphData.links.length} edges · Click a node to select it
      </div>
    </div>
  )
}