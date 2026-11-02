import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getUser, getUserFriends, getRecommendations, getNetworkDegrees } from '../services/api'
import RecommendationCard from '../components/RecommendationCard'

export default function Profile() {
  const { userId } = useParams()
  const [user, setUser] = useState(null)
  const [friends, setFriends] = useState([])
  const [recommendations, setRecommendations] = useState([])
  const [recommendationSummary, setRecommendationSummary] = useState(null)
  const [degrees, setDegrees] = useState(null)
  const [algorithm, setAlgorithm] = useState('v2')
  const [loading, setLoading] = useState(true)
  const [recLoading, setRecLoading] = useState(false)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      getUser(userId),
      getUserFriends(userId),
      getNetworkDegrees(userId)
    ])
      .then(([userRes, friendsRes, degreesRes]) => {
        setUser(userRes.data)
        setFriends(friendsRes.data)
        setDegrees(degreesRes.data)
      })
      .finally(() => setLoading(false))
  }, [userId])

  useEffect(() => {
    if (!userId) return
    setRecLoading(true)
    getRecommendations(userId, 10, algorithm)
      .then(res => {
        setRecommendations(res.data.recommendations)
        setRecommendationSummary(res.data)
      })
      .finally(() => setRecLoading(false))
  }, [userId, algorithm])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <p className="text-gray-400">Loading profile...</p>
    </div>
  )

  if (!user) return (
    <div className="flex items-center justify-center h-64">
      <p className="text-gray-400">User not found.</p>
    </div>
  )

  return (
    <div>
      <div className="bg-white border border-slate-200 rounded-2xl p-6 mb-6 shadow-sm">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-full bg-blue-50 flex items-center justify-center text-blue-700 font-bold text-2xl">
            {user.name.charAt(0).toUpperCase()}
          </div>
          <div>
            <h2 className="text-2xl font-bold text-slate-950">{user.name}</h2>
            <p className="text-slate-400 text-sm">{user.email}</p>
            <div className="flex gap-4 mt-1 text-sm text-slate-500">
              {user.company && <span>🏢 {user.company}</span>}
              {user.location && <span>📍 {user.location}</span>}
              {user.education && <span>🎓 {user.education}</span>}
            </div>
          </div>
        </div>

        {degrees && (
          <div className="grid grid-cols-3 gap-4 mt-6 pt-6 border-t border-slate-100">
            <div className="text-center">
              <p className="text-2xl font-bold text-slate-950">{degrees.first_degree}</p>
              <p className="text-xs text-slate-400">1st degree</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-slate-950">{degrees.second_degree}</p>
              <p className="text-xs text-slate-400">2nd degree</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-slate-950">{degrees.third_degree}</p>
              <p className="text-xs text-slate-400">3rd degree</p>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div>
          <h3 className="font-semibold text-slate-900 mb-4">
            Friends ({friends.length})
          </h3>
          <div className="space-y-2">
            {friends.slice(0, 10).map(f => (
              <div
                key={f.id}
                className="flex items-center gap-3 bg-white border border-slate-200 rounded-xl px-4 py-3"
              >
                <div className="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-600 font-bold text-xs">
                  {f.name.charAt(0).toUpperCase()}
                </div>
                <p className="text-sm text-slate-700">{f.name}</p>
              </div>
            ))}
            {friends.length > 10 && (
              <p className="text-xs text-slate-400 px-2">
                +{friends.length - 10} more friends
              </p>
            )}
          </div>
        </div>

        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="font-semibold text-slate-900">Recommendations</h3>
              <p className="text-xs text-slate-500 mt-1">
                {recommendationSummary?.algorithm === 'v1'
                  ? 'Ranked by shared friends'
                  : 'Ranked by three graph signals'}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-400">Algorithm</span>
              <select
                value={algorithm}
                onChange={e => setAlgorithm(e.target.value)}
                className="text-sm border border-slate-200 rounded-lg px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="v2">V2 Multi-signal</option>
                <option value="v1">V1 Mutual friends</option>
              </select>
            </div>
          </div>

          {recLoading ? (
            <p className="text-slate-400 text-sm">Loading recommendations...</p>
          ) : recommendations.length === 0 ? (
            <p className="text-slate-400 text-sm">No recommendations found.</p>
          ) : (
            <div className="space-y-4">
              {recommendations.map(rec => (
                <RecommendationCard key={rec.user_id} rec={rec} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}