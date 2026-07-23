import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { X, Send, Sparkles, Sprout, Bot, User, RefreshCw } from "lucide-react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

const SUGGESTED_QUERIES = [
  "Wheat selling price in Surat APMC mandi",
  "PM Kisan scheme eligibility & document list",
  "Kisan Credit Card (KCC) required papers",
  "Cotton traders contact numbers in Surat",
  "Weather forecast & spray risk advice for Surat",
];

export default function AIChatModal({ isOpen, onClose }) {
  const [messages, setMessages] = useState([
    {
      sender: "ai",
      intent: "general",
      text: "Namaste! I am Navjeevan AI — your agricultural assistant for Gujarat. Ask me about APMC mandi prices, government schemes (PM Kisan, KCC, Fasal Bima), trader contacts, or weather advice!"
    }
  ]);
  const [inputQuery, setInputQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const chatBottomRef = useRef(null);

  useEffect(() => {
    if (chatBottomRef.current) {
      chatBottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, loading]);

  if (!isOpen) return null;

  const handleSend = async (queryText) => {
    const q = queryText || inputQuery;
    if (!q.trim() || loading) return;

    setMessages((prev) => [...prev, { sender: "user", text: q }]);
    setInputQuery("");
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: q })
      });

      const data = await res.json();
      const textResponse = data.response || data.data || "Sorry, no response available.";
      const intent = data.intent || "general";

      setMessages((prev) => [...prev, { sender: "ai", intent, text: textResponse }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          intent: "general",
          text: "⚠️ Connection error. Please ensure backend server is running on http://127.0.0.1:8000."
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-darkText/60 backdrop-blur-sm">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="bg-white w-full max-w-3xl rounded-4xl shadow-2xl overflow-hidden flex flex-col h-[680px] max-h-[90vh] border border-borderColor"
        >
          {/* MODAL HEADER */}
          <div className="bg-primary text-white p-6 flex items-center justify-between shadow-md">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-white/20 text-accentYellow flex items-center justify-center">
                <Sprout className="w-6 h-6" />
              </div>
              <div>
                <h3 className="font-bold text-lg font-sans flex items-center gap-2">
                  Navjeevan AI Assistant
                  <Sparkles className="w-4 h-4 text-accentYellow animate-pulse" />
                </h3>
                <p className="text-xs text-white/80">Gujarat Agriculture & APMC Market Intelligence</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-full hover:bg-white/10 text-white/80 hover:text-white transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* CHAT MESSAGES VIEWPORT */}
          <div className="flex-1 p-6 overflow-y-auto bg-bgSoft space-y-4">
            {messages.map((msg, idx) => (
              <div
                key={idx}
                className={`flex gap-3 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                {msg.sender === "ai" && (
                  <div className="w-9 h-9 rounded-full bg-primary text-white flex items-center justify-center flex-shrink-0 text-sm">
                    <Bot className="w-5 h-5 text-accentYellow" />
                  </div>
                )}

                <div
                  className={`max-w-[80%] p-4 rounded-2xl text-sm leading-relaxed ${
                    msg.sender === "user"
                      ? "bg-primary text-white rounded-br-none shadow-md font-medium"
                      : "bg-white text-darkText border border-borderColor/80 shadow-soft rounded-bl-none"
                  }`}
                >
                  {msg.sender === "ai" && msg.intent && (
                    <span className="inline-block px-2.5 py-0.5 rounded-full bg-primary/10 text-primary text-[10px] font-bold uppercase tracking-wider mb-2">
                      {msg.intent}
                    </span>
                  )}
                  <div className="whitespace-pre-wrap">{msg.text}</div>
                </div>

                {msg.sender === "user" && (
                  <div className="w-9 h-9 rounded-full bg-accentYellow text-darkText font-bold flex items-center justify-center flex-shrink-0 text-sm">
                    <User className="w-5 h-5" />
                  </div>
                )}
              </div>
            ))}

            {loading && (
              <div className="flex gap-3 items-center text-grayText text-xs italic bg-white p-3 rounded-2xl border border-borderColor max-w-xs">
                <RefreshCw className="w-4 h-4 animate-spin text-primary" />
                <span>Querying APMC dataset & AI model...</span>
              </div>
            )}
            <div ref={chatBottomRef} />
          </div>

          {/* SUGGESTED PRESET CHIPS */}
          <div className="px-6 py-2 bg-white border-t border-borderColor flex gap-2 overflow-x-auto no-scrollbar">
            {SUGGESTED_QUERIES.map((sq, i) => (
              <button
                key={i}
                onClick={() => handleSend(sq)}
                className="px-3 py-1.5 rounded-full bg-bgSoft hover:bg-primary/10 text-primary border border-borderColor text-xs font-medium whitespace-nowrap transition-colors flex-shrink-0"
              >
                {sq}
              </button>
            ))}
          </div>

          {/* INPUT FORM */}
          <div className="p-4 bg-white border-t border-borderColor">
            <form
              onSubmit={(e) => {
                e.preventDefault();
                handleSend();
              }}
              className="flex items-center gap-3 bg-bgSoft p-2 rounded-full border border-borderColor focus-within:border-primary transition-all"
            >
              <input
                type="text"
                value={inputQuery}
                onChange={(e) => setInputQuery(e.target.value)}
                placeholder="Ask about wheat prices, PM Kisan, traders, documents..."
                className="flex-1 bg-transparent px-4 py-2 text-sm text-darkText outline-none"
              />
              <button
                type="submit"
                disabled={loading || !inputQuery.trim()}
                className="w-10 h-10 rounded-full bg-primary hover:bg-primary-dark text-white flex items-center justify-center disabled:opacity-50 transition-all shadow-md"
              >
                <Send className="w-4 h-4" />
              </button>
            </form>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
