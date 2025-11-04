export interface Product {
  _id: string
  name: string
  description: string
  price: number
  originalPrice?: number
  discount?: number
  category: string
  images: string[]
  stock: number
  rating?: number
  reviews?: number
  tags?: string[]
  specifications?: Record<string, string>
  createdAt: string
  updatedAt: string
}

export interface CartItem {
  product: Product
  quantity: number
}

export interface User {
  _id: string
  uid: string
  email: string
  displayName?: string
  photoURL?: string
  role: 'customer' | 'admin'
  createdAt: string
}

export interface Order {
  _id: string
  userId: string
  items: {
    productId: string
    name: string
    price: number
    quantity: number
    image: string
  }[]
  totalAmount: number
  status: 'pending' | 'processing' | 'shipped' | 'delivered' | 'cancelled'
  paymentStatus: 'pending' | 'paid' | 'failed'
  paymentMethod: string
  shippingAddress: {
    name: string
    phone: string
    address: string
    city: string
    postalCode: string
    country: string
  }
  createdAt: string
  updatedAt: string
}

export interface Category {
  _id: string
  name: string
  slug: string
  description?: string
  image?: string
  icon?: string
}
