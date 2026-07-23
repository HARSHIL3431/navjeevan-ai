import { motion } from "framer-motion";
import { Sparkles, Award, Zap, ShieldCheck } from "lucide-react";

export default function WhyChooseUs() {
  const reasons = [
    {
      title: "Real Gujarat APMC Mandi Integration",
      desc: "Direct data feeds for Surat, Navsari, Bardoli, and Anand market auctions.",
      icon: Award,
    },
    {
      title: "Zero Latency AI Intent Engine",
      desc: "Fast intent parsing that immediately pinpoints whether you need prices, schemes, or documents.",
      icon: Zap,
    },
    {
      title: "Weather & Spray Risk Advisor",
      desc: "Automated climate risk tracking using OpenWeatherMap & Open-Meteo services.",
      icon: ShieldCheck,
    },
  ];

  return (
    <section className="py-28 bg-white relative overflow-hidden">
      <div className="max-w-container mx-auto px-6 grid lg:grid-cols-12 gap-16 items-center">
        {/* LEFT COLUMN: TEXT CONTENT & PROGRESS */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="lg:col-span-6"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <Sparkles className="w-4 h-4 text-accentYellow" />
            <span>Why Choose Navjeevan AI</span>
          </div>

          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText mb-6 leading-tight">
            Designed for <span className="text-primary font-serif italic">Precision Agriculture</span>
          </h2>

          <p className="text-grayText text-base sm:text-lg mb-10 leading-relaxed font-light">
            Traditional market lookup forces farmers to make multiple calls and wait in long mandi queues. Navjeevan AI provides real-time transparency and instant decision support in seconds.
          </p>

          <div className="space-y-6 mb-12">
            {reasons.map((item, index) => {
              const Icon = item.icon;
              return (
                <div key={index} className="flex gap-4 p-4 rounded-2xl bg-bgSoft border border-borderColor/60">
                  <div className="w-12 h-12 rounded-xl bg-primary text-white flex items-center justify-center flex-shrink-0">
                    <Icon className="w-6 h-6 text-accentYellow" />
                  </div>
                  <div>
                    <h4 className="text-lg font-bold text-darkText mb-1">{item.title}</h4>
                    <p className="text-grayText text-sm leading-relaxed">{item.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>

          {/* CIRCULAR STAT PROGRESS */}
          <div className="grid grid-cols-2 gap-6 pt-6 border-t border-borderColor">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-full border-4 border-primary border-t-accentYellow flex items-center justify-center font-bold text-darkText text-lg">
                98%
              </div>
              <div>
                <div className="font-bold text-darkText">Accuracy Rate</div>
                <div className="text-xs text-grayText">Verified Market Data</div>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-full border-4 border-lightGreen border-r-primary flex items-center justify-center font-bold text-darkText text-lg">
                24/7
              </div>
              <div>
                <div className="font-bold text-darkText">AI Availability</div>
                <div className="text-xs text-grayText">Always Online</div>
              </div>
            </div>
          </div>
        </motion.div>

        {/* RIGHT COLUMN: LARGE IMAGE & DECORATION */}
        <motion.div
          initial={{ opacity: 0, x: 40 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.7 }}
          className="lg:col-span-6 relative"
        >
          <div className="relative rounded-4xl overflow-hidden shadow-2xl border-8 border-bgSoft">
            <img
              src="https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&w=1000&q=80"
              alt="Agriculture Technology"
              className="w-full h-[560px] object-cover hover:scale-105 transition-transform duration-700"
            />
          </div>
        </motion.div>
      </div>
    </section>
  );
}
