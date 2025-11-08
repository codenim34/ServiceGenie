'use client';

/**
 * Product card component for displaying products.
 */
import React from 'react';
import Image from 'next/image';
import { Product } from '../lib/types';

interface ProductCardProps {
  product: Product;
  onAddToCart?: (product: Product) => void;
}

export default function ProductCard({ product, onAddToCart }: ProductCardProps) {
  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition">
      {product.image_url && (
        <div className="relative h-48 w-full">
          <Image
            src={product.image_url}
            alt={product.name}
            fill
            className="object-cover"
          />
        </div>
      )}
      <div className="p-4">
        <h3 className="text-lg font-semibold mb-2">{product.name}</h3>
        {product.sku && (
          <p className="text-xs uppercase tracking-wide text-gray-400 mb-1">SKU: {product.sku}</p>
        )}
        {product.description && (
          <p className="text-gray-600 text-sm mb-2 line-clamp-2">
            {product.description}
          </p>
        )}
        <div className="flex items-center justify-between">
          <span className="text-xl font-bold text-blue-600">
            ${product.price.toFixed(2)}
          </span>
          <span className="text-sm text-gray-500">
            {product.category}
          </span>
        </div>
        <div className="mt-2 space-y-1 text-sm">
          <p className={product.stock > 0 ? 'text-green-600' : 'text-red-600'}>
            {product.stock > 0 ? `Quantity Available: ${product.stock}` : 'Out of Stock'}
          </p>
          {(product.color || product.size) && (
            <p className="text-gray-500">
              {product.color && <span>Color: {product.color}</span>}
              {product.color && product.size && <span className="mx-2">•</span>}
              {product.size && <span>Size: {product.size}</span>}
            </p>
          )}
        </div>
        {onAddToCart && product.is_available && product.stock > 0 && (
          <button
            onClick={() => onAddToCart(product)}
            className="mt-4 w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition"
          >
            Add to Cart
          </button>
        )}
      </div>
    </div>
  );
}

