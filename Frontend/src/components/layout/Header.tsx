'use client'

import Link from 'next/link'
import { useState } from 'react'
import { ShoppingCart, User, Menu, X, Search, LogOut } from 'lucide-react'
import { useAuth } from '@/lib/auth/AuthContext'
import { useCart } from '@/lib/store/CartContext'
import { useRouter } from 'next/navigation'

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const { user, logout } = useAuth()
  const { itemCount } = useCart()
  const router = useRouter()

  const handleLogout = async () => {
    await logout()
    router.push('/')
  }

  return (
    <header className="sticky top-0 z-50 glass-effect">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link href="/" className="flex items-center space-x-2">
            <div className="w-10 h-10 rounded-full royal-gradient flex items-center justify-center">
              <span className="text-white font-bold text-xl">SG</span>
            </div>
            <span className="text-xl font-bold text-white hidden sm:block">
              ServiceGenie
            </span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center space-x-8">
            <Link
              href="/"
              className="text-gray-300 hover:text-primary-400 transition-colors"
            >
              Home
            </Link>
            <Link
              href="/products"
              className="text-gray-300 hover:text-primary-400 transition-colors"
            >
              Products
            </Link>
            <Link
              href="/categories"
              className="text-gray-300 hover:text-primary-400 transition-colors"
            >
              Categories
            </Link>
            <Link
              href="/about"
              className="text-gray-300 hover:text-primary-400 transition-colors"
            >
              About
            </Link>
          </nav>

          {/* Right Side Icons */}
          <div className="flex items-center space-x-4">
            <button className="text-gray-300 hover:text-primary-400 transition-colors">
              <Search size={20} />
            </button>

            <Link
              href="/cart"
              className="relative text-gray-300 hover:text-primary-400 transition-colors"
            >
              <ShoppingCart size={20} />
              {itemCount > 0 && (
                <span className="absolute -top-2 -right-2 bg-primary-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                  {itemCount}
                </span>
              )}
            </Link>

            {user ? (
              <div className="relative group">
                <button className="flex items-center space-x-2 text-gray-300 hover:text-primary-400 transition-colors">
                  <User size={20} />
                  <span className="hidden sm:block">{user.displayName || 'Account'}</span>
                </button>
                
                {/* Dropdown */}
                <div className="absolute right-0 mt-2 w-48 glass-effect rounded-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <Link
                    href="/profile"
                    className="block px-4 py-2 text-gray-300 hover:text-primary-400 hover:bg-primary-500/10 rounded-t-lg"
                  >
                    My Profile
                  </Link>
                  <Link
                    href="/orders"
                    className="block px-4 py-2 text-gray-300 hover:text-primary-400 hover:bg-primary-500/10"
                  >
                    My Orders
                  </Link>
                  <button
                    onClick={handleLogout}
                    className="w-full text-left px-4 py-2 text-gray-300 hover:text-primary-400 hover:bg-primary-500/10 rounded-b-lg flex items-center space-x-2"
                  >
                    <LogOut size={16} />
                    <span>Logout</span>
                  </button>
                </div>
              </div>
            ) : (
              <Link
                href="/auth/login"
                className="px-4 py-2 royal-gradient hover:royal-gradient-hover rounded-lg text-white font-medium transition-all"
              >
                Login
              </Link>
            )}

            {/* Mobile Menu Button */}
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="md:hidden text-gray-300"
            >
              {mobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden py-4 space-y-2">
            <Link
              href="/"
              className="block px-4 py-2 text-gray-300 hover:text-primary-400 hover:bg-primary-500/10 rounded"
              onClick={() => setMobileMenuOpen(false)}
            >
              Home
            </Link>
            <Link
              href="/products"
              className="block px-4 py-2 text-gray-300 hover:text-primary-400 hover:bg-primary-500/10 rounded"
              onClick={() => setMobileMenuOpen(false)}
            >
              Products
            </Link>
            <Link
              href="/categories"
              className="block px-4 py-2 text-gray-300 hover:text-primary-400 hover:bg-primary-500/10 rounded"
              onClick={() => setMobileMenuOpen(false)}
            >
              Categories
            </Link>
            <Link
              href="/about"
              className="block px-4 py-2 text-gray-300 hover:text-primary-400 hover:bg-primary-500/10 rounded"
              onClick={() => setMobileMenuOpen(false)}
            >
              About
            </Link>
          </div>
        )}
      </div>
    </header>
  )
}
