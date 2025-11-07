'use client';

/**
 * Owner dashboard page.
 */
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '../../lib/firebase';
import { api } from '../../lib/api';
import { Analytics, Product, Order } from '../../lib/types';
import AnalyticsCard from '../../components/AnalyticsCard';
import ProductCard from '../../components/ProductCard';
import Link from 'next/link';

export default function DashboardPage() {
  const router = useRouter();
  const [user, loading] = useAuthState(auth);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [products, setProducts] = useState<Product[]>([]);
  const [orders, setOrders] = useState<Order[]>([]);
  const [loadingData, setLoadingData] = useState(true);

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
      return;
    }

    if (user) {
      fetchDashboardData();
    }
  }, [user, loading]);

  const fetchDashboardData = async () => {
    try {
      const [analyticsData, productsData, ordersData] = await Promise.all([
        api.getOwnerAnalytics(),
        api.getProducts(),
        api.getOrders(),
      ]);
      setAnalytics(analyticsData);
      setProducts(productsData);
      setOrders(ordersData);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoadingData(false);
    }
  };

  if (loading || loadingData) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (!user) {
    return null;
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <Link
          href="/products"
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Manage Products
        </Link>
      </div>

      {analytics && <AnalyticsCard analytics={analytics} />}

      <div>
        <h2 className="text-2xl font-bold mb-4">Recent Products</h2>
        {products.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No products yet. <Link href="/products" className="text-blue-600 hover:underline">Create your first product</Link>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {products.slice(0, 6).map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>

      <div>
        <h2 className="text-2xl font-bold mb-4">Recent Orders</h2>
        {orders.length === 0 ? (
          <div className="text-center py-8 text-gray-500">No orders yet.</div>
        ) : (
          <div className="space-y-4">
            {orders.slice(0, 5).map((order) => (
              <div key={order.id} className="bg-white p-4 rounded-lg shadow">
                <div className="flex justify-between items-center">
                  <div>
                    <p className="font-semibold">{order.customer_email}</p>
                    <p className="text-sm text-gray-600">
                      {order.items.length} item(s) - ${order.total_amount.toFixed(2)}
                    </p>
                  </div>
                  <span
                    className={`px-3 py-1 rounded text-sm ${
                      order.status === 'pending'
                        ? 'bg-yellow-100 text-yellow-800'
                        : order.status === 'confirmed'
                        ? 'bg-blue-100 text-blue-800'
                        : order.status === 'delivered'
                        ? 'bg-green-100 text-green-800'
                        : 'bg-gray-100 text-gray-800'
                    }`}
                  >
                    {order.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

