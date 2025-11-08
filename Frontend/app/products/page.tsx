'use client';

/**
 * Products management page.
 */
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '../../lib/firebase';
import { api } from '../../lib/api';
import { Product } from '../../lib/types';
import ProductCard from '../../components/ProductCard';
import ProductForm from '../../components/ProductForm';
import toast from 'react-hot-toast';

export default function ProductsPage() {
  const router = useRouter();
  const [user, loading] = useAuthState(auth);
  const [products, setProducts] = useState<Product[]>([]);
  const [loadingProducts, setLoadingProducts] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
      return;
    }

    if (user) {
      fetchProducts();
    }
  }, [user, loading]);

  const fetchProducts = async () => {
    try {
      const data = await api.getProducts();
      setProducts(data);
    } catch (error) {
      console.error('Error fetching products:', error);
      toast.error('Failed to fetch products');
    } finally {
      setLoadingProducts(false);
    }
  };

  const handleSubmit = async (formData: FormData) => {
    try {
      if (editingProduct) {
        // Update product
        const updateData: any = {};
        formData.forEach((value, key) => {
          if (key !== 'image') {
            updateData[key] = value;
          }
        });

        if (updateData.quantity !== undefined) {
          updateData.stock = Number(updateData.quantity);
          delete updateData.quantity;
        }
        if (updateData.stock !== undefined) {
          updateData.stock = Number(updateData.stock);
        }
        if (updateData.price !== undefined) {
          updateData.price = parseFloat(updateData.price);
        }
        if (updateData.is_available !== undefined) {
          updateData.is_available = updateData.is_available === 'true';
        }

        await api.updateProduct(editingProduct.id, updateData);
        toast.success('Product updated successfully');
      } else {
        // Create product
        await api.createProduct(formData);
        toast.success('Product created successfully');
      }
      setShowForm(false);
      setEditingProduct(null);
      fetchProducts();
    } catch (error) {
      console.error('Error saving product:', error);
      toast.error('Failed to save product');
    }
  };

  const handleEdit = (product: Product) => {
    setEditingProduct(product);
    setShowForm(true);
  };

  const handleDelete = async (productId: string) => {
    if (!confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      await api.deleteProduct(productId);
      toast.success('Product deleted successfully');
      fetchProducts();
    } catch (error) {
      console.error('Error deleting product:', error);
      toast.error('Failed to delete product');
    }
  };

  if (loading || loadingProducts) {
    return <div className="text-center py-8">Loading...</div>;
  }

  if (!user) {
    return null;
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Products</h1>
        <button
          onClick={() => {
            setEditingProduct(null);
            setShowForm(true);
          }}
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
        >
          Add Product
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-lg shadow">
          <h2 className="text-xl font-bold mb-4">
            {editingProduct ? 'Edit Product' : 'Create Product'}
          </h2>
          <ProductForm
            product={editingProduct || undefined}
            onSubmit={handleSubmit}
            onCancel={() => {
              setShowForm(false);
              setEditingProduct(null);
            }}
          />
        </div>
      )}

      {products.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No products yet. Create your first product!
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {products.map((product) => (
            <div key={product.id}>
              <ProductCard product={product} />
              <div className="mt-2 flex space-x-2">
                <button
                  onClick={() => handleEdit(product)}
                  className="px-3 py-1 bg-yellow-500 text-white rounded hover:bg-yellow-600 transition"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(product.id)}
                  className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

