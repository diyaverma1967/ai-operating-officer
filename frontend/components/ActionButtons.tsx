import React, { useState } from "react";
import { fetchTriggerAutomation } from "@/lib/api";
import { detectActionTypes } from "@/utils/detectActionTypes";

export default function ActionsRow({ suggestedActions }: { suggestedActions: string[] }) {
  const [githubUrl, setGithubUrl] = useState<string | null>(null);
  const [jiraUrl, setJiraUrl] = useState<string | null>(null);

  const { github, jira, graph } = detectActionTypes(suggestedActions);

  const handleJira = async () => {
    const jiraAction = suggestedActions.find((act) =>
      /jira|ticket|issue|open ticket/i.test(act)
    );
    if (!jiraAction) return;
    const res = await fetchTriggerAutomation("jira", jiraAction, "");
    if (res.url) setJiraUrl(res.url);
    else alert("Jira ticket creation failed.");
  };

  const handleGithub = async () => {
    const githubAction = suggestedActions.find((act) =>
      /github|repo|repository|codebase/i.test(act)
    );
    if (!githubAction) return;
    const res = await fetchTriggerAutomation("github", githubAction, "");
    if (res.url) setGithubUrl(res.url);
    else alert("GitHub repo creation failed.");
  };

  const handleGraphAPI = () => {
    window.open("https://calendar.google.com/calendar/r/eventedit", "_blank");
  };

  return (
    <>
      <button
        onClick={handleGithub}
        disabled={!github}
        className={`flex items-center justify-center gap-3 py-3 rounded-3xl font-semibold shadow-md transition-transform hover:scale-105
          ${github ? "bg-indigo-500 text-white cursor-pointer" : "bg-gray-300 text-gray-500 cursor-not-allowed"}
        `}
        title={github ? "Create GitHub Repo" : "No GitHub repo action detected."}
      >
        Create GitHub Repo
      </button>
      <button
        onClick={handleJira}
        disabled={!jira}
        className={`flex items-center justify-center gap-3 py-3 rounded-3xl font-semibold shadow-md transition-transform hover:scale-105
          ${jira ? "bg-purple-600 text-white cursor-pointer" : "bg-gray-300 text-gray-500 cursor-not-allowed"}
        `}
        title={jira ? "Create Jira Ticket" : "No Jira ticket action detected."}
      >
        Create Jira Ticket
      </button>
      <button
        onClick={handleGraphAPI}
        className="flex items-center justify-center gap-3 py-3 rounded-3xl bg-pink-500 text-white font-semibold shadow-md transition-transform hover:scale-105"
        title="Schedule Meeting"
      >
        Schedule Meeting
      </button>

      {/* Display URLs */}
      <div className="mt-4 space-y-2">
        {githubUrl && (
          <div>
            ✅ GitHub Repo:{" "}
            <a
              // href={githubUrl}
              href={"https://github.com/diyaverma1967?tab=repositories"}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              {githubUrl}
            </a>
          </div>
        )}
        {jiraUrl && (
          <div>
            ✅ Jira Ticket:{" "}
            <a
              href={jiraUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              {jiraUrl}
            </a>
          </div>
        )}
      </div>
    </>
  );
}
