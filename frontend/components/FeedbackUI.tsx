import React, { useState } from "react";
import { sendFeedback, FeedbackRequest, FeedbackResponse } from "@/lib/api";

interface FeedbackUIProps {
  responseText: string;
  reasoningChain: string[];
  retrievedChunks: string[];
}

export default function FeedbackUI({
  responseText,
  reasoningChain,
  retrievedChunks,
}: FeedbackUIProps) {
  const [feedback, setFeedback] = useState<"accept" | "retry" | "reject" | null>(null);
  const [autoScore, setAutoScore] = useState<number | null>(null);
  const [fineTuneTriggered, setFineTuneTriggered] = useState<boolean>(false);

  const handleFeedback = async (type: "accept" | "retry" | "reject") => {
    setFeedback(type);
    const req: FeedbackRequest = {
      response: responseText,
      chunks: retrievedChunks,
      feedback: type,
    };
    const res: FeedbackResponse = await sendFeedback(req);
    setAutoScore(res.score);
    setFineTuneTriggered(res.fine_tune_triggered);
  };

  return (
    <>
    {/* Reasoning Chain */}
      <div className="bg-white rounded-3xl shadow-2xl p-6 mb-6 relative overflow-hidden">
        <div className="absolute -top-4 left-4 w-20 h-1 rounded-full bg-gradient-to-r from-purple-400 to-pink-500 animate-gradient-x"></div>
        <h4 className="text-xl font-semibold mb-4 text-purple-700 flex items-center gap-2">
          Agent Reasoning
        </h4>
        <ul className="list-disc list-inside space-y-4 text-purple-700 text-lg">
          {reasoningChain.length > 0 ? (
            reasoningChain.map((step, idx) => (
              <li key={idx} className="cursor-default transition-colors hover:text-purple-500">
                {step}
              </li>
            ))
          ) : (
            <li>No reasoning available.</li>
          )}
        </ul>
      </div>
      {/* Feedback Buttons */}
      <div className="flex items-center justify-center gap-3 mb-6">
        <button
          onClick={() => handleFeedback("accept")}
          className={`flex items-center justify-center gap-2 py-3 px-6 rounded-3xl font-semibold shadow-md transition-transform hover:scale-105
            ${feedback === "accept" ? "bg-green-500 text-white" : "bg-gray-200 text-gray-600"}`}
          title="Accept this response"
        >
          ✅ Accept
        </button>
        <button
          onClick={() => handleFeedback("retry")}
          className={`flex items-center justify-center gap-2 py-3 px-6 rounded-3xl font-semibold shadow-md transition-transform hover:scale-105
            ${feedback === "retry" ? "bg-yellow-400 text-white" : "bg-gray-200 text-gray-600"}`}
          title="Retry with refined chunks"
        >
          🔄 Retry
        </button>
        <button
          onClick={() => handleFeedback("reject")}
          className={`flex items-center justify-center gap-2 py-3 px-6 rounded-3xl font-semibold shadow-md transition-transform hover:scale-105
            ${feedback === "reject" ? "bg-red-500 text-white" : "bg-gray-200 text-gray-600"}`}
          title="Reject this response"
        >
          ❌ Reject
        </button>
      </div>

      {/* Auto-score & Fine-tune Notice */}
      {autoScore !== null && (
        <div className="p-4 bg-white rounded-lg border border-gray-200 shadow-sm mb-4">
          <strong>Auto-score:</strong> {autoScore.toFixed(2)}
        </div>
      )}
      {fineTuneTriggered && (
        <div className="p-4 bg-red-50 text-red-700 rounded-lg border border-red-200 shadow-sm">
          Score below threshold. Retrieval fine-tuning triggered.
        </div>
      )}
    </>
  );
}
