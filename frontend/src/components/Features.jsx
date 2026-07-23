import { motion } from "framer-motion";
import { Leaf, Cpu, Headphones, CheckCircle2 } from "lucide-react";

export default function Features() {
  const features = [
    {
      icon: Leaf,
      title: "Eco Friendly Practices",
      desc: "Sustainable organic farming recommendations tailored for Gujarat soils and weather cycles.",
      color: "bg-emerald-50 text-emerald-600",
    },
    {
      icon: Cpu,
      title: "AI Powered Insights",
      desc: "Instant price forecasting across APMC mandis and AI intent detection for farmer queries.",
      color: "bg-blue-50 text-blue-600",
    },
    {
      icon: Headphones,
      title: "Fast 24/7 Support",
      desc: "Instant responses on WhatsApp and web interface for schemes, market prices, and traders.",
      color: "bg-amber-50 text-amber-600",
    },
    {
      icon: CheckCircle2,
      title: "Certified Experts",
      desc: "Verified APMC agents, official government scheme links, and updated crop market data.",
      color: "bg-purple-50 text-purple-600",
    },
  ];

  return (
    <section className="py-24 bg-bgSoft relative z-20 -mt-10">
      <div className="max-w-container mx-auto px-6">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((item, index) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white p-8 rounded-3xl shadow-soft hover:shadow-cardHover transition-all duration-300 transform hover:-translate-y-2 border border-borderColor/60 group"
              >
                <div className={`w-14 h-14 rounded-2xl ${item.color} flex items-center justify-center mb-6 transition-transform group-hover:scale-110`}>
                  <Icon className="w-7 h-7" />
                </div>
                <h3 className="text-xl font-bold font-sans text-darkText mb-3 group-hover:text-primary transition-colors">
                  {item.title}
                </h3>
                <p className="text-grayText text-sm leading-relaxed">
                  {item.desc}
                </p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
