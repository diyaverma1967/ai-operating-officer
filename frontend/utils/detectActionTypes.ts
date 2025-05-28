export function detectActionTypes(suggestedActions: string[]) {
  const githubRegex = /github|repo|repository|codebase|create code repo/i;
  const jiraRegex = /jira|ticket|issue|open ticket|create issue|raise a ticket/i;
  const graphRegex = /graph api|meeting|schedule|calendar|teams meeting/i;

  const github = suggestedActions.some(action => githubRegex.test(action));
  const jira = suggestedActions.some(action => jiraRegex.test(action));
  const graph = suggestedActions.some(action => graphRegex.test(action));

  const matched = {
    github: suggestedActions.find(action => githubRegex.test(action)) || null,
    jira: suggestedActions.find(action => jiraRegex.test(action)) || null,
    graph: suggestedActions.find(action => graphRegex.test(action)) || null,
  };

  return { github, jira, graph, matched };
}
