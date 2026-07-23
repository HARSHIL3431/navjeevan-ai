import { motion } from "framer-motion";
import { Sparkles, ArrowRight } from "lucide-react";

export default function CTASection({ onOpenChat }) {
  return (
    <section className="py-20 bg-white relative">
      <div className="max-w-container mx-auto px-6">
        <div className="relative rounded-5xl bg-gradient-to-r from-primary-dark via-primary to-primary-dark p-12 sm:p-20 text-white overflow-hidden shadow-2xl text-center">
          {/* FLOATING DECORATIVE GLOWS */}
          <div className="absolute top-0 right-0 w-96 h-96 bg-accentYellow/20 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-lightGreen/20 rounded-full blur-3xl" />

          <div className="relative z-10 max-w-3xl mx-auto">
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-accentYellow text-xs font-semibold uppercase tracking-wider mb-6">
              <Sparkles className="w-4 h-4" />
              <span>Transform Your Agriculture Today</span>
            </div>

            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans mb-6 leading-tight">
              Ready to Get Real-Time APMC Mandi Prices & AI Crop Advice?
            </h2>

            <p className="text-white/80 text-lg mb-10 font-light">
              Join over 10,000 farmers in Gujarat who rely on Navjeevan AI for transparent market pricing, scheme guidance, and direct trader contacts.
            </p>

            <button
              onClick={onOpenChat}
              className="inline-flex items-center gap-3 bg-accentYellow hover:bg-yellow-400 text-darkText font-bold text-lg px-10 py-5 rounded-full shadow-xl hover:shadow-2xl transition-all transform hover:-translate-y-1"
            >
              <span>Launch AI Assistant Now</span>
              <ArrowRight className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}
