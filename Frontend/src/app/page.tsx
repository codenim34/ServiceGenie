import Hero from '@/components/home/Hero'
import FeaturedProducts from '@/components/home/FeaturedProducts'
import Categories from '@/components/home/Categories'
import WhyChooseUs from '@/components/home/WhyChooseUs'

export default function Home() {
  return (
    <div className="min-h-screen">
      <Hero />
      <Categories />
      <FeaturedProducts />
      <WhyChooseUs />
    </div>
  )
}
