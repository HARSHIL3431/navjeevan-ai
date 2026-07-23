import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Sprout, Menu, X, CloudSun, Sparkles } from "lucide-react";

export default function Navbar({ onOpenChat, weather }) {
  const [scrolled, setScrolled] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 30);
    };
    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const navLinks = [
    { name: "Home", href: "#home" },
    { name: "About", href: "#about" },
    { name: "Services", href: "#services" },
    { name: "Weather Detection", href: "#weather" },
    { name: "Process", href: "#process" },
    { name: "Projects", href: "#projects" },
    { name: "Blog", href: "#blog" },
    { name: "Contact", href: "#contact" },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-white/95 backdrop-blur-md shadow-soft py-3 border-b border-borderColor"
          : "bg-transparent py-5"
      }`}
    >
      <div className="max-w-container mx-auto px-6 flex items-center justify-between">
        {/* LOGO */}
        <a href="#home" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center shadow-md transform group-hover:rotate-6 transition-transform">
            <Sprout className="w-6 h-6 text-accentYellow" />
          </div>
          <div>
            <span
              className={`text-xl font-bold font-sans tracking-tight transition-colors ${
                scrolled ? "text-darkText" : "text-white"
              }`}
            >
              Navjeevan <span className="text-lightGreen">AI</span>
            </span>
            <span className="block text-[10px] uppercase tracking-widest text-accentYellow font-semibold">
              Agri Intelligence
            </span>
          </div>
        </a>

        {/* DESKTOP NAV LINKS */}
        <nav className="hidden lg:flex items-center gap-6">
          {navLinks.map((link) => (
            <a
              key={link.name}
              href={link.href}
              className={`text-sm font-medium transition-colors relative hover:text-lightGreen group ${
                scrolled ? "text-darkText" : "text-white/90"
              }`}
            >
              {link.name}
              <span className="absolute left-0 bottom-[-4px] w-0 h-[2px] bg-accentYellow transition-all duration-300 group-hover:w-full" />
            </a>
          ))}
        </nav>

        {/* RIGHT ACTION BUTTONS */}
        <div className="hidden lg:flex items-center gap-3">
          <a
            href="#weather"
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-xs font-bold transition-all ${
              scrolled
                ? "bg-primary/10 border border-primary/20 text-primary hover:bg-primary hover:text-white"
                : "bg-white/20 border border-white/30 text-white hover:bg-white hover:text-primary-dark"
            }`}
          >
            <CloudSun className="w-4 h-4 text-accentYellow" />
            <span>Weather Detection: {weather ? weather.temp : "Live"}</span>
          </a>

          <button
            onClick={onOpenChat}
            className="flex items-center gap-2 bg-gradient-to-r from-primary to-primary-dark hover:from-primary-dark hover:to-primary text-white font-medium text-sm px-5 py-2.5 rounded-full shadow-md hover:shadow-lg transition-all transform hover:-translate-y-0.5"
          >
            <Sparkles className="w-4 h-4 text-accentYellow animate-pulse" />
            <span>Ask AI Assistant</span>
          </button>
        </div>


        {/* MOBILE MENU TOGGLE */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className={`lg:hidden p-2 rounded-lg ${
            scrolled ? "text-darkText" : "text-white"
          }`}
          aria-label="Toggle menu"
        >
          {mobileMenuOpen ? <X className="w-7 h-7" /> : <Menu className="w-7 h-7" />}
        </button>
      </div>

      {/* MOBILE MENU DRAWER */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, x: "100%" }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: "100%" }}
            transition={{ type: "tween", duration: 0.3 }}
            className="fixed inset-y-0 right-0 w-80 bg-white shadow-2xl z-50 p-6 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-8 pb-4 border-b border-borderColor">
                <div className="flex items-center gap-2">
                  <Sprout className="w-6 h-6 text-primary" />
                  <span className="font-bold text-lg text-darkText">Navjeevan AI</span>
                </div>
                <button
                  onClick={() => setMobileMenuOpen(false)}
                  className="p-1 rounded-lg text-grayText hover:text-darkText"
                >
                  <X className="w-6 h-6" />
                </button>
              </div>

              <div className="flex flex-col gap-4">
                {navLinks.map((link) => (
                  <a
                    key={link.name}
                    href={link.href}
                    onClick={() => setMobileMenuOpen(false)}
                    className="text-base font-medium text-darkText hover:text-primary py-2 border-b border-gray-100"
                  >
                    {link.name}
                  </a>
                ))}
              </div>
            </div>

            <div className="pt-6 border-t border-borderColor">
              <button
                onClick={() => {
                  setMobileMenuOpen(false);
                  onOpenChat();
                }}
                className="w-full flex items-center justify-center gap-2 bg-primary hover:bg-primary-dark text-white font-semibold py-3 rounded-full shadow-md"
              >
                <Sparkles className="w-4 h-4 text-accentYellow" />
                <span>Launch AI Assistant</span>
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
