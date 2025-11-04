import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

class APIClient {
  private client = axios.create({
    baseURL: API_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  })

  constructor() {
    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle unauthorized
          window.location.href = '/auth/login'
        }
        return Promise.reject(error)
      }
    )
  }

  setAuthToken(token: string | null) {
    if (token) {
      this.client.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete this.client.defaults.headers.common['Authorization']
    }
  }

  async get<T>(url: string, config = {}) {
    const response = await this.client.get<T>(url, config)
    return response.data
  }

  async post<T>(url: string, data: any, config = {}) {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async put<T>(url: string, data: any, config = {}) {
    const response = await this.client.put<T>(url, data, config)
    return response.data
  }

  async delete<T>(url: string, config = {}) {
    const response = await this.client.delete<T>(url, config)
    return response.data
  }
}

export const apiClient = new APIClient()
