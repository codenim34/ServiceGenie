'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ShoppingBag, Sparkles } from 'lucide-react'

export default function Hero() {
  return (
    <section className="relative min-h-[80vh] flex items-center justify-center overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0 bg-gradient-royal opacity-80"></div>
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-primary-500 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-72 h-72 bg-primary-700 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-700"></div>
        <div className="absolute -bottom-8 left-1/2 w-72 h-72 bg-primary-400 rounded-full mix-blend-multiply filter blur-3xl opacity-20 animate-pulse delay-1000"></div>
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="text-center max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="flex items-center justify-center mb-6">
              <Sparkles className="text-primary-400 mr-2" size={32} />
              <h1 className="text-5xl md:text-7xl font-bold text-white">
                Welcome to <span className="text-primary-400">ServiceGenie</span>
              </h1>
            </div>
            
            <p className="text-xl md:text-2xl text-gray-300 mb-8">
              Your AI-powered e-commerce destination for seamless shopping experience
            </p>
            
            <p className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto">
              Discover amazing products with intelligent recommendations, 
              personalized shopping assistance, and unbeatable deals.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/products"
                className="inline-flex items-center justify-center px-8 py-4 royal-gradient hover:royal-gradient-hover rounded-lg text-white font-semibold text-lg transition-all transform hover:scale-105 shadow-lg"
              >
                <ShoppingBag className="mr-2" size={24} />
                Shop Now
              </Link>
              
              <Link
                href="/about"
                className="inline-flex items-center justify-center px-8 py-4 glass-effect hover:bg-primary-500/20 rounded-lg text-white font-semibold text-lg transition-all"
              >
                Learn More
              </Link>
            </div>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0, y: 40 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-20"
          >
            <div className="glass-effect p-6 rounded-lg">
              <h3 className="text-4xl font-bold text-primary-400 mb-2">1000+</h3>
              <p className="text-gray-300">Products</p>
            </div>
            <div className="glass-effect p-6 rounded-lg">
              <h3 className="text-4xl font-bold text-primary-400 mb-2">500+</h3>
              <p className="text-gray-300">Happy Customers</p>
            </div>
            <div className="glass-effect p-6 rounded-lg">
              <h3 className="text-4xl font-bold text-primary-400 mb-2">24/7</h3>
              <p className="text-gray-300">AI Support</p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  )
}
