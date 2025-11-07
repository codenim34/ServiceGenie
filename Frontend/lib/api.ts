/**
 * API client for backend communication.
 */
import axios, { AxiosInstance } from 'axios';
import { auth } from './firebase';
import { User } from 'firebase/auth';

const API_BASE_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000';

// Create axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/api/v1`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  async (config) => {
    const user: User | null = auth.currentUser;
    if (user) {
      try {
        const token = await user.getIdToken();
        config.headers.Authorization = `Bearer ${token}`;
      } catch (error) {
        console.error('Error getting auth token:', error);
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// API functions
export const api = {
  // Auth
  verifyToken: async (token: string) => {
    const response = await apiClient.post('/auth/verify', { token });
    return response.data;
  },

  // Products
  getProducts: async (ownerId?: string, category?: string) => {
    const params: any = {};
    if (ownerId) params.owner_id = ownerId;
    if (category) params.category = category;
    const response = await apiClient.get('/products', { params });
    return response.data;
  },

  getProduct: async (productId: string) => {
    const response = await apiClient.get(`/products/${productId}`);
    return response.data;
  },

  createProduct: async (formData: FormData) => {
    const response = await apiClient.post('/products', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  updateProduct: async (productId: string, data: any) => {
    const response = await apiClient.put(`/products/${productId}`, data);
    return response.data;
  },

  deleteProduct: async (productId: string) => {
    await apiClient.delete(`/products/${productId}`);
  },

  // Orders
  createOrder: async (ownerId: string, orderData: any) => {
    const response = await apiClient.post('/orders', orderData, {
      params: { owner_id: ownerId },
    });
    return response.data;
  },

  getOrders: async (ownerId?: string) => {
    const params: any = {};
    if (ownerId) params.owner_id = ownerId;
    const response = await apiClient.get('/orders', { params });
    return response.data;
  },

  getOrder: async (orderId: string) => {
    const response = await apiClient.get(`/orders/${orderId}`);
    return response.data;
  },

  // Owner
  createOwner: async (data: any) => {
    const response = await apiClient.post('/owners', data);
    return response.data;
  },

  getOwnerProfile: async () => {
    const response = await apiClient.get('/owners/me');
    return response.data;
  },

  updateOwnerProfile: async (data: any) => {
    const response = await apiClient.put('/owners/me', data);
    return response.data;
  },

  getOwnerAnalytics: async () => {
    const response = await apiClient.get('/owners/me/analytics');
    return response.data;
  },

  // AI Agent
  chatWithAgent: async (message: string, ownerId?: string) => {
    const response = await apiClient.post('/agent/chat', {
      content: message,
      owner_id: ownerId,
    });
    return response.data;
  },

  getChatHistory: async (ownerId?: string) => {
    const params: any = {};
    if (ownerId) params.owner_id = ownerId;
    const response = await apiClient.get('/agent/chat/history', { params });
    return response.data;
  },
};

export default apiClient;

