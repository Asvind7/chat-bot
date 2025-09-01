import { useEffect, useRef, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000/ask";

function Message({ role, content, card }) {
  const isUser = role === "user";
  return (
    <div className={`w-full flex ${isUser ? "justify-end" : "justify-start"} mb-3`}>
      <div className={`max-w-[85%] rounded-2xl px-4 py-3 shadow ${isUser ? "bg-blue-600 text-white" : "bg-white border border-gray-200"}`}>
        <div className="whitespace-pre-wrap leading-relaxed">{content}</div>
        {card && (
          <div className="mt-3 flex items-start gap-3">
            {card.image_url && (
              <img src={card.image_url} alt={card.title} className="w-16 h-16 object-cover rounded-xl border" />
            )}
            <div>
              <div className="font-semibold">{card.title}</div>
              {card.subtitle && <div className="text-sm text-gray-600">{card.subtitle}</div>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function App() {
  const [input, setInput] = useState("");
  const [msgs, setMsgs] = useState([
    { role: "assistant", content: "Ahoy! Ask me anything about the Straw Hat Pirates ⚓" }
  ]);
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs, loading]);

  const send = async () => {
    const text = input.trim();
    if (!text) return;
    setMsgs((m) => [...m, { role: "user", content: text }]);
    setInput("");
    setLoading(true);
    try {
      const res = await axios.get(API, { params: { q: text } });
      console.log(res.data); // <-- inspect this in browser console
      let { text: answer, card } = res.data;
      if (typeof answer === "object") {
        // If backend wraps text inside an object
        answer = answer.text || JSON.stringify(answer);
        card = answer.card || card;
      }
      setMsgs((m) => [...m, { role: "assistant", content: answer || "…" , card }]);
    } catch (e) {
      setMsgs((m) => [...m, { role: "assistant", content: "Connection error. Is the backend running on 127.0.0.1:8000?" }]);
    } finally {
      setLoading(false);
    }
  };
  
  const onKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  };

  return (
    <div className="h-dvh flex flex-col">
      {/* Header */}
      <header className="sticky top-0 z-10 bg-white border-b border-gray-200">
        <div className="max-w-3xl mx-auto px-4 py-3 flex items-center gap-3">
          <div className="text-2xl">☀️</div>
          <div>
            <div className="font-semibold">Straw Hat Chat</div>
            <div className="text-xs text-gray-500">Local knowledge • Light theme</div>
          </div>
        </div>
      </header>

      {/* Chat */}
      <main className="flex-1 overflow-y-auto">
        <div className="max-w-3xl mx-auto px-4 py-4">
          {msgs.map((m, i) => (
            <Message key={i} role={m.role} content={m.content} card={m.card} />
          ))}
          {loading && (
            <div className="w-full flex justify-start mb-3">
              <div className="bg-white border border-gray-200 rounded-2xl px-4 py-3 shadow">
                <span className="inline-flex gap-1">
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:120ms]"></span>
                  <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:240ms]"></span>
                </span>
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </main>

      {/* Composer */}
      <footer className="sticky bottom-0 bg-white border-t border-gray-200">
        <div className="max-w-3xl mx-auto px-4 py-3">
          <div className="flex items-end gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={onKey}
              placeholder="Ask about Luffy, Zoro, the helmsman, or a Devil Fruit..."
              className="flex-1 resize-none rounded-2xl border border-gray-300 px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              rows={1}
            />
            <button
              onClick={send}
              className="shrink-0 rounded-2xl bg-blue-600 text-white px-4 py-3 font-medium hover:bg-blue-700 disabled:opacity-50"
              disabled={loading}
            >
              Send
            </button>
          </div>
          <div className="text-[10px] text-black-500 mt-2">
            Tip: try “Who is the helmsman?”, “What is Luffy’s Devil Fruit?”, or “Thousand Sunny”.
          </div>
        </div>
      </footer>
    </div>
  );
}
