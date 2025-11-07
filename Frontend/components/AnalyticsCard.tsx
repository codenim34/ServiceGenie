'use client';

/**
 * Analytics card component for displaying statistics.
 */
import React from 'react';
import { Analytics } from '../lib/types';

interface AnalyticsCardProps {
  analytics: Analytics;
}

export default function AnalyticsCard({ analytics }: AnalyticsCardProps) {
  const cards = [
    {
      title: 'Total Orders',
      value: analytics.total_orders,
      color: 'bg-blue-500',
    },
    {
      title: 'Total Sales',
      value: `$${analytics.total_sales.toFixed(2)}`,
      color: 'bg-green-500',
    },
    {
      title: 'Total Products',
      value: analytics.total_products,
      color: 'bg-purple-500',
    },
    {
      title: 'Pending Orders',
      value: analytics.pending_orders,
      color: 'bg-orange-500',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card, index) => (
        <div
          key={index}
          className={`${card.color} text-white p-6 rounded-lg shadow-md`}
        >
          <h3 className="text-lg font-semibold mb-2">{card.title}</h3>
          <p className="text-3xl font-bold">{card.value}</p>
        </div>
      ))}
    </div>
  );
}

