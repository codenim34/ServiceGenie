import Link from 'next/link'
import { Facebook, Twitter, Instagram, Mail, Phone, MapPin } from 'lucide-react'

export default function Footer() {
  return (
    <footer className="glass-effect mt-20">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* About Section */}
          <div>
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-10 h-10 rounded-full royal-gradient flex items-center justify-center">
                <span className="text-white font-bold text-xl">SG</span>
              </div>
              <span className="text-xl font-bold text-white">ServiceGenie</span>
            </div>
            <p className="text-gray-400 text-sm">
              Your AI-powered e-commerce destination for seamless shopping experience.
            </p>
            <div className="flex space-x-4 mt-4">
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">
                <Facebook size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">
                <Twitter size={20} />
              </a>
              <a href="#" className="text-gray-400 hover:text-primary-400 transition-colors">
                <Instagram size={20} />
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/about" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  About Us
                </Link>
              </li>
              <li>
                <Link href="/products" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  Products
                </Link>
              </li>
              <li>
                <Link href="/categories" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  Categories
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Customer Service */}
          <div>
            <h3 className="text-white font-semibold mb-4">Customer Service</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/faq" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  FAQ
                </Link>
              </li>
              <li>
                <Link href="/shipping" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  Shipping Info
                </Link>
              </li>
              <li>
                <Link href="/returns" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  Returns
                </Link>
              </li>
              <li>
                <Link href="/privacy" className="text-gray-400 hover:text-primary-400 transition-colors text-sm">
                  Privacy Policy
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-white font-semibold mb-4">Contact Us</h3>
            <ul className="space-y-3">
              <li className="flex items-start space-x-2 text-gray-400 text-sm">
                <MapPin size={16} className="mt-1 flex-shrink-0" />
                <span>123 Commerce Street, Dhaka, Bangladesh</span>
              </li>
              <li className="flex items-center space-x-2 text-gray-400 text-sm">
                <Phone size={16} />
                <span>+880 123 456 7890</span>
              </li>
              <li className="flex items-center space-x-2 text-gray-400 text-sm">
                <Mail size={16} />
                <span>support@servicegenie.com</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-primary-500/20 mt-8 pt-8 text-center">
          <p className="text-gray-400 text-sm">
            &copy; {new Date().getFullYear()} ServiceGenie. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}
