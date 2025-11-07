/**
 * TypeScript type definitions.
 */

export interface User {
  uid: string;
  email: string | null;
  displayName: string | null;
  photoURL: string | null;
}

export interface Product {
  id: string;
  owner_id: string;
  name: string;
  description?: string;
  price: number;
  category: string;
  image_url?: string;
  stock: number;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface OrderItem {
  product_id: string;
  product_name: string;
  quantity: number;
  price: number;
}

export interface Order {
  id: string;
  owner_id: string;
  customer_id?: string;
  customer_email: string;
  customer_name?: string;
  items: OrderItem[];
  total_amount: number;
  status: 'pending' | 'confirmed' | 'shipped' | 'delivered' | 'cancelled';
  shipping_address?: string;
  created_at: string;
  updated_at: string;
}

export interface Owner {
  id: string;
  firebase_uid: string;
  email: string;
  business_name?: string;
  phone?: string;
  address?: string;
  created_at: string;
  updated_at: string;
}

export interface Analytics {
  total_orders: number;
  total_sales: number;
  total_products: number;
  pending_orders: number;
}

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export interface ChatResponse {
  reply: string;
  products: Product[];
}

