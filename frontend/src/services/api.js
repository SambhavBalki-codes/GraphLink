import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

export const getUsers = (skip = 0, limit = 20) =>
  api.get(`/users?skip=${skip}&limit=${limit}`)

export const getUser = (userId) =>
  api.get(`/users/${userId}`)

export const createUser = (data) =>
  api.post('/users', data)

export const updateUser = (userId, data) =>
  api.patch(`/users/${userId}`, data)

export const deleteUser = (userId) =>
  api.delete(`/users/${userId}`)

export const getUserFriends = (userId) =>
  api.get(`/users/${userId}/friends`)

export const getRecommendations = (userId, limit = 10, algorithm = 'v2') =>
  api.get(`/users/${userId}/recommendations?limit=${limit}&algorithm=${algorithm}`)

export const getConnectionPath = (userId, otherUserId) =>
  api.get(`/users/${userId}/path/${otherUserId}`)

export const getNetworkDegrees = (userId) =>
  api.get(`/users/${userId}/network`)

export const getUserStats = (userId) =>
  api.get(`/users/${userId}/stats`)

export const getNetworkStats = () =>
  api.get('/stats')

export const getCacheStats = () =>
  api.get('/cache/stats')

export const getMetrics = () =>
  api.get('/metrics')

export const createFriendship = (userId1, userId2) =>
  api.post('/friendships', { user_id_1: userId1, user_id_2: userId2 })

export const deleteFriendship = (userId1, userId2) =>
  api.delete('/friendships', { data: { user_id_1: userId1, user_id_2: userId2 } })

export default api