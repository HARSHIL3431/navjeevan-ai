import { motion } from "framer-motion";
import { Check, ShieldCheck, ArrowRight } from "lucide-react";

export default function AboutSection({ onOpenChat }) {
  const checklist = [
    "Real-time Mandi Rate Aggregation across Gujarat",
    "Verified APMC Trader Contact Directory",
    "Government Scheme Eligibility & Document Checklist",
    "Smart AI Decision Engine for Fertilizer & Crop Protection"
  ];

  return (
    <section id="about" className="py-28 bg-white relative overflow-hidden">
      <div className="max-w-container mx-auto px-6 grid lg:grid-cols-12 gap-16 items-center">
        {/* LEFT COLUMN: IMAGE WITH BADGE */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="lg:col-span-6 relative"
        >
          <div className="relative rounded-4xl overflow-hidden shadow-2xl border-8 border-bgSoft">
            <img
              src="https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=1000&q=80"
              alt="Navjeevan AI Agriculture"
              className="w-full h-[540px] object-cover hover:scale-105 transition-transform duration-700"
            />
          </div>

          {/* FLOATING EXPERIENCE BADGE */}
          <div className="absolute bottom-8 right-8 bg-primary text-white p-6 rounded-3xl shadow-xl max-w-[200px] border border-white/20">
            <div className="text-4xl font-bold font-sans text-accentYellow">15+</div>
            <div className="text-xs uppercase tracking-wider font-medium text-white/90 mt-1">
              Years of Gujarat Agricultural Data
            </div>
          </div>
        </motion.div>

        {/* RIGHT COLUMN: TEXT CONTENT */}
        <motion.div
          initial={{ opacity: 0, x: 40 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="lg:col-span-6"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <ShieldCheck className="w-4 h-4" />
            <span>About Navjeevan AI</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText mb-6 leading-tight">
            Empowering Farmers with <span className="text-primary font-serif italic">Real-Time Data</span>
          </h2>

          <p className="text-grayText text-base sm:text-lg mb-8 leading-relaxed font-light">
            Navjeevan AI bridges the gap between traditional farming and modern data science. Built specifically for farmers in Gujarat, our platform aggregates real-time mandi prices, trader directories, and government welfare schemes into a simple AI interface.
          </p>

          <div className="space-y-4 mb-10">
            {checklist.map((item, index) => (
              <div key={index} className="flex items-center gap-3">
                <div className="w-6 h-6 rounded-full bg-lightGreen/20 text-primary flex items-center justify-center flex-shrink-0">
                  <Check className="w-4 h-4" />
                </div>
                <span className="text-darkText font-medium text-base">{item}</span>
              </div>
            ))}
          </div>

          <button
            onClick={onOpenChat}
            className="flex items-center gap-3 bg-primary hover:bg-primary-dark text-white font-semibold px-8 py-4 rounded-full shadow-md hover:shadow-lg transition-all"
          >
            <span>Ask AI Assistant</span>
            <ArrowRight className="w-5 h-5" />
          </button>
        </motion.div>
      </div>
    </section>
  );
}
