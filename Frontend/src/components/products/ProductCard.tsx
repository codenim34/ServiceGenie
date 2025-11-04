'use client'

import Image from 'next/image'
import Link from 'next/link'
import { Product } from '@/types'
import { ShoppingCart, Heart, Star } from 'lucide-react'
import { useCart } from '@/lib/store/CartContext'
import { useState } from 'react'

interface ProductCardProps {
  product: Product
}

export default function ProductCard({ product }: ProductCardProps) {
  const { addToCart } = useCart()
  const [liked, setLiked] = useState(false)

  const discountPercentage = product.originalPrice
    ? Math.round(((product.originalPrice - product.price) / product.originalPrice) * 100)
    : 0

  return (
    <div className="glass-effect rounded-xl overflow-hidden group hover:shadow-2xl hover:shadow-primary-500/20 transition-all">
      <Link href={`/products/${product._id}`} className="block relative">
        <div className="relative h-64 bg-gray-800">
          <Image
            src={product.images[0] || '/placeholder.png'}
            alt={product.name}
            fill
            className="object-cover group-hover:scale-110 transition-transform duration-300"
          />
          
          {discountPercentage > 0 && (
            <div className="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 rounded-lg text-sm font-bold">
              -{discountPercentage}%
            </div>
          )}

          {product.stock < 10 && product.stock > 0 && (
            <div className="absolute top-2 right-2 bg-orange-500 text-white px-2 py-1 rounded-lg text-xs">
              Only {product.stock} left
            </div>
          )}

          {product.stock === 0 && (
            <div className="absolute inset-0 bg-black/60 flex items-center justify-center">
              <span className="text-white text-xl font-bold">Out of Stock</span>
            </div>
          )}
        </div>
      </Link>

      <div className="p-4">
        <Link href={`/products/${product._id}`}>
          <h3 className="text-white font-semibold mb-2 line-clamp-2 hover:text-primary-400 transition-colors">
            {product.name}
          </h3>
        </Link>

        {product.rating && (
          <div className="flex items-center mb-2">
            <div className="flex items-center">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  size={14}
                  className={i < Math.round(product.rating!) ? 'text-yellow-400 fill-yellow-400' : 'text-gray-600'}
                />
              ))}
            </div>
            <span className="text-gray-400 text-sm ml-2">
              ({product.reviews || 0})
            </span>
          </div>
        )}

        <div className="flex items-center justify-between mb-4">
          <div>
            <span className="text-primary-400 font-bold text-xl">
              ${product.price.toFixed(2)}
            </span>
            {product.originalPrice && (
              <span className="text-gray-500 line-through text-sm ml-2">
                ${product.originalPrice.toFixed(2)}
              </span>
            )}
          </div>
        </div>

        <div className="flex gap-2">
          <button
            onClick={() => addToCart(product)}
            disabled={product.stock === 0}
            className="flex-1 royal-gradient hover:royal-gradient-hover disabled:bg-gray-600 disabled:cursor-not-allowed text-white py-2 px-4 rounded-lg font-medium flex items-center justify-center transition-all"
          >
            <ShoppingCart size={18} className="mr-2" />
            Add to Cart
          </button>
          
          <button
            onClick={() => setLiked(!liked)}
            className={`glass-effect p-2 rounded-lg transition-colors ${
              liked ? 'text-red-500' : 'text-gray-400 hover:text-red-500'
            }`}
          >
            <Heart size={20} className={liked ? 'fill-current' : ''} />
          </button>
        </div>
      </div>
    </div>
  )
}
