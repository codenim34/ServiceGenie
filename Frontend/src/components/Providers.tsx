'use client'

import { AuthProvider } from '@/lib/auth/AuthContext'
import { CartProvider } from '@/lib/store/CartContext'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <AuthProvider>
      <CartProvider>
        {children}
      </CartProvider>
    </AuthProvider>
  )
}
