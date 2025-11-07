'use client';

/**
 * Navigation bar component.
 */
import React from 'react';
import Link from 'next/link';
import { useAuthState } from 'react-firebase-hooks/auth';
import { auth } from '../lib/firebase';
import { signOut } from 'firebase/auth';
import { useRouter } from 'next/navigation';

export default function Navbar() {
  const [user, loading] = useAuthState(auth);
  const router = useRouter();

  const handleSignOut = async () => {
    try {
      await signOut(auth);
      router.push('/');
    } catch (error) {
      console.error('Error signing out:', error);
    }
  };

  return (
    <nav className="bg-blue-600 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="text-2xl font-bold">
            ServiceGenie
          </Link>

          <div className="flex items-center space-x-4">
            {loading ? (
              <div className="text-sm">Loading...</div>
            ) : user ? (
              <>
                <Link
                  href="/dashboard"
                  className="px-4 py-2 rounded hover:bg-blue-700 transition"
                >
                  Dashboard
                </Link>
                <Link
                  href="/products"
                  className="px-4 py-2 rounded hover:bg-blue-700 transition"
                >
                  Products
                </Link>
                <Link
                  href="/chat"
                  className="px-4 py-2 rounded hover:bg-blue-700 transition"
                >
                  Chat
                </Link>
                <span className="text-sm">{user.email}</span>
                <button
                  onClick={handleSignOut}
                  className="px-4 py-2 bg-red-500 rounded hover:bg-red-600 transition"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/login"
                  className="px-4 py-2 rounded hover:bg-blue-700 transition"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="px-4 py-2 bg-blue-500 rounded hover:bg-blue-700 transition"
                >
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

