import React from "react";

export default function DummyFinalUILayout() {
  const dummyThoughts =
    "Satya Nadella emphasizes cloud migration as a key digital transformation step.";
  const dummyReasoning = [
    "Retrieved relevant passages from keynote transcript.",
    "Focused on cloud-native telemetry topics.",
    "Proposed next actions based on query context.",
  ];
  const dummySources = [
    {
      url: "https://example.com/keynote",
      chunk_id: 1,
      preview: "Keynote excerpt detailing cloud strategy and impact on global infrastructure.",
    },
    {
      url: "https://example.com/blog",
      chunk_id: 2,
      preview: "Blog post outlining telemetry integration and real-world applications.",
    },
  ];
  const dummyNextActions = [
    "Create Jira ticket for telemetry requirements",
    "Setup GitHub repo for PoC",
    "Schedule meeting manually via Graph API",
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-indigo-50 via-white to-indigo-50 p-8 font-sans text-gray-900 flex justify-center items-start">
      <article className="max-w-4xl w-full space-y-12">

        <h1 className="text-4xl font-serif font-bold text-indigo-700 text-center tracking-wide drop-shadow-sm select-none">
          AI Operating Officer
        </h1>

        {/* Paraphrased Answer */}
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <div className="absolute -top-6 left-6 w-28 h-1 rounded-full bg-gradient-to-r from-indigo-400 to-purple-500 animate-gradient-x"></div>
          <h2 className="text-2xl font-semibold mb-4 tracking-wide text-indigo-700 flex items-center gap-3 select-none">
            <span className="text-3xl">💡</span> Paraphrased Answer
          </h2>
          <p className="leading-relaxed text-lg text-gray-800">{dummyThoughts}</p>
        </section>

        {/* Agent Reasoning */}
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <div className="absolute -top-6 left-6 w-28 h-1 rounded-full bg-gradient-to-r from-purple-400 to-pink-500 animate-gradient-x delay-200"></div>
          <h2 className="text-2xl font-semibold mb-6 tracking-wide text-purple-700 flex items-center gap-3 select-none">
            <span className="text-3xl">🧠</span> Agent Reasoning
          </h2>
          <ol className="list-decimal list-inside space-y-4 text-gray-700 text-lg">
            {dummyReasoning.map((item, idx) => (
              <li
                key={idx}
                className="bg-purple-50 rounded-xl p-4 shadow-sm hover:shadow-md transition-shadow duration-300 cursor-default"
              >
                {item}
              </li>
            ))}
          </ol>
        </section>

        {/* Sources - simplified, no left border or bg */}
        <section className="bg-white rounded-3xl shadow-2xl p-8 relative overflow-hidden">
          <div className="absolute -top-6 left-6 w-28 h-1 rounded-full bg-gradient-to-r from-green-400 to-teal-500 animate-gradient-x delay-400"></div>
          <h2 className="text-2xl font-semibold mb-6 tracking-wide text-green-700 flex items-center gap-3 select-none">
            <span className="text-3xl">📎</span> Sources
          </h2>
          <ul className="space-y-6">
            {dummySources.map((src, idx) => (
              <li
                key={idx}
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
            <span className="text-3xl">🔧</span> Suggested Actions
          </h2>

          <ul className="list-disc list-inside space-y-4 text-rose-700 text-lg mb-10">
            {dummyNextActions.map((action, idx) => (
              <li
                key={idx}
                className="hover:text-rose-500 transition-colors cursor-default"
              >
                {action}
              </li>
            ))}
          </ul>

          {/* Buttons */}
          <div className="grid grid-cols-3 gap-8">
            <button
              disabled
              className="flex items-center justify-center gap-3 bg-rose-100 text-rose-600 rounded-3xl py-3 text-lg font-semibold shadow-md cursor-not-allowed select-none transition-transform hover:scale-105"
              title="Button disabled in dummy layout"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M3 7v10a4 4 0 004 4h10a4 4 0 004-4V7"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M16 3h-1a4 4 0 00-4 4v1m0 4h.01"
                />
              </svg>
              Create GitHub Repo
            </button>
            <button
              disabled
              className="flex items-center justify-center gap-3 bg-rose-100 text-rose-600 rounded-3xl py-3 text-lg font-semibold shadow-md cursor-not-allowed select-none transition-transform hover:scale-105"
              title="Button disabled in dummy layout"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M12 8v4m0 0v4m0-4h4m-4 0H8"
                />
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M7 12h.01M17 12h.01M12 16h.01M12 8h.01"
                />
              </svg>
              Create Jira Ticket
            </button>
            <button
              disabled
              className="flex items-center justify-center gap-3 bg-rose-100 text-rose-600 rounded-3xl py-3 text-lg font-semibold shadow-md cursor-not-allowed select-none transition-transform hover:scale-105"
              title="Button disabled in dummy layout"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                strokeWidth={2}
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  d="M15 10l4.553-2.276A2 2 0 0122 9.618v4.764a2 2 0 01-2.447 1.894L15 14m-6 0v2a2 2 0 002 2h6a2 2 0 002-2v-2m-6 0L9 10"
                />
              </svg>
              Graph API (Manual)
            </button>
          </div>
        </section>
      </article>

      {/* Animation for gradient bars */}
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


// import React from "react";

// export default function DummyFinalUILayout() {
//   // Dummy static data
//   const dummyThoughts =
//     "Satya Nadella emphasizes cloud migration as a key digital transformation step.";
//   const dummyReasoning = [
//     "Retrieved relevant passages from keynote transcript.",
//     "Focused on cloud-native telemetry topics.",
//     "Proposed next actions based on query context.",
//   ];
//   const dummySources = [
//     { url: "https://example.com/keynote", chunk_id: 1, preview: "Keynote excerpt..." },
//     { url: "https://example.com/blog", chunk_id: 2, preview: "Blog post excerpt..." },
//   ];
//   const dummyNextActions = [
//     "Create Jira ticket for telemetry requirements",
//     "Setup GitHub repo for PoC",
//     "Schedule meeting manually via Graph API",
//   ];

//   return (
//     <div className="max-w-3xl mx-auto p-6 space-y-8 bg-gray-50 min-h-screen">
//       <h1 className="text-3xl font-bold text-center mb-6 text-indigo-700">
//         AI Operating Officer
//       </h1>

//       <section className="bg-white p-6 rounded-xl shadow-md space-y-4">
//         <h2 className="text-xl font-semibold text-indigo-600 tracking-wide">💡 Paraphrased Answer</h2>
//         <p className="text-gray-800">{dummyThoughts}</p>
//       </section>

//       <section className="bg-white p-6 rounded-xl shadow-md space-y-4">
//         <h2 className="text-xl font-semibold text-indigo-600 tracking-wide">🧠 Agent Reasoning</h2>
//         <ul className="list-decimal list-inside space-y-2 text-gray-700">
//           {dummyReasoning.map((item, idx) => (
//             <li key={idx}>{item}</li>
//           ))}
//         </ul>
//       </section>

//       <section className="bg-white p-6 rounded-xl shadow-md space-y-4">
//         <h2 className="text-xl font-semibold text-indigo-600 tracking-wide">📎 Sources</h2>
//         <ul className="space-y-6">
//           {dummySources.map((src, idx) => (
//             <li key={idx} className="border-l-4 border-indigo-300 pl-5 bg-indigo-50 rounded-md p-4 shadow-sm hover:shadow-md transition-shadow duration-300">
//               <a
//                 href={src.url}
//                 target="_blank"
//                 rel="noopener noreferrer"
//                 className="text-indigo-700 font-semibold hover:underline break-words"
//               >
//                 Chunk [{src.chunk_id}]
//               </a>
//               <p className="mt-2 text-sm text-indigo-900">{src.preview}</p>
//             </li>
//           ))}
//         </ul>
//       </section>

//       <section className="bg-white p-6 rounded-xl shadow-md space-y-4">
//         <h2 className="text-xl font-semibold text-indigo-600 tracking-wide">🔧 Suggested Actions</h2>
//         <ul className="list-disc list-inside space-y-2 text-gray-700">
//           {dummyNextActions.map((action, idx) => (
//             <li key={idx}>{action}</li>
//           ))}
//         </ul>

//         <div className="mt-6 flex gap-6">
//           <button
//             disabled
//             className="flex-1 py-3 rounded font-semibold bg-gray-200 text-gray-500 cursor-not-allowed select-none shadow-sm"
//             title="Button disabled in dummy layout"
//           >
//             Create GitHub Repo
//           </button>
//           <button
//             disabled
//             className="flex-1 py-3 rounded font-semibold bg-gray-200 text-gray-500 cursor-not-allowed select-none shadow-sm"
//             title="Button disabled in dummy layout"
//           >
//             Create Jira Ticket
//           </button>
//           <button
//             disabled
//             className="flex-1 py-3 rounded font-semibold bg-gray-200 text-gray-500 cursor-not-allowed select-none shadow-sm"
//             title="Button disabled in dummy layout"
//           >
//             Graph API (Manual)
//           </button>
//         </div>
//       </section>
//     </div>
//   );
// }





// import React from "react";

// export default function DummyFinalUILayout() {
//   // Dummy static data
//   const dummyThoughts =
//     "Satya Nadella emphasizes cloud migration as a key digital transformation step.";
//   const dummyReasoning = [
//     "Retrieved relevant passages from keynote transcript.",
//     "Focused on cloud-native telemetry topics.",
//     "Proposed next actions based on query context.",
//   ];
//   const dummySources = [
//     { url: "https://example.com/keynote", chunk_id: 1, preview: "Keynote excerpt..." },
//     { url: "https://example.com/blog", chunk_id: 2, preview: "Blog post excerpt..." },
//   ];
//   const dummyNextActions = [
//     "Create Jira ticket for telemetry requirements",
//     "Setup GitHub repo for PoC",
//     "Schedule meeting manually via Graph API",
//   ];

//   return (
//     <div className="max-w-3xl mx-auto p-6 space-y-6 bg-gray-50 min-h-screen">
//       <h1 className="text-3xl font-bold text-center mb-4">AI Operating Officer</h1>

//       <section>
//         <h2 className="text-xl font-semibold text-blue-700 mb-2">💡 Paraphrased Answer</h2>
//         <p className="p-4 bg-white rounded shadow">{dummyThoughts}</p>
//       </section>

//       <section>
//         <h2 className="text-xl font-semibold text-purple-700 mb-2">🧠 Agent Reasoning</h2>
//         <ul className="list-disc list-inside p-4 bg-white rounded shadow space-y-1">
//           {dummyReasoning.map((item, idx) => (
//             <li key={idx}>{item}</li>
//           ))}
//         </ul>
//       </section>

//       <section>
//         <h2 className="text-xl font-semibold text-green-700 mb-2">📎 Sources</h2>
//         <ul className="list-disc list-inside p-4 bg-white rounded shadow space-y-4">
//           {dummySources.map((src, idx) => (
//             <li key={idx}>
//               <a
//                 href={src.url}
//                 target="_blank"
//                 rel="noopener noreferrer"
//                 className="text-blue-600 hover:underline font-semibold"
//               >
//                 Chunk [{src.chunk_id}]
//               </a>
//               <p className="text-gray-700 mt-1">{src.preview}</p>
//             </li>
//           ))}
//         </ul>
//       </section>

//       <section>
//         <h2 className="text-xl font-semibold text-rose-700 mb-2">🔧 Suggested Actions</h2>
//         <ul className="list-disc list-inside p-4 bg-white rounded shadow space-y-1">
//           {dummyNextActions.map((action, idx) => (
//             <li key={idx}>{action}</li>
//           ))}
//         </ul>
//       </section>

//       <section className="flex gap-4 mt-4">
//         <button
//           className="flex-1 bg-gray-200 py-3 rounded font-semibold cursor-not-allowed"
//           disabled
//           title="Button disabled in dummy layout"
//         >
//           Create GitHub Repo
//         </button>
//         <button
//           className="flex-1 bg-gray-200 py-3 rounded font-semibold cursor-not-allowed"
//           disabled
//           title="Button disabled in dummy layout"
//         >
//           Create Jira Ticket
//         </button>
//         <button
//           className="flex-1 bg-gray-200 py-3 rounded font-semibold cursor-not-allowed"
//           disabled
//           title="Button disabled in dummy layout"
//         >
//           Graph API (Manual)
//         </button>
//       </section>
//     </div>
//   );
// }
