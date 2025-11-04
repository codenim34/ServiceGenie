import { Truck, Shield, Headphones, CreditCard } from 'lucide-react'

const features = [
  {
    icon: Truck,
    title: 'Free Shipping',
    description: 'On orders over $50',
  },
  {
    icon: Shield,
    title: 'Secure Payment',
    description: '100% secure transactions',
  },
  {
    icon: Headphones,
    title: '24/7 AI Support',
    description: 'Instant assistance anytime',
  },
  {
    icon: CreditCard,
    title: 'Easy Returns',
    description: '30-day return policy',
  },
]

export default function WhyChooseUs() {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <h2 className="text-4xl font-bold text-white mb-4">Why Choose Us</h2>
          <p className="text-gray-400 text-lg">Experience the ServiceGenie difference</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature) => {
            const Icon = feature.icon
            return (
              <div
                key={feature.title}
                className="glass-effect p-8 rounded-xl text-center hover:bg-primary-500/20 transition-all group"
              >
                <div className="w-20 h-20 rounded-full royal-gradient flex items-center justify-center mb-4 mx-auto group-hover:scale-110 transition-transform">
                  <Icon className="text-white" size={40} />
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">{feature.title}</h3>
                <p className="text-gray-400">{feature.description}</p>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
