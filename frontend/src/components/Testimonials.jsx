import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";

export default function Testimonials() {
  const reviews = [
    {
      name: "Rajeshbhai Patel",
      role: "Wheat & Cotton Farmer, Surat",
      review: "Navjeevan AI gave me the exact bidding price for Surat APMC mandi. I sold 25 quintals of wheat at ₹2,120/qtl instead of ₹1,980 at local traders!",
      avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80",
    },
    {
      name: "Sureshbhai Desai",
      role: "Groundnut Grower, Navsari",
      review: "The Kisan Credit Card document checklist was 100% accurate. I gathered my 7/12 extract and Aadhaar forms in one afternoon without multiple bank trips.",
      avatar: "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?auto=format&fit=crop&w=200&q=80",
    },
    {
      name: "Dineshbhai Chaudhari",
      role: "Paddy Farmer, Bardoli",
      review: "The weather advisor notified me about heavy rain in South Gujarat just before spraying pesticide. Saved me thousands of rupees in chemical costs!",
      avatar: "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?auto=format&fit=crop&w=200&q=80",
    },
  ];

  return (
    <section className="py-28 bg-bgSoft relative overflow-hidden">
      <div className="max-w-container mx-auto px-6">
        {/* SECTION HEADER */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <span>Farmer Testimonials</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText leading-tight">
            Trusted by <span className="text-primary font-serif italic">10,000+ Farmers</span>
          </h2>
        </div>

        {/* TESTIMONIAL CARDS GRID */}
        <div className="grid md:grid-cols-3 gap-8">
          {reviews.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.15 }}
              className="bg-white p-8 rounded-3xl shadow-soft border border-borderColor/60 relative flex flex-col justify-between"
            >
              <div>
                <Quote className="w-10 h-10 text-accentYellow/40 mb-4" />
                <div className="flex gap-1 text-accentYellow mb-4">
                  {[...Array(5)].map((_, i) => (
                    <Star key={i} className="w-4 h-4 fill-current" />
                  ))}
                </div>
                <p className="text-grayText text-sm leading-relaxed mb-6 font-light italic">
                  "{item.review}"
                </p>
              </div>

              <div className="flex items-center gap-4 pt-4 border-t border-gray-100">
                <img
                  src={item.avatar}
                  alt={item.name}
                  className="w-12 h-12 rounded-full object-cover border-2 border-primary/20"
                />
                <div>
                  <h4 className="text-base font-bold text-darkText">{item.name}</h4>
                  <p className="text-xs text-grayText">{item.role}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
