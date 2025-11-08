'use client';

export default function Footer() {
  return (
    <footer className="bg-gray-100">
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-gray-600">© 2025 ServiceGenie. All rights reserved.</p>
          </div>
          <div className="flex space-x-6">
            <a href="/about" className="text-gray-600 hover:text-blue-600">
              About
            </a>
            <a href="/contact" className="text-gray-600 hover:text-blue-600">
              Contact
            </a>
            <a href="/privacy" className="text-gray-600 hover:text-blue-600">
              Privacy Policy
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}