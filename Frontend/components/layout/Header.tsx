'use client';

export default function Header() {
  return (
    <header className="bg-white shadow-sm">
      <nav className="container mx-auto px-4 py-3">
        <div className="flex items-center justify-between">
          <a href="/" className="text-2xl font-bold text-blue-600">
            ServiceGenie
          </a>
          <div className="flex items-center space-x-4">
            <a href="/products" className="text-gray-600 hover:text-blue-600">
              Products
            </a>
            <a href="/chat" className="text-gray-600 hover:text-blue-600">
              Chat
            </a>
            <a href="/dashboard" className="text-gray-600 hover:text-blue-600">
              Dashboard
            </a>
          </div>
        </div>
      </nav>
    </header>
  );
}