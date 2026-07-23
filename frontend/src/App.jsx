import { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import Features from "./components/Features";
import WeatherWidget from "./components/WeatherWidget";
import AboutSection from "./components/AboutSection";
import ServicesSection from "./components/ServicesSection";
import WhyChooseUs from "./components/WhyChooseUs";
import ProcessTimeline from "./components/ProcessTimeline";
import StatsCounter from "./components/StatsCounter";
import GalleryProjects from "./components/GalleryProjects";
import Testimonials from "./components/Testimonials";
import FAQSection from "./components/FAQSection";
import BlogSection from "./components/BlogSection";
import ContactSection from "./components/ContactSection";
import CTASection from "./components/CTASection";
import Footer from "./components/Footer";
import AIChatModal from "./components/AIChatModal";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export default function App() {
  const [chatOpen, setChatOpen] = useState(false);
  const [weather, setWeather] = useState({ temp: "29°C", condition: "Partly Cloudy", city: "Surat" });

  useEffect(() => {
    fetch(`${API_BASE}/api/v1/weather?location=Surat`)
      .then((res) => res.json())
      .then((resData) => {
        const data = resData.data;
        if (data && data.temp_c !== undefined) {
          setWeather({
            temp: `${data.temp_c}°C`,
            condition: data.humidity_percent ? `Humidity ${data.humidity_percent}%` : "Partly Cloudy",
            city: data.location || "Surat",
          });
        }
      })
      .catch(() => {
        setWeather({ temp: "27°C", condition: "Monsoon Showers", city: "Surat" });
      });
  }, []);

  return (
    <div className="min-h-screen bg-bgSoft font-sans text-darkText selection:bg-accentYellow selection:text-darkText">
      {/* NAVBAR */}
      <Navbar onOpenChat={() => setChatOpen(true)} weather={weather} />

      {/* HERO SECTION */}
      <Hero onOpenChat={() => setChatOpen(true)} />

      {/* FEATURES SECTION */}
      <Features />

      {/* LIVE WEATHER DETECTION WIDGET */}
      <WeatherWidget />

      {/* ABOUT SECTION */}
      <AboutSection onOpenChat={() => setChatOpen(true)} />


      {/* SERVICES SECTION */}
      <ServicesSection onOpenChat={() => setChatOpen(true)} />

      {/* WHY CHOOSE US */}
      <WhyChooseUs />

      {/* PROCESS TIMELINE */}
      <ProcessTimeline />

      {/* STATS COUNTER */}
      <StatsCounter />

      {/* GALLERY / PROJECTS */}
      <GalleryProjects />

      {/* TESTIMONIALS */}
      <Testimonials />

      {/* FAQ SECTION */}
      <FAQSection />

      {/* BLOG SECTION */}
      <BlogSection />

      {/* CONTACT SECTION */}
      <ContactSection />

      {/* CTA BANNER */}
      <CTASection onOpenChat={() => setChatOpen(true)} />

      {/* FOOTER */}
      <Footer />

      {/* AI CHAT ASSISTANT MODAL */}
      <AIChatModal isOpen={chatOpen} onClose={() => setChatOpen(false)} />
    </div>
  );
}
