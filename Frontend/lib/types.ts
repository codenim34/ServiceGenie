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
  sku?: string;
  description?: string;
  price: number;
  category: string;
  color?: string;
  size?: string;
  image_url?: string;
  stock: number;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface BusinessLocation {
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  country?: string;
  latitude?: number;
  longitude?: number;
}

export interface BusinessContact {
  name?: string;
  email?: string;
  phone?: string;
  whatsapp?: string;
  website?: string;
}

export interface StorefrontMeta {
  slug: string;
  url?: string;
  published: boolean;
  updated_at?: string;
}

export interface BusinessProfile {
  name: string;
  slug: string;
  description?: string;
  category?: string;
  logo_url?: string;
  location?: BusinessLocation;
  contact?: BusinessContact;
  storefront?: StorefrontMeta;
  created_at: string;
  updated_at: string;
}

export interface OwnerOnboarding {
  completed: boolean;
  completed_at?: string;
  storefront_url?: string;
  storefront_slug?: string;
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
  business_profile?: BusinessProfile;
  onboarding?: OwnerOnboarding;
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

export interface StorefrontData {
  business: {
    name: string;
    description?: string;
    category?: string;
    logo_url?: string;
    location?: BusinessLocation;
    contact?: BusinessContact;
    storefront: StorefrontMeta;
  };
  products: Product[];
}

