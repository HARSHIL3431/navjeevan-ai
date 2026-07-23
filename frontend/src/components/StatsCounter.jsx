import { motion } from "framer-motion";

export default function StatsCounter() {
  const stats = [
    { value: "20K+", label: "Quintals Traced" },
    { value: "12K+", label: "Farmers Connected" },
    { value: "98%", label: "Satisfaction Rate" },
    { value: "250+", label: "Gujarat Mandis Covered" },
  ];

  return (
    <section className="relative py-24 bg-primary-dark text-white overflow-hidden">
      {/* BACKGROUND IMAGE OVERLAY */}
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-20 mix-blend-overlay"
        style={{ backgroundImage: `url('https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=2000&q=80')` }}
      />
      <div className="absolute inset-0 bg-gradient-to-r from-primary-dark via-primary-dark/95 to-primary-dark" />

      <div className="max-w-container mx-auto px-6 relative z-10">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 text-center">
          {stats.map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="p-6 rounded-3xl bg-white/5 backdrop-blur-md border border-white/10"
            >
              <div className="text-4xl sm:text-5xl font-extrabold font-sans text-accentYellow mb-2">
                {item.value}
              </div>
              <div className="text-sm sm:text-base font-medium text-white/80 uppercase tracking-wider">
                {item.label}
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
