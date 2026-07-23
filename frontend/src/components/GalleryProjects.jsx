import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";

export default function GalleryProjects() {
  const [activeTab, setActiveTab] = useState("All");

  const categories = ["All", "Markets", "Crops", "Schemes"];

  const projects = [
    {
      title: "Surat APMC Grain Mandi",
      category: "Markets",
      image: "https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?auto=format&fit=crop&w=800&q=80",
    },
    {
      title: "Golden Wheat Harvest South Gujarat",
      category: "Crops",
      image: "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80",
    },
    {
      title: "PM-KISAN Direct Benefit Transfer",
      category: "Schemes",
      image: "https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=800&q=80",
    },
    {
      title: "Navsari Organic Groundnut Fields",
      category: "Crops",
      image: "https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&w=800&q=80",
    },
    {
      title: "Bardoli Cotton Auction Yard",
      category: "Markets",
      image: "https://images.unsplash.com/photo-1574943320219-553eb213f72d?auto=format&fit=crop&w=800&q=80",
    },
    {
      title: "Kisan Credit Card Verification",
      category: "Schemes",
      image: "https://images.unsplash.com/photo-1618042164219-62c820f10723?auto=format&fit=crop&w=800&q=80",
    },
  ];

  const filtered = activeTab === "All" ? projects : projects.filter((p) => p.category === activeTab);

  return (
    <section id="projects" className="py-28 bg-white">
      <div className="max-w-container mx-auto px-6">
        {/* SECTION HEADER */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <span>Agricultural Showcase</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText leading-tight">
            Our Impact Across <span className="text-primary font-serif italic">Gujarat</span>
          </h2>
        </div>

        {/* TABS FILTER */}
        <div className="flex flex-wrap justify-center gap-3 mb-12">
          {categories.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-6 py-2.5 rounded-full text-sm font-medium transition-all ${
                activeTab === tab
                  ? "bg-primary text-white shadow-md"
                  : "bg-bgSoft text-grayText hover:text-darkText hover:bg-gray-200"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* MASONRY GALLERY GRID */}
        <motion.div layout className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          <AnimatePresence>
            {filtered.map((item, index) => (
              <motion.div
                key={item.title}
                layout
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                exit={{ opacity: 0, scale: 0.9 }}
                transition={{ duration: 0.4 }}
                className="relative rounded-3xl overflow-hidden shadow-soft group h-72"
              >
                <img
                  src={item.image}
                  alt={item.title}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-darkText/90 via-darkText/30 to-transparent opacity-80 group-hover:opacity-95 transition-opacity" />
                <div className="absolute bottom-6 left-6 right-6 text-white">
                  <span className="inline-block px-3 py-1 bg-accentYellow text-darkText text-xs font-bold rounded-full mb-2 uppercase tracking-wider">
                    {item.category}
                  </span>
                  <h3 className="text-lg font-bold font-sans">{item.title}</h3>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>
        </motion.div>
      </div>
    </section>
  );
}
