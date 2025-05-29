"use client";

import { useState } from "react";
import { fetchResponse } from "@/lib/api";
import ResultCard from "./ResultCard";
import LoadingSpinner from "./LoadingSpinner";
import { AgentResponse } from "@/types";

type QA = {
  query: string;
  response: AgentResponse | null;
};

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [history, setHistory] = useState<QA[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (query.trim() === "") {
      alert("Please enter a query before asking the agent.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetchResponse(query);
      // Prepend the new result to history (newest at top)
      setHistory(prev => [{ query, response: res }, ...prev]);
      setQuery(""); // Optionally clear input after submit
    } catch (err) {
      console.error("API Error", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-50 via-white to-indigo-50 p-8 font-sans text-gray-900 flex justify-center items-start">
      <div className="max-w-4xl w-full space-y-8">

        <h1 className="text-4xl font-serif font-bold text-indigo-700 text-center tracking-wide drop-shadow-sm select-none">
          AI Operating Officer
        </h1>

        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="e.g., What does Satya think about cloud migration?"
          rows={5}
          className="w-full p-5 border border-gray-300 rounded-3xl focus:outline-none focus:ring-4 focus:ring-indigo-400 resize-none text-lg leading-relaxed shadow-md transition"
          disabled={loading}
        />

        <button
          onClick={handleSubmit}
          disabled={loading || query.trim() === ""}
          className={`w-full py-3 rounded-3xl font-semibold text-white shadow-md transition
            ${loading || query.trim() === "" ? "bg-indigo-300 cursor-not-allowed" : "bg-indigo-600 hover:bg-indigo-700"}`}
        >
          {loading ? "Loading..." : "Ask Agent"}
        </button>

        {loading && <LoadingSpinner />}

        {/* Render each result, newest first */}
        {history.map((qa, idx) => (
          <div key={idx} className="mt-8">
            <div className="mb-2 text-indigo-900 font-semibold text-lg">
              Q{history.length - idx}: {qa.query}
            </div>
            {qa.response && <ResultCard response={qa.response} />}
          </div>
        ))}

      </div>
    </div>
  );
}
