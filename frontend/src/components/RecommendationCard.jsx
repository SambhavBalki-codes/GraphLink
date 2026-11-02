export default function RecommendationCard({ rec }) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 hover:shadow-md transition-all">
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-green-100 flex items-center justify-center text-green-600 font-bold text-sm">
            {rec.name.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="font-semibold text-gray-900 text-sm">{rec.name}</p>
            <p className="text-gray-400 text-xs">{rec.reason}</p>
          </div>
        </div>
        <div className="text-right">
          <span className="bg-blue-50 text-blue-600 text-xs font-medium px-2 py-1 rounded-full">
            Score: {rec.score?.toFixed(2)}
          </span>
        </div>
      </div>

      <div className="mt-4">
        <p className="text-xs text-gray-500 font-medium mb-2">Mutual Friends</p>
        <div className="flex flex-wrap gap-2">
          {rec.mutual_friends.map((mf) => (
            <span
              key={mf.user_id}
              className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full"
            >
              {mf.name}
            </span>
          ))}
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-gray-100">
        <p className="text-xs text-gray-400">
          🔗 {rec.distance} degree connection
        </p>
      </div>
    </div>
  )
}