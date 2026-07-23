import { motion } from "framer-motion";
import { TrendingUp, CloudSun, FileText, PhoneCall, Building2, ShieldAlert, ArrowUpRight } from "lucide-react";

export default function ServicesSection({ onOpenChat }) {
  const services = [
    {
      icon: TrendingUp,
      title: "APMC Market Price Optimizer",
      desc: "Compare live bidding rates for wheat, cotton, and groundnut across Surat, Navsari, Bardoli, and Anand mandis.",
      image: "https://images.unsplash.com/photo-1574943320219-553eb213f72d?auto=format&fit=crop&w=800&q=80",
    },
    {
      icon: CloudSun,
      title: "Weather Risk & Spray Advisor",
      desc: "Real-time weather tracking with OpenWeatherMap & Open-Meteo fallbacks to optimize pesticide and fertilizer spraying schedule.",
      image: "https://images.unsplash.com/photo-1534274988757-a28bf1a57c17?auto=format&fit=crop&w=800&q=80",
    },
    {
      icon: FileText,
      title: "Govt Schemes & Subsidies",
      desc: "Instant guidance and eligibility checks for PM Kisan Samman Nidhi, PM Fasal Bima Yojana, and Kisan Credit Card (KCC).",
      image: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
    },
    {
      icon: PhoneCall,
      title: "Direct Licensed Trader Directory",
      desc: "Get verified contact details and direct WhatsApp numbers for cotton, grain, and groundnut buyers in South Gujarat.",
      image: "https://images.unsplash.com/photo-1560472355-536de3962603?auto=format&fit=crop&w=800&q=80",
    },
    {
      icon: Building2,
      title: "Mandi Timing & Operating Info",
      desc: "Full auction schedules, code details, and helpline numbers for all major APMC markets across Gujarat.",
      image: "https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&w=800&q=80",
    },
    {
      icon: ShieldAlert,
      title: "Document Verification Checklist",
      desc: "Complete list of required 7/12 land records, Aadhaar proof, and bank documents for loan & subsidy processing.",
      image: "https://images.unsplash.com/photo-1618042164219-62c820f10723?auto=format&fit=crop&w=800&q=80",
    },
  ];

  return (
    <section id="services" className="py-28 bg-bgSoft relative">
      <div className="max-w-container mx-auto px-6">
        {/* SECTION HEADER */}
        <div className="text-center max-w-2xl mx-auto mb-20">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <span>Our AI Core Services</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText leading-tight">
            Comprehensive Agriculture <span className="text-primary font-serif italic">Solutions</span>
          </h2>
        </div>

        {/* SERVICES GRID */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {services.map((item, index) => {
            const Icon = item.icon;
            return (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white rounded-3xl overflow-hidden shadow-soft hover:shadow-cardHover border border-borderColor/60 transition-all duration-500 group flex flex-col justify-between"
              >
                <div>
                  {/* IMAGE WRAPPER */}
                  <div className="relative h-56 overflow-hidden">
                    <img
                      src={item.image}
                      alt={item.title}
                      className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                    />
                    <div className="absolute top-4 right-4 w-12 h-12 rounded-2xl bg-white/90 backdrop-blur-md text-primary flex items-center justify-center shadow-md">
                      <Icon className="w-6 h-6" />
                    </div>
                  </div>

                  {/* CONTENT */}
                  <div className="p-8">
                    <h3 className="text-xl font-bold font-sans text-darkText mb-3 group-hover:text-primary transition-colors">
                      {item.title}
                    </h3>
                    <p className="text-grayText text-sm leading-relaxed mb-6">
                      {item.desc}
                    </p>
                  </div>
                </div>

                {/* BOTTOM ACTION */}
                <div className="px-8 pb-8">
                  <button
                    onClick={onOpenChat}
                    className="w-full flex items-center justify-between text-sm font-semibold text-primary group-hover:text-primary-dark border-t border-gray-100 pt-4"
                  >
                    <span>Consult AI Assistant</span>
                    <div className="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center group-hover:bg-primary group-hover:text-white transition-all">
                      <ArrowUpRight className="w-4 h-4" />
                    </div>
                  </button>
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
