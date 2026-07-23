import { motion } from "framer-motion";
import { MessageSquare, Cpu, CheckCircle, Headphones } from "lucide-react";

export default function ProcessTimeline() {
  const steps = [
    {
      num: "01",
      title: "Query & Consultation",
      desc: "Ask any farming question regarding crop prices, PM Kisan, KCC, or disease symptoms.",
      icon: MessageSquare,
    },
    {
      num: "02",
      title: "AI Intent Analysis",
      desc: "Navjeevan AI parses your query, extracts crop/location entities, and queries the dataset.",
      icon: Cpu,
    },
    {
      num: "03",
      title: "Smart Execution",
      desc: "Receive formatted APMC market recommendations, document checklists, and trader contacts.",
      icon: CheckCircle,
    },
    {
      num: "04",
      title: "Continuous Support",
      desc: "Track weather conditions and stay updated on subsidy application statuses.",
      icon: Headphones,
    },
  ];

  return (
    <section id="process" className="py-28 bg-bgSoft relative">
      <div className="max-w-container mx-auto px-6">
        {/* SECTION HEADER */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <span>How Navjeevan AI Works</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText leading-tight">
            Simple 4-Step <span className="text-primary font-serif italic">Process</span>
          </h2>
        </div>

        {/* TIMELINE GRID */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8 relative">
          {steps.map((item, index) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                className="bg-white p-8 rounded-3xl shadow-soft border border-borderColor/60 relative group hover:border-primary/40 transition-all"
              >
                <div className="flex items-center justify-between mb-6">
                  <div className="w-14 h-14 rounded-2xl bg-primary/10 text-primary flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-all">
                    <Icon className="w-7 h-7" />
                  </div>
                  <span className="text-3xl font-extrabold font-serif text-accentYellow/80">{item.num}</span>
                </div>
                <h3 className="text-xl font-bold font-sans text-darkText mb-3">{item.title}</h3>
                <p className="text-grayText text-sm leading-relaxed">{item.desc}</p>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
