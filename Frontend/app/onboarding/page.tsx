'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import React, { useEffect, useMemo, useState } from 'react';
import toast from 'react-hot-toast';
import { useAuthState } from 'react-firebase-hooks/auth';

import ProductForm from '../../components/ProductForm';
import ProductCard from '../../components/ProductCard';
import { api } from '../../lib/api';
import { auth } from '../../lib/firebase';
import {
  BusinessContact,
  BusinessLocation,
  Owner,
  Product,
} from '../../lib/types';

const steps = ['Business Profile', 'Products', 'Launch'];

type LocationFormState = BusinessLocation & {
  address_line1: string;
  address_line2: string;
  city: string;
  state: string;
  postal_code: string;
  country: string;
};

type ContactFormState = BusinessContact & {
  name: string;
  email: string;
  phone: string;
  whatsapp: string;
  website: string;
};

const initialLocation: LocationFormState = {
  address_line1: '',
  address_line2: '',
  city: '',
  state: '',
  postal_code: '',
  country: '',
};

const initialContact: ContactFormState = {
  name: '',
  email: '',
  phone: '',
  whatsapp: '',
  website: '',
};

export default function OnboardingPage() {
  const router = useRouter();
  const [user, authLoading] = useAuthState(auth);

  const [owner, setOwner] = useState<Owner | null>(null);
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submittingBusiness, setSubmittingBusiness] = useState(false);
  const [products, setProducts] = useState<Product[]>([]);
  const [productsLoading, setProductsLoading] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [showProductForm, setShowProductForm] = useState(true);

  const [businessName, setBusinessName] = useState('');
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [location, setLocation] = useState<LocationFormState>(initialLocation);
  const [contact, setContact] = useState<ContactFormState>(initialContact);
  const [logoFile, setLogoFile] = useState<File | null>(null);
  const [logoPreview, setLogoPreview] = useState<string | null>(null);
  const [storefrontUrl, setStorefrontUrl] = useState<string | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.replace('/login');
    }
  }, [authLoading, user, router]);

  useEffect(() => {
    if (!authLoading && user) {
      bootstrap();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [authLoading, user?.uid]);

  useEffect(() => {
    return () => {
      if (logoPreview && logoPreview.startsWith('blob:')) {
        URL.revokeObjectURL(logoPreview);
      }
    };
  }, [logoPreview]);

  const bootstrap = async () => {
    try {
      setLoading(true);
      const profile = await ensureOwnerProfile();
      if (profile.onboarding?.completed) {
        router.replace('/dashboard');
        return;
      }

      hydrateBusinessState(profile);
      await fetchProducts(profile.firebase_uid);
    } catch (error) {
      console.error('Failed to load onboarding data', error);
      toast.error('Unable to load onboarding. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const ensureOwnerProfile = async (): Promise<Owner> => {
    try {
      const profile = await api.getOwnerProfile();
      setOwner(profile);
      setStorefrontUrl(profile.onboarding?.storefront_url ?? null);
      return profile;
    } catch (error: any) {
      if (error?.response?.status === 404 && user?.email) {
        const created = await api.createOwner({ email: user.email });
        setOwner(created);
        return created;
      }
      throw error;
    }
  };

  const hydrateBusinessState = (profile: Owner) => {
    const businessProfile = profile.business_profile;
    setBusinessName(businessProfile?.name || profile.business_name || '');
    setCategory(businessProfile?.category || '');
    setDescription(businessProfile?.description || '');

    if (businessProfile?.location) {
      setLocation((prev) => ({
        ...prev,
        ...businessProfile.location,
      }));
    }

    if (businessProfile?.contact) {
      setContact((prev) => ({
        ...prev,
        ...businessProfile.contact,
      }));
    } else if (profile.email) {
      setContact((prev) => ({ ...prev, email: profile.email }));
    }

    if (businessProfile?.logo_url) {
      setLogoPreview(businessProfile.logo_url);
    }
    setStorefrontUrl(profile.onboarding?.storefront_url ?? null);
  };

  const fetchProducts = async (ownerId?: string) => {
    try {
      setProductsLoading(true);
      const resolvedOwnerId = ownerId || owner?.firebase_uid;
      const data = await api.getProducts(resolvedOwnerId);
      setProducts(data);
    } catch (error) {
      console.error('Failed to load products', error);
      toast.error('Unable to load products. Please try again.');
    } finally {
      setProductsLoading(false);
    }
  };

  const filteredLocationPayload = useMemo(() => {
    const payload: Record<string, string> = {};
    Object.entries(location).forEach(([key, value]) => {
      if (value) {
        payload[key] = value;
      }
    });
    return Object.keys(payload).length > 0 ? payload : null;
  }, [location]);

  const filteredContactPayload = useMemo(() => {
    const payload: Record<string, string> = {};
    Object.entries(contact).forEach(([key, value]) => {
      if (value) {
        payload[key] = value;
      }
    });
    return Object.keys(payload).length > 0 ? payload : null;
  }, [contact]);

  const handleBusinessSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!businessName.trim() || !category.trim()) {
      toast.error('Business name and category are required.');
      return;
    }

    try {
      setSubmittingBusiness(true);
      const formData = new FormData();
      formData.append('business_name', businessName.trim());
      formData.append('category', category.trim());
      if (description.trim()) {
        formData.append('description', description.trim());
      }
      if (filteredLocationPayload) {
        formData.append('location', JSON.stringify(filteredLocationPayload));
      }
      if (filteredContactPayload) {
        formData.append('contact', JSON.stringify(filteredContactPayload));
      }
      if (logoFile) {
        formData.append('logo', logoFile);
      }

      const updatedOwner: Owner = await api.completeBusinessOnboarding(formData);
      setOwner(updatedOwner);
      setStorefrontUrl(updatedOwner.onboarding?.storefront_url ?? null);
      toast.success('Business profile saved');
      await fetchProducts(updatedOwner.firebase_uid);
      setStep(1);
    } catch (error) {
      console.error('Failed to complete onboarding', error);
      toast.error('Could not save business profile. Please try again.');
    } finally {
      setSubmittingBusiness(false);
    }
  };

  const handleLogoChange = (file: File | null) => {
    if (logoPreview && logoPreview.startsWith('blob:')) {
      URL.revokeObjectURL(logoPreview);
    }
    if (file) {
      setLogoFile(file);
      setLogoPreview(URL.createObjectURL(file));
    } else {
      setLogoFile(null);
      setLogoPreview(owner?.business_profile?.logo_url || null);
    }
  };

  const handleProductSubmit = async (formData: FormData) => {
    try {
      if (editingProduct) {
        const updatePayload: Record<string, any> = {};
        formData.forEach((value, key) => {
          if (key === 'image') {
            return;
          }
          updatePayload[key] = value;
        });

        if (updatePayload.quantity !== undefined) {
          updatePayload.stock = Number(updatePayload.quantity);
          delete updatePayload.quantity;
        }
        if (updatePayload.stock !== undefined) {
          updatePayload.stock = Number(updatePayload.stock);
        }
        if (updatePayload.price !== undefined) {
          updatePayload.price = parseFloat(updatePayload.price);
        }
        if (updatePayload.is_available !== undefined) {
          updatePayload.is_available = updatePayload.is_available === 'true';
        }

        await api.updateProduct(editingProduct.id, updatePayload);
        toast.success('Product updated');
      } else {
        await api.createProduct(formData);
        toast.success('Product added');
      }

      setEditingProduct(null);
      setShowProductForm(false);
      await fetchProducts(owner?.firebase_uid);
    } catch (error) {
      console.error('Failed to save product', error);
      toast.error('Could not save product. Please try again.');
    }
  };

  const handleDeleteProduct = async (productId: string) => {
    if (!confirm('Remove this product from your storefront?')) {
      return;
    }
    try {
      await api.deleteProduct(productId);
      toast.success('Product removed');
      await fetchProducts(owner?.firebase_uid);
    } catch (error) {
      console.error('Failed to delete product', error);
      toast.error('Could not remove product. Please try again.');
    }
  };

  const proceedToLaunch = async () => {
    try {
      const refreshedOwner = await api.getOwnerProfile();
      setOwner(refreshedOwner);
      setStorefrontUrl(refreshedOwner.onboarding?.storefront_url ?? storefrontUrl);
      setStep(2);
    } catch (error) {
      console.error('Failed to refresh owner profile', error);
      toast.error('Unable to prepare storefront. Please try again.');
    }
  };

  if (loading) {
    return <div className="text-center py-12">Loading onboarding...</div>;
  }

  return (
    <div className="space-y-8">
      <header className="space-y-2">
        <p className="text-sm uppercase tracking-wide text-blue-600">Step {step + 1} of {steps.length}</p>
        <h1 className="text-3xl font-bold">Launch your storefront</h1>
        <p className="text-gray-600">
          We&apos;ll collect a few details about your business, add your first products, and publish your hosted shop page.
        </p>
      </header>

      <div className="flex items-center space-x-6">
        {steps.map((label, index) => {
          const isActive = index === step;
          const isCompleted = index < step;
          return (
            <div key={label} className="flex-1">
              <div className="flex items-center space-x-3">
                <div
                  className={`flex h-10 w-10 items-center justify-center rounded-full border-2 ${
                    isCompleted
                      ? 'border-blue-600 bg-blue-600 text-white'
                      : isActive
                      ? 'border-blue-600 text-blue-600'
                      : 'border-gray-300 text-gray-400'
                  }`}
                >
                  {isCompleted ? '✓' : index + 1}
                </div>
                <div>
                  <p className={`text-sm font-medium ${isActive || isCompleted ? 'text-blue-600' : 'text-gray-400'}`}>
                    {label}
                  </p>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {step === 0 && (
        <section className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
          <form onSubmit={handleBusinessSubmit} className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-[2fr_1fr] gap-6">
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Business Name *</label>
                  <input
                    type="text"
                    value={businessName}
                    onChange={(e) => setBusinessName(e.target.value)}
                    required
                    className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Category *</label>
                    <input
                      type="text"
                      value={category}
                      onChange={(e) => setCategory(e.target.value)}
                      required
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-1">Contact Phone</label>
                    <input
                      type="tel"
                      value={contact.phone}
                      onChange={(e) => setContact((prev) => ({ ...prev, phone: e.target.value }))}
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Description</label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={4}
                    className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    placeholder="Tell shoppers about your business, story, or unique offerings"
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Contact Email</label>
                    <input
                      type="email"
                      value={contact.email}
                      onChange={(e) => setContact((prev) => ({ ...prev, email: e.target.value }))}
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Website</label>
                    <input
                      type="url"
                      value={contact.website}
                      onChange={(e) => setContact((prev) => ({ ...prev, website: e.target.value }))}
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">Location</label>
                    <input
                      type="text"
                      value={location.address_line1}
                      onChange={(e) => setLocation((prev) => ({ ...prev, address_line1: e.target.value }))}
                      placeholder="Street, number"
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">City</label>
                    <input
                      type="text"
                      value={location.city}
                      onChange={(e) => setLocation((prev) => ({ ...prev, city: e.target.value }))}
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-1">State / Region</label>
                    <input
                      type="text"
                      value={location.state}
                      onChange={(e) => setLocation((prev) => ({ ...prev, state: e.target.value }))}
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Postal Code</label>
                    <input
                      type="text"
                      value={location.postal_code}
                      onChange={(e) => setLocation((prev) => ({ ...prev, postal_code: e.target.value }))}
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-1">Country</label>
                    <input
                      type="text"
                      value={location.country}
                      onChange={(e) => setLocation((prev) => ({ ...prev, country: e.target.value }))}
                      className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Business Logo</label>
                  <div className="border border-dashed border-gray-300 rounded-lg p-4 text-center">
                    {logoPreview ? (
                      <div className="space-y-3">
                        <div className="relative mx-auto h-32 w-32 overflow-hidden rounded-full border border-gray-200">
                          <Image src={logoPreview} alt={businessName || 'Business logo'} fill className="object-cover" />
                        </div>
                        <button
                          type="button"
                          onClick={() => handleLogoChange(null)}
                          className="text-sm text-red-500 hover:underline"
                        >
                          Remove logo
                        </button>
                      </div>
                    ) : (
                      <p className="text-sm text-gray-500">Upload a square logo (PNG or JPG)</p>
                    )}
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => handleLogoChange(e.target.files?.[0] || null)}
                      className="mt-3 block w-full text-sm text-gray-600"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">Primary Contact Name</label>
                  <input
                    type="text"
                    value={contact.name}
                    onChange={(e) => setContact((prev) => ({ ...prev, name: e.target.value }))}
                    className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-1">WhatsApp</label>
                  <input
                    type="text"
                    value={contact.whatsapp}
                    onChange={(e) => setContact((prev) => ({ ...prev, whatsapp: e.target.value }))}
                    className="w-full rounded-md border border-gray-200 px-3 py-2 focus:border-blue-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>

            <div className="flex items-center justify-end space-x-4">
              <button
                type="submit"
                disabled={submittingBusiness}
                className="rounded-md bg-blue-600 px-6 py-2 text-white shadow hover:bg-blue-700 disabled:opacity-50"
              >
                {submittingBusiness ? 'Saving...' : 'Save & Continue'}
              </button>
            </div>
          </form>
        </section>
      )}

      {step === 1 && (
        <section className="space-y-6">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-semibold">Add your products</h2>
                <p className="text-sm text-gray-500">Create at least one product to publish your storefront.</p>
              </div>
              <button
                onClick={() => {
                  setEditingProduct(null);
                  setShowProductForm(true);
                }}
                className="rounded-md bg-blue-600 px-4 py-2 text-white shadow hover:bg-blue-700"
              >
                Add Product
              </button>
            </div>

            {showProductForm && (
              <div className="mt-6 border-t border-gray-100 pt-6">
                <ProductForm
                  product={editingProduct || undefined}
                  onSubmit={async (formData) => {
                    await handleProductSubmit(formData);
                    setShowProductForm(false);
                  }}
                  onCancel={() => {
                    setEditingProduct(null);
                    setShowProductForm(false);
                  }}
                />
              </div>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {productsLoading ? (
              <div className="md:col-span-2 lg:col-span-3 text-center py-8">Loading products...</div>
            ) : products.length === 0 ? (
              <div className="md:col-span-2 lg:col-span-3 flex flex-col items-center justify-center space-y-2 rounded-xl border border-dashed border-gray-300 py-12 text-gray-500">
                <p>No products yet.</p>
                <p className="text-sm">Add at least one product to continue.</p>
              </div>
            ) : (
              products.map((product) => (
                <div key={product.id} className="space-y-3">
                  <ProductCard product={product} />
                  <div className="flex space-x-3">
                    <button
                      onClick={() => {
                        setEditingProduct(product);
                        setShowProductForm(true);
                      }}
                      className="flex-1 rounded-md bg-yellow-500 px-3 py-2 text-white hover:bg-yellow-600"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteProduct(product.id)}
                      className="flex-1 rounded-md bg-red-500 px-3 py-2 text-white hover:bg-red-600"
                    >
                      Remove
                    </button>
                  </div>
                </div>
              ))
            )}
          </div>

          <div className="flex items-center justify-end">
            <button
              onClick={proceedToLaunch}
              disabled={products.length === 0}
              className="rounded-md bg-blue-600 px-6 py-2 text-white shadow hover:bg-blue-700 disabled:opacity-50"
            >
              Review & Launch
            </button>
          </div>
        </section>
      )}

      {step === 2 && (
        <section className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 space-y-4">
            <h2 className="text-2xl font-semibold">Your storefront is ready!</h2>
            <p className="text-gray-600">
              Share your hosted storefront link or keep adding products from your dashboard at any time.
            </p>

            <div className="rounded-lg border border-gray-200 p-4 space-y-2">
              <p className="text-sm uppercase tracking-wide text-gray-500">Storefront URL</p>
              {storefrontUrl ? (
                <Link href={storefrontUrl} className="text-blue-600 hover:underline" target="_blank">
                  {storefrontUrl}
                </Link>
              ) : (
                <p className="text-gray-500">Storefront URL will be available once the platform domain is configured.</p>
              )}
            </div>

            <div className="rounded-lg border border-gray-200 p-4 space-y-1">
              <p className="text-sm uppercase tracking-wide text-gray-500">Storefront slug</p>
              <p className="font-mono text-sm">{owner?.business_profile?.slug ?? 'N/A'}</p>
            </div>

            <div className="flex space-x-3 pt-4">
              <Link
                href="/dashboard"
                className="flex-1 rounded-md bg-blue-600 px-4 py-2 text-center text-white hover:bg-blue-700"
              >
                Go to Dashboard
              </Link>
              {storefrontUrl && (
                <Link
                  href={storefrontUrl}
                  target="_blank"
                  className="flex-1 rounded-md border border-blue-600 px-4 py-2 text-center text-blue-600 hover:bg-blue-50"
                >
                  View Storefront
                </Link>
              )}
            </div>
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
            <h3 className="text-lg font-semibold mb-4">Next steps</h3>
            <ul className="space-y-3 text-sm text-gray-600">
              <li>• Invite your team to manage inventory and orders.</li>
              <li>• Configure payment and fulfillment preferences.</li>
              <li>• Share your storefront link on social channels.</li>
            </ul>
          </div>
        </section>
      )}
    </div>
  );
}


