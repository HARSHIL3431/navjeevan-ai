import { useState } from "react";
import { motion } from "framer-motion";
import { Phone, Mail, MapPin, Clock, Send, CheckCircle2 } from "lucide-react";

export default function ContactSection() {
  const [formSubmitted, setFormSubmitted] = useState(false);
  const [formData, setFormData] = useState({ name: "", email: "", phone: "", subject: "", message: "" });

  const handleSubmit = (e) => {
    e.preventDefault();
    setFormSubmitted(true);
    setTimeout(() => {
      setFormSubmitted(false);
      setFormData({ name: "", email: "", phone: "", subject: "", message: "" });
    }, 4000);
  };

  return (
    <section id="contact" className="py-28 bg-white relative">
      <div className="max-w-container mx-auto px-6">
        {/* TOP SECTION: HEADER & CONTACT CARDS */}
        <div className="text-center max-w-2xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-semibold uppercase tracking-wider mb-4">
            <span>Get in Touch</span>
          </div>
          <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold font-sans text-darkText leading-tight mb-4">
            We Are Here To <span className="text-primary font-serif italic">Help You</span>
          </h2>
          <p className="text-grayText text-base">
            Reach out to our agricultural support team or visit our office in South Gujarat.
          </p>
        </div>

        {/* 3 CONTACT CARDS */}
        <div className="grid md:grid-cols-3 gap-8 mb-20">
          <div className="p-8 rounded-3xl bg-bgSoft border border-borderColor/60 text-center flex flex-col items-center">
            <div className="w-14 h-14 rounded-2xl bg-primary text-white flex items-center justify-center mb-6 shadow-md">
              <Phone className="w-7 h-7 text-accentYellow" />
            </div>
            <h4 className="text-xl font-bold text-darkText mb-2">Call Us Direct</h4>
            <p className="text-grayText text-sm mb-4">Monday – Saturday (8:00 AM – 6:00 PM)</p>
            <a href="tel:+919876543210" className="text-primary font-bold text-lg hover:underline">+91 98765 43210</a>
          </div>

          <div className="p-8 rounded-3xl bg-bgSoft border border-borderColor/60 text-center flex flex-col items-center">
            <div className="w-14 h-14 rounded-2xl bg-primary text-white flex items-center justify-center mb-6 shadow-md">
              <Mail className="w-7 h-7 text-accentYellow" />
            </div>
            <h4 className="text-xl font-bold text-darkText mb-2">Email Support</h4>
            <p className="text-grayText text-sm mb-4">Send your queries anytime</p>
            <a href="mailto:support@navjeevan-ai.org" className="text-primary font-bold text-lg hover:underline">support@navjeevan-ai.org</a>
          </div>

          <div className="p-8 rounded-3xl bg-bgSoft border border-borderColor/60 text-center flex flex-col items-center">
            <div className="w-14 h-14 rounded-2xl bg-primary text-white flex items-center justify-center mb-6 shadow-md">
              <MapPin className="w-7 h-7 text-accentYellow" />
            </div>
            <h4 className="text-xl font-bold text-darkText mb-2">Visit Our Office</h4>
            <p className="text-grayText text-sm mb-4">APMC Market Complex, Ring Road</p>
            <span className="text-primary font-bold text-lg">Surat, Gujarat 395002</span>
          </div>
        </div>

        {/* BOTTOM SECTION: MAP/HOURS + CONTACT FORM */}
        <div className="grid lg:grid-cols-12 gap-12 items-start">
          {/* LEFT: MAP & BUSINESS HOURS */}
          <div className="lg:col-span-5 space-y-8">
            {/* GOOGLE MAPS EMBED */}
            <div className="rounded-3xl overflow-hidden shadow-soft border border-borderColor/80 h-72">
              <iframe
                title="Surat APMC Location"
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d119066.41709540026!2d72.75225628601614!3d21.161026848135894!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be04e59411d1563%3A0xfe4558290938b042!2sSurat%2C%20Gujarat!5e0!3m2!1sen!2sin!4v1700000000000!5m2!1sen!2sin"
                className="w-full h-full border-0"
                allowFullScreen=""
                loading="lazy"
              />
            </div>

            {/* WORKING HOURS */}
            <div className="p-8 rounded-3xl bg-primary-dark text-white space-y-4">
              <div className="flex items-center gap-3 text-accentYellow">
                <Clock className="w-6 h-6" />
                <h4 className="text-lg font-bold">APMC Mandi Operating Hours</h4>
              </div>
              <div className="space-y-2 text-sm text-white/80 border-t border-white/10 pt-4">
                <div className="flex justify-between">
                  <span>Surat APMC Auction:</span>
                  <span className="font-semibold text-white">6:00 AM – 2:00 PM (Mon–Sat)</span>
                </div>
                <div className="flex justify-between">
                  <span>Navsari APMC Yard:</span>
                  <span className="font-semibold text-white">7:00 AM – 1:00 PM (Mon–Sat)</span>
                </div>
                <div className="flex justify-between">
                  <span>AI Web & Chat Service:</span>
                  <span className="font-semibold text-accentYellow">24/7 Always Active</span>
                </div>
              </div>
            </div>
          </div>

          {/* RIGHT: ROUNDED CONTACT FORM */}
          <div className="lg:col-span-7 bg-bgSoft p-8 sm:p-12 rounded-4xl border border-borderColor/80 shadow-soft">
            <h3 className="text-2xl font-bold font-sans text-darkText mb-2">Send Us a Message</h3>
            <p className="text-grayText text-sm mb-8">Fill out the form below and our agricultural experts will respond within 24 hours.</p>

            {formSubmitted ? (
              <div className="p-8 bg-emerald-50 border border-emerald-200 rounded-3xl text-center space-y-3">
                <CheckCircle2 className="w-12 h-12 text-emerald-600 mx-auto animate-bounce" />
                <h4 className="text-xl font-bold text-emerald-900">Message Sent Successfully!</h4>
                <p className="text-emerald-700 text-sm">Thank you for reaching out. Our team will contact you shortly.</p>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid sm:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-xs font-bold text-darkText uppercase tracking-wider mb-2">Full Name</label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      placeholder="e.g. Rajesh Patel"
                      className="w-full px-5 py-4 rounded-2xl bg-white border border-borderColor focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none text-darkText text-sm transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-darkText uppercase tracking-wider mb-2">Email Address</label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      placeholder="rajesh@example.com"
                      className="w-full px-5 py-4 rounded-2xl bg-white border border-borderColor focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none text-darkText text-sm transition-all"
                    />
                  </div>
                </div>

                <div className="grid sm:grid-cols-2 gap-6">
                  <div>
                    <label className="block text-xs font-bold text-darkText uppercase tracking-wider mb-2">Phone Number</label>
                    <input
                      type="tel"
                      required
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      placeholder="+91 98765 43210"
                      className="w-full px-5 py-4 rounded-2xl bg-white border border-borderColor focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none text-darkText text-sm transition-all"
                    />
                  </div>
                  <div>
                    <label className="block text-xs font-bold text-darkText uppercase tracking-wider mb-2">Subject</label>
                    <input
                      type="text"
                      required
                      value={formData.subject}
                      onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
                      placeholder="Mandi Price Inquiry"
                      className="w-full px-5 py-4 rounded-2xl bg-white border border-borderColor focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none text-darkText text-sm transition-all"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-bold text-darkText uppercase tracking-wider mb-2">Your Message</label>
                  <textarea
                    rows={4}
                    required
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    placeholder="Describe your query regarding mandi prices, schemes, or crop advice..."
                    className="w-full px-5 py-4 rounded-2xl bg-white border border-borderColor focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none text-darkText text-sm transition-all resize-none"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full flex items-center justify-center gap-3 bg-primary hover:bg-primary-dark text-white font-semibold text-base py-4 rounded-full shadow-lg hover:shadow-xl transition-all"
                >
                  <Send className="w-5 h-5" />
                  <span>Send Message Now</span>
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
}
