'use client';

/**
 * Home page - Modern and beautiful design
 */
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuthState } from 'react-firebase-hooks/auth';
import { ShoppingBag, Sparkles, ArrowRight, Star, TrendingUp, Zap } from 'lucide-react';
import { auth } from '../lib/firebase';
import { api } from '../lib/api';
import { Product } from '../lib/types';
import ProductCard from '../components/ProductCard';

export default function Home() {
  const [user] = useAuthState(auth);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await api.getProducts();
        // Handle both array and object response formats
        const productsList = Array.isArray(data) ? data : (data.products || []);
        setProducts(productsList.slice(0, 6));
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative min-h-[85vh] flex items-center justify-center overflow-hidden">
        {/* Animated Background Gradient */}
        <div className="absolute inset-0 royal-gradient opacity-90"></div>
        
        {/* Animated Blob Backgrounds */}
        <div className="absolute inset-0 overflow-hidden">
          <motion.div
            className="absolute top-20 left-10 w-96 h-96 bg-[#0047e6] rounded-full mix-blend-multiply filter blur-3xl opacity-20"
            animate={{
              scale: [1, 1.2, 1],
              x: [0, 50, 0],
              y: [0, 30, 0],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
          <motion.div
            className="absolute top-40 right-10 w-96 h-96 bg-[#1a66ff] rounded-full mix-blend-multiply filter blur-3xl opacity-20"
            animate={{
              scale: [1, 1.3, 1],
              x: [0, -40, 0],
              y: [0, 50, 0],
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 1
            }}
          />
          <motion.div
            className="absolute -bottom-20 left-1/2 w-96 h-96 bg-[#002780] rounded-full mix-blend-multiply filter blur-3xl opacity-20"
            animate={{
              scale: [1, 1.1, 1],
              x: [0, 30, 0],
              y: [0, -40, 0],
            }}
            transition={{
              duration: 12,
              repeat: Infinity,
              ease: "easeInOut",
              delay: 2
            }}
          />
        </div>

        {/* Content */}
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center max-w-5xl mx-auto">
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="flex items-center justify-center mb-6">
                <Sparkles className="text-[#0047e6] mr-3" size={40} />
                <h1 className="text-5xl md:text-7xl font-bold text-white">
                  Welcome to <span className="text-[#0047e6] shimmer">ServiceGenie</span>
                </h1>
              </div>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
                className="text-xl md:text-2xl text-gray-300 mb-4"
              >
                AI-powered commerce platform for seamless shopping experience
              </motion.p>
              
              <motion.p
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.4 }}
                className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto"
              >
                Discover amazing products with intelligent recommendations, 
                personalized shopping assistance, and unbeatable deals.
              </motion.p>

              {!user && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.8, delay: 0.6 }}
                  className="flex flex-col sm:flex-row gap-4 justify-center mb-16"
                >
                  <Link
                    href="/register"
                    className="inline-flex items-center justify-center px-8 py-4 royal-gradient hover:royal-gradient-hover rounded-lg text-white font-semibold text-lg transition-all transform hover:scale-105 shadow-lg shadow-[#0047e6]/50"
                  >
                    <ShoppingBag className="mr-2" size={24} />
                    Get Started
                    <ArrowRight className="ml-2" size={20} />
                  </Link>
                  <Link
                    href="/login"
                    className="inline-flex items-center justify-center px-8 py-4 glass-effect hover:bg-[#0047e6]/20 rounded-lg text-white font-semibold text-lg transition-all border border-[#0047e6]/30"
                  >
                    Login
                  </Link>
                </motion.div>
              )}

              {/* Stats */}
              <motion.div
                initial={{ opacity: 0, y: 40 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.8, delay: 0.8 }}
                className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12"
              >
                <div className="glass-effect p-6 rounded-xl hover:scale-105 transition-transform">
                  <div className="flex items-center justify-center mb-3">
                    <TrendingUp className="text-[#0047e6] mr-2" size={28} />
                    <h3 className="text-4xl font-bold text-[#0047e6]">1000+</h3>
                  </div>
                  <p className="text-gray-300 text-lg">Products</p>
                </div>
                <div className="glass-effect p-6 rounded-xl hover:scale-105 transition-transform">
                  <div className="flex items-center justify-center mb-3">
                    <Star className="text-[#0047e6] mr-2" size={28} />
                    <h3 className="text-4xl font-bold text-[#0047e6]">500+</h3>
                  </div>
                  <p className="text-gray-300 text-lg">Happy Customers</p>
                </div>
                <div className="glass-effect p-6 rounded-xl hover:scale-105 transition-transform">
                  <div className="flex items-center justify-center mb-3">
                    <Zap className="text-[#0047e6] mr-2" size={28} />
                    <h3 className="text-4xl font-bold text-[#0047e6]">24/7</h3>
                  </div>
                  <p className="text-gray-300 text-lg">AI Support</p>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="py-20 relative">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6 }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-4">
              Featured Products
            </h2>
            <div className="w-24 h-1 royal-gradient mx-auto mb-4"></div>
            <p className="text-gray-400 text-lg max-w-2xl mx-auto">
              Discover our handpicked selection of premium products
            </p>
          </motion.div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {[...Array(6)].map((_, i) => (
                <motion.div
                  key={i}
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.3, delay: i * 0.1 }}
                  className="glass-effect rounded-xl p-6 animate-pulse"
                >
                  <div className="bg-gray-700/50 h-64 rounded-lg mb-4"></div>
                  <div className="bg-gray-700/50 h-4 rounded mb-2"></div>
                  <div className="bg-gray-700/50 h-4 rounded w-2/3"></div>
                </motion.div>
              ))}
            </div>
          ) : products.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-center py-16"
            >
              <div className="glass-effect rounded-xl p-12 max-w-md mx-auto">
                <ShoppingBag className="mx-auto mb-4 text-gray-500" size={64} />
                <p className="text-gray-400 text-xl">
                  No products available at the moment.
                </p>
                <p className="text-gray-500 mt-2">
                  Check back soon for amazing deals!
                </p>
              </div>
            </motion.div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {products.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 30 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: index * 0.1 }}
                >
                  <ProductCard product={product} />
                </motion.div>
              ))}
            </div>
          )}

          {products.length > 0 && (
            <motion.div
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              className="text-center mt-12"
            >
              <Link
                href="/products"
                className="inline-flex items-center glass-effect hover:bg-[#0047e6]/20 px-8 py-4 rounded-lg text-white font-semibold text-lg transition-all border border-[#0047e6]/30 group"
              >
                View All Products
                <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={20} />
              </Link>
            </motion.div>
          )}
        </div>
      </section>
    </div>
  );
}

