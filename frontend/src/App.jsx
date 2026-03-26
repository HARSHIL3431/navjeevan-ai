import { useState } from "react";

const API_BASE = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";

export default function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("Ask your farming question to get started.");
  const [loading, setLoading] = useState(false);

  const onSubmit = async (event) => {
    event.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    try {
      const result = await fetch(`${API_BASE}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query })
      });

      let json = {};
      try {
        json = await result.json();
      } catch (error) {
        json = {};
      }

      if (!result.ok) {
        setResponse(json.message || "Request failed. Please try again.");
        return;
      }

      if (json.status === "error") {
        setResponse(json.message || "Something went wrong.");
        return;
      }

      setResponse(json.data || json.response || "No response returned.");
    } catch (error) {
      setResponse("Backend unavailable. Start API with: uvicorn backend.main:app --reload");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={{ maxWidth: 880, margin: "32px auto", padding: "0 16px", fontFamily: "system-ui, sans-serif" }}>
      <h1>Navjeevan AI</h1>
      <p>FastAPI + React architecture ready.</p>
      <form onSubmit={onSubmit} style={{ display: "flex", gap: 10, marginTop: 16 }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g. Compare wheat prices in Surat and Navsari"
          style={{ flex: 1, padding: 10 }}
        />
        <button type="submit" disabled={loading}>{loading ? "Sending..." : "Send"}</button>
      </form>
      <section style={{ marginTop: 20, padding: 14, border: "1px solid #ddd", borderRadius: 8, whiteSpace: "pre-wrap" }}>
        {response}
      </section>
    </main>
  );
}
