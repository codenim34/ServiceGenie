'use client'

import { Laptop, Watch, Headphones, Shirt, Home, Gift } from 'lucide-react'
import Link from 'next/link'

const categories = [
  { name: 'Electronics', icon: Laptop, slug: 'electronics', color: 'from-blue-500 to-purple-600' },
  { name: 'Fashion', icon: Shirt, slug: 'fashion', color: 'from-pink-500 to-rose-600' },
  { name: 'Watches', icon: Watch, slug: 'watches', color: 'from-amber-500 to-orange-600' },
  { name: 'Audio', icon: Headphones, slug: 'audio', color: 'from-green-500 to-teal-600' },
  { name: 'Home & Living', icon: Home, slug: 'home-living', color: 'from-indigo-500 to-blue-600' },
  { name: 'Gifts', icon: Gift, slug: 'gifts', color: 'from-red-500 to-pink-600' },
]

export default function Categories() {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-white mb-4">Shop by Category</h2>
          <p className="text-gray-400 text-lg">Explore our wide range of products</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
          {categories.map((category) => {
            const Icon = category.icon
            return (
              <Link
                key={category.slug}
                href={`/products?category=${category.slug}`}
                className="glass-effect p-6 rounded-xl hover:bg-primary-500/20 transition-all transform hover:scale-105 group"
              >
                <div className={`w-16 h-16 rounded-full bg-gradient-to-br ${category.color} flex items-center justify-center mb-4 mx-auto group-hover:rotate-12 transition-transform`}>
                  <Icon className="text-white" size={32} />
                </div>
                <h3 className="text-white text-center font-semibold">{category.name}</h3>
              </Link>
            )
          })}
        </div>
      </div>
    </section>
  )
}
