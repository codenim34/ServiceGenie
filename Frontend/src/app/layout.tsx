import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'
import { Providers } from '@/components/Providers'
import Header from '@/components/layout/Header'
import Footer from '@/components/layout/Footer'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'ServiceGenie - Your E-Commerce Destination',
  description: 'AI-powered e-commerce platform for seamless shopping experience',
  keywords: 'ecommerce, shopping, online store, AI assistant',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <Providers>
          <div className="min-h-screen flex flex-col">
            <Header />
            <main className="flex-1">
              {children}
            </main>
            <Footer />
          </div>
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 3000,
              style: {
                background: '#0f1419',
                color: '#fff',
                border: '1px solid #0047e6',
              },
              success: {
                iconTheme: {
                  primary: '#0047e6',
                  secondary: '#fff',
                },
              },
              error: {
                iconTheme: {
                  primary: '#ff4444',
                  secondary: '#fff',
                },
              },
            }}
          />
        </Providers>
      </body>
    </html>
  )
}
