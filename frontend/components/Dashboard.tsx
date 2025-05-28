
"use client";

import { useState } from "react";
import { fetchResponse } from "@/lib/api";
import ResultCard from "./ResultCard";
import LoadingSpinner from "./LoadingSpinner";
import { AgentResponse } from "@/types";

export default function Dashboard() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState<AgentResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (query.trim() === "") {
      alert("Please enter a query before asking the agent.");
      return;
    }
    setLoading(true);
    try {
      const res = await fetchResponse(query);
      setResponse(res);
    } catch (err) {
      console.error("API Error", err);
      setResponse(null);
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

        {response && <ResultCard response={response} />}
      </div>
    </div>
  );
}
