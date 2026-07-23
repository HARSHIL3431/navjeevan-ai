import { motion } from "framer-motion";
import { ArrowRight, Calendar, Tag } from "lucide-react";

export default function BlogSection() {
  const posts = [
    {
      title: "How South Gujarat Farmers Can Maximize Wheat Bidding Rates",
      category: "Market Strategy",
      date: "July 20, 2026",
      image: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
    },
    {
      title: "Step-by-Step PM Fasal Bima Crop Insurance Claim Guide",
      category: "Govt Schemes",
      date: "July 18, 2026",
      image: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
    },
    {
      title: "Weather Risk Management for Groundnut Moisture Control",
      category: "Smart Farming",
      date: "July 14, 2026",
      image: "https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=800&q=80",
    },
  ];

  return (
    <section id="blog" className="py-28 bg-bgSoft">
      <div className="max-w-container mx-auto px-6">
        {/* SECTION HEADER */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <span>Latest Articles & Guides</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText leading-tight">
            Agricultural Insights & <span className="text-primary font-serif italic">News</span>
          </h2>
        </div>

        {/* BLOG CARDS GRID */}
        <div className="grid md:grid-cols-3 gap-8">
          {posts.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              className="bg-white rounded-3xl overflow-hidden shadow-soft hover:shadow-cardHover border border-borderColor/60 transition-all duration-500 group flex flex-col justify-between"
            >
              <div>
                <div className="relative h-52 overflow-hidden">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                  />
                  <div className="absolute top-4 left-4 bg-primary text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                    {item.category}
                  </div>
                </div>

                <div className="p-6">
                  <div className="flex items-center gap-4 text-xs text-grayText mb-3">
                    <span className="flex items-center gap-1">
                      <Calendar className="w-3.5 h-3.5 text-primary" />
                      {item.date}
                    </span>
                  </div>
                  <h3 className="text-lg font-bold font-sans text-darkText mb-3 group-hover:text-primary transition-colors leading-snug">
                    {item.title}
                  </h3>
                </div>
              </div>

              <div className="px-6 pb-6">
                <a
                  href="#contact"
                  className="flex items-center gap-2 text-sm font-semibold text-primary group-hover:text-primary-dark"
                >
                  <span>Read Article</span>
                  <ArrowRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
                </a>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
