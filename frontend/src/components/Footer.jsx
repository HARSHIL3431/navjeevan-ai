import { Sprout, Mail, Phone, MapPin, Send } from "lucide-react";

export default function Footer() {
  return (
    <footer className="bg-primary-dark text-white pt-24 pb-12 border-t border-white/10">
      <div className="max-w-container mx-auto px-6">
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
          {/* COLUMN 1: COMPANY */}
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-10 h-10 rounded-xl bg-primary text-white flex items-center justify-center shadow-md">
                <Sprout className="w-6 h-6 text-accentYellow" />
              </div>
              <span className="text-xl font-bold font-sans text-white">
                Navjeevan <span className="text-lightGreen">AI</span>
              </span>
            </div>
            <p className="text-white/70 text-sm leading-relaxed mb-6 font-light">
              AI-powered agricultural platform empowering Gujarat farmers with real-time APMC mandi prices, trader directories, and welfare scheme support.
            </p>
            <div className="text-xs text-white/50">
              © {new Date().getFullYear()} Navjeevan AI. All Rights Reserved.
            </div>
          </div>

          {/* COLUMN 2: QUICK LINKS */}
          <div>
            <h4 className="text-lg font-bold font-sans text-accentYellow mb-6">Quick Links</h4>
            <ul className="space-y-3 text-sm text-white/80">
              <li><a href="#home" className="hover:text-lightGreen transition-colors">Home</a></li>
              <li><a href="#about" className="hover:text-lightGreen transition-colors">About Us</a></li>
              <li><a href="#services" className="hover:text-lightGreen transition-colors">Services</a></li>
              <li><a href="#process" className="hover:text-lightGreen transition-colors">How It Works</a></li>
              <li><a href="#projects" className="hover:text-lightGreen transition-colors">Projects & Gallery</a></li>
              <li><a href="#contact" className="hover:text-lightGreen transition-colors">Contact Us</a></li>
            </ul>
          </div>

          {/* COLUMN 3: SERVICES */}
          <div>
            <h4 className="text-lg font-bold font-sans text-accentYellow mb-6">Services</h4>
            <ul className="space-y-3 text-sm text-white/80">
              <li>APMC Mandi Price Optimizer</li>
              <li>Weather & Spray Advisor</li>
              <li>PM Kisan Scheme Checklist</li>
              <li>Kisan Credit Card (KCC) Support</li>
              <li>Verified Trader Directory</li>
            </ul>
          </div>

          {/* COLUMN 4: NEWSLETTER */}
          <div>
            <h4 className="text-lg font-bold font-sans text-accentYellow mb-6">Stay Updated</h4>
            <p className="text-white/70 text-sm mb-4">Subscribe to receive daily APMC market price alerts and weather updates.</p>
            <form onSubmit={(e) => e.preventDefault()} className="space-y-3">
              <div className="relative">
                <input
                  type="email"
                  placeholder="Enter your email"
                  className="w-full px-4 py-3 rounded-full bg-white/10 border border-white/20 text-white placeholder-white/50 text-sm outline-none focus:border-accentYellow"
                />
                <button
                  type="submit"
                  className="absolute right-1 top-1 bottom-1 px-4 rounded-full bg-accentYellow text-darkText font-bold text-xs hover:bg-yellow-400 transition-all flex items-center justify-center"
                >
                  <Send className="w-4 h-4" />
                </button>
              </div>
            </form>
          </div>
        </div>

        {/* BOTTOM COPYRIGHT */}
        <div className="pt-8 border-t border-white/10 text-center text-xs text-white/50 flex flex-wrap justify-between items-center gap-4">
          <div>Built for Farmers in Gujarat, India 🌾</div>
          <div className="flex gap-6">
            <a href="#privacy" className="hover:text-white transition-colors">Privacy Policy</a>
            <a href="#terms" className="hover:text-white transition-colors">Terms of Service</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
