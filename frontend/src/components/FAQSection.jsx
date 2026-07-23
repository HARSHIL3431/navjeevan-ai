import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, HelpCircle } from "lucide-react";

export default function FAQSection() {
  const [openIndex, setOpenIndex] = useState(0);

  const faqs = [
    {
      q: "How does Navjeevan AI fetch market prices for Gujarat mandis?",
      a: "Navjeevan AI connects directly to APMC market dataset records and government price feeds to provide current auction prices for wheat, cotton, groundnut, and paddy in Surat, Navsari, Bardoli, and Anand."
    },
    {
      q: "Is Navjeevan AI free for farmers in Gujarat?",
      a: "Yes, Navjeevan AI is completely free to use for all farmers, cooperative workers, and agricultural extension agents."
    },
    {
      q: "Which government welfare schemes are covered?",
      a: "Our AI database includes PM Kisan Samman Nidhi, PM Fasal Bima Yojana (Crop Insurance), Kisan Credit Card (KCC), Gujarat State Soil Health Card, and solar pump subsidy programs."
    },
    {
      q: "How can I verify licensed cotton and grain traders?",
      a: "Type 'cotton traders in Surat' or 'grain buyers in Navsari' into the AI Assistant to view licensed trader names, verified phone numbers, and WhatsApp contacts."
    },
  ];

  return (
    <section className="py-28 bg-white">
      <div className="max-w-container mx-auto px-6 max-w-4xl">
        {/* SECTION HEADER */}
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <HelpCircle className="w-4 h-4" />
            <span>Frequently Asked Questions</span>
          </div>
          <h2 className="text-3xl sm:text-4xl font-bold font-sans text-darkText">
            Got Questions? We Have <span className="text-primary font-serif italic">Answers</span>
          </h2>
        </div>

        {/* ACCORDION CARDS */}
        <div className="space-y-4">
          {faqs.map((item, index) => (
            <div
              key={index}
              className="border border-borderColor/80 rounded-2xl overflow-hidden bg-bgSoft transition-all"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? -1 : index)}
                className="w-full p-6 text-left flex items-center justify-between gap-4 font-bold text-darkText text-lg hover:text-primary transition-colors"
              >
                <span>{item.q}</span>
                <ChevronDown
                  className={`w-5 h-5 text-primary transition-transform duration-300 ${
                    openIndex === index ? "rotate-180" : ""
                  }`}
                />
              </button>
              <AnimatePresence>
                {openIndex === index && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="overflow-hidden"
                  >
                    <div className="px-6 pb-6 text-grayText text-sm leading-relaxed border-t border-gray-200/60 pt-4">
                      {item.a}
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
