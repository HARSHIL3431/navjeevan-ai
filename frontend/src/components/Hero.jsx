import { motion } from "framer-motion";
import { ArrowRight, Sparkles, TrendingUp, Users, Award } from "lucide-react";

export default function Hero({ onOpenChat }) {
  return (
    <section id="home" className="relative min-h-screen pt-32 pb-20 bg-primary-dark overflow-hidden flex items-center">
      {/* BACKGROUND IMAGE OVERLAY */}
      <div 
        className="absolute inset-0 bg-cover bg-center opacity-25 mix-blend-overlay"
        style={{ backgroundImage: `url('https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=2000&q=80')` }}
      />

      {/* GRADIENT OVERLAY */}
      <div className="absolute inset-0 bg-gradient-to-b from-primary-dark/80 via-primary-dark/90 to-bgSoft" />

      {/* ORGANIC FLOATING SHAPES */}
      <div className="absolute top-20 left-10 w-72 h-72 bg-lightGreen/10 rounded-full blur-3xl animate-pulse-glow" />
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-accentYellow/10 rounded-full blur-3xl animate-pulse-glow" />

      <div className="max-w-container mx-auto px-6 relative z-10 grid lg:grid-cols-12 gap-12 items-center">
        {/* LEFT COLUMN: HERO TEXT */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="lg:col-span-7 text-white"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-accentYellow text-xs font-semibold uppercase tracking-wider mb-6">
            <Sparkles className="w-4 h-4" />
            <span>AI-Powered Agriculture Management</span>
          </div>

          <h1 className="text-4xl sm:text-5xl lg:text-6xl xl:text-7xl font-bold font-sans tracking-tight leading-[1.1] mb-6">
            Smart Farming Solutions for <span className="text-accentYellow italic font-serif">Gujarat Farmers</span>
          </h1>

          <p className="text-lg sm:text-xl text-white/80 max-w-2xl mb-8 leading-relaxed font-light">
            Real-time APMC mandi prices, instant crop disease advisory, direct trader directory, and automated government scheme assistance driven by Navjeevan AI intelligence.
          </p>

          <div className="flex flex-wrap items-center gap-4 mb-12">
            <button
              onClick={onOpenChat}
              className="flex items-center gap-3 bg-accentYellow hover:bg-yellow-400 text-darkText font-semibold text-base px-8 py-4 rounded-full shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-1"
            >
              <span>Explore AI Advisory</span>
              <ArrowRight className="w-5 h-5" />
            </button>

            <a
              href="#weather"
              className="flex items-center gap-2 bg-lightGreen hover:bg-emerald-600 text-white font-semibold text-base px-7 py-4 rounded-full shadow-md hover:shadow-lg transition-all transform hover:-translate-y-1"
            >
              <span>🌦️ Weather Detection</span>
            </a>

            <a
              href="#services"
              className="flex items-center gap-2 border-2 border-white/30 hover:border-white text-white font-medium text-base px-7 py-3.5 rounded-full transition-all hover:bg-white/10"
            >
              Our Services
            </a>
          </div>


          {/* HERO STATS BAR */}
          <div className="grid grid-cols-3 gap-6 pt-8 border-t border-white/15">
            <div>
              <div className="text-3xl font-bold text-accentYellow font-sans">10K+</div>
              <div className="text-xs text-white/70 uppercase tracking-wider mt-1 font-medium">Farmers Empowered</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-accentYellow font-sans">98%</div>
              <div className="text-xs text-white/70 uppercase tracking-wider mt-1 font-medium">Query Satisfaction</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-accentYellow font-sans">15+ Yrs</div>
              <div className="text-xs text-white/70 uppercase tracking-wider mt-1 font-medium">Agricultural Data</div>
            </div>
          </div>
        </motion.div>

        {/* RIGHT COLUMN: HERO IMAGE & FLOATING CARDS */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="lg:col-span-5 relative"
        >
          <div className="relative mx-auto max-w-md lg:max-w-none">
            {/* HERO MAIN IMAGE */}
            <div className="relative z-10 rounded-4xl overflow-hidden shadow-2xl border-4 border-white/20">
              <img
                src="https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?auto=format&fit=crop&w=1000&q=80"
                alt="Gujarat Agriculture Farmer"
                className="w-full h-[520px] object-cover hover:scale-105 transition-transform duration-700"
              />
            </div>

            {/* FLOATING CARD 1 */}
            <motion.div
              initial={{ y: 20 }}
              animate={{ y: [0, -10, 0] }}
              transition={{ repeat: Infinity, duration: 4, ease: "easeInOut" }}
              className="absolute -top-6 -left-6 z-20 glass-card p-4 rounded-2xl shadow-soft flex items-center gap-3 border border-white/40"
            >
              <div className="w-12 h-12 rounded-xl bg-primary/10 text-primary flex items-center justify-center">
                <TrendingUp className="w-6 h-6" />
              </div>
              <div>
                <div className="text-xs text-grayText font-medium">Surat Mandi Wheat</div>
                <div className="text-base font-bold text-darkText">₹2,120 / Quintal</div>
              </div>
            </motion.div>

            {/* FLOATING CARD 2 */}
            <motion.div
              initial={{ y: -20 }}
              animate={{ y: [0, 10, 0] }}
              transition={{ repeat: Infinity, duration: 5, ease: "easeInOut" }}
              className="absolute -bottom-6 -right-6 z-20 glass-card p-4 rounded-2xl shadow-soft flex items-center gap-3 border border-white/40"
            >
              <div className="w-12 h-12 rounded-xl bg-lightGreen/20 text-primary flex items-center justify-center">
                <Award className="w-6 h-6" />
              </div>
              <div>
                <div className="text-xs text-grayText font-medium">PM Kisan Scheme</div>
                <div className="text-base font-bold text-darkText">Direct Subsidy</div>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
