'use client';

/**
 * Home page.
 */
import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuthState } from 'react-firebase-hooks/auth';
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
        setProducts(data);
      } catch (error) {
        console.error('Error fetching products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div>
      <div className="text-center mb-12">
        <h1 className="text-4xl font-bold mb-4">Welcome to ServiceGenie</h1>
        <p className="text-xl text-gray-600 mb-8">
          AI-powered commerce platform for seamless shopping experience
        </p>
        {!user && (
          <div className="space-x-4">
            <Link
              href="/register"
              className="px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
            >
              Get Started
            </Link>
            <Link
              href="/login"
              className="px-6 py-3 border border-blue-600 text-blue-600 rounded hover:bg-blue-50 transition"
            >
              Login
            </Link>
          </div>
        )}
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-6">Featured Products</h2>
        {loading ? (
          <div className="text-center py-8">Loading products...</div>
        ) : products.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No products available at the moment.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.slice(0, 6).map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

