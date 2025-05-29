import { AgentResponse } from "@/types";
import ActionsRow from "@/components/ActionButtons";
import FeedbackUI from "@/components/FeedbackUI";

export default function ResultCard({ response }: { response: AgentResponse }) {
  return (
    <div className="max-w-4xl mx-auto min-h-screen p-8 bg-gradient-to-b from-indigo-50 via-white to-indigo-50 font-sans text-gray-900">
      <article className="space-y-12">

        {/* Paraphrased Answer */}
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <div className="absolute -top-6 left-6 w-28 h-1 rounded-full bg-gradient-to-r from-indigo-400 to-purple-500 animate-gradient-x"></div>
          <h2 className="text-2xl font-semibold mb-4 tracking-wide text-indigo-700 flex items-center gap-3 select-none">
            <span className="text-3xl"></span> Paraphrased Answer
          </h2>
          <p className="leading-relaxed text-lg text-gray-800">{response.thoughts}</p>
        </section>

        {/* Agent Reasoning */}
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <div className="absolute -top-6 left-6 w-28 h-1 rounded-full bg-gradient-to-r from-purple-400 to-pink-500 animate-gradient-x delay-200"></div>
          <h2 className="text-2xl font-semibold mb-6 tracking-wide text-purple-700 flex items-center gap-3 select-none">
            <span className="text-3xl"></span> Agent Reasoning
          </h2>
          <ol className="list-decimal list-inside space-y-4 text-gray-700 text-lg">
            {response.agent_reasoning.map((r, i) => (
              <li
                key={i}
                className="bg-purple-50 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow duration-300 cursor-default"
              >
                {r}
              </li>
            ))}
          </ol>
        </section>

        {/* Sources */}
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <div className="absolute -top-6 left-6 w-28 h-1 rounded-full bg-gradient-to-r from-green-400 to-teal-500 animate-gradient-x delay-400"></div>
          <h2 className="text-2xl font-semibold mb-6 tracking-wide text-green-700 flex items-center gap-3 select-none">
            <span className="text-3xl"></span> Sources
          </h2>
          <ul className="space-y-6">
            {response.sources.map((src: any, i) => (
              <li
                key={i}
                className="rounded-2xl p-6 shadow-sm hover:shadow-lg transition-shadow duration-300 cursor-pointer"
              >
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-green-800 font-semibold text-xl hover:underline"
                >
                  Chunk [{src.chunk_id}]
                </a>
                <p className="mt-3 text-green-900 text-base leading-relaxed">{src.preview}</p>
              </li>
            ))}
          </ul>
        </section>

        {/* Suggested Actions */}
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <div className="absolute -top-6 left-6 w-28 h-1 rounded-full bg-gradient-to-r from-pink-400 to-rose-500 animate-gradient-x delay-600"></div>
          <h2 className="text-2xl font-semibold mb-6 tracking-wide text-rose-600 flex items-center gap-3 select-none">
            <span className="text-3xl"></span> Suggested Actions
          </h2>
          <ul className="list-disc list-inside space-y-4 text-rose-700 text-lg mb-10">
            {response.next_actions.map((action, i) => (
              <li key={i}>{action}</li>
            ))}
          </ul>

          {/* Action Buttons */}
          <div className="grid grid-cols-3 gap-8">
            <ActionsRow suggestedActions={response.next_actions} />        
          </div>
        </section>
        
        
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
            <FeedbackUI
              responseText={response.thoughts}
              reasoningChain={response.agent_reasoning}
              retrievedChunks={response.sources}
            />
        </section>
      
      </article>
      {/* Gradient animation */}
      <style>{`
        @keyframes gradient-x {
          0%, 100% {
            background-position: 0% 50%;
          }
          50% {
            background-position: 100% 50%;
          }
        }
        .animate-gradient-x {
          background-size: 200% 200%;
          animation: gradient-x 4s ease infinite;
        }
      `}</style>
    </div>
  );
}
