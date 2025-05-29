**AI Operating Officer**
An intelligent multi-agent AI system built for Microsoft Teams to accelerate strategic decision-making through seamless retrieval, reasoning, and automation.

![Built with FastAPI](https://img.shields.io/badge/Built%20with-FastAPI-blue) ![React](https://img.shields.io/badge/Frontend-React-informational)

---

##1. Value Proposition

* **Strategic Insights**: Synthesizes information across text, audio, slides, and code to deliver board-room–ready recommendations.
* **Persona-Accurate Delivery**: Answers in the voice of executives (CEO, CTO, Head of Product) with transparent source attribution.
* **Closed-Loop Automation**: One-click actions to create GitHub repos, open JIRA tickets, or schedule follow-up meetings via Graph API.
* **Explain & Improve**: Exposes its reasoning chain, collects feedback, and auto-scores with RAGAS + DeepEval for continual learning.

##2. Architecture

```plaintext
+------------------+              +--------------------+           +----------------+
|  Microsoft Teams | <----------> |   FastAPI Backend  | <-------> |    Frontend    |
+------------------+              +--------------------+           +----------------+
                                   |                |       
               +--------------------------+      +-------------------------+
               |   Multi-Agent Layer      |      |  Automation Nodes       |
               |  (Retriever, Synthesizer,|      | (GitHub, JIRA, Calendar)|
               |   Reasoning, Inspector)  |      +-------------------------+ 
               +--------------------------+   
```
System Flow:

1. Frontend: Built with React + TypeScript, provides an intuitive UI for chat, evidence, and     
             actions.

2. Backend: FastAPI server orchestrates a multi-agent graph:

   Retriever Agent: Finds the most relevant, persona-specific context.

   Synthesizer: Generates concise, source-cited executive answers.

   Reasoner: Explains why these chunks and actions were chosen.

   Inspector: Reviews answers for quality, faithfulness, and justification.

   Automation Nodes: Integrate with GitHub, JIRA, Teams Calendar, and more.
   
##3. Getting Started
    
  Prerequisites: Python 3.10+, Node.js 16+, API tokens for JIRA and GitHub.

1. **Clone the repo**

   ```bash
   git clone https://github.com/diyaverma1967/ai-operating-officer-
   cd ai-operating-officer-/backend
   ```
2. **Backend Setup**

   ```bash
   python3.10 -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env         # Fill in API tokens (JIRA, GitHub, Graph)
   uvicorn api:app --reload --port 8000
   ```
3. **Frontend Setup**

   ```bash
   cd ../frontend
   npm install
   npm run dev    # http://localhost:3000
   ```
4. **.env**

   ```
   JIRA_EMAIL=your-email@example.com
   JIRA_API_TOKEN=your-token-here
   JIRA_PROJECT_KEY=PT
   GITHUB_TOKEN=your-github-token
   GITHUB_ORG=your-github-org
    ```
    
##4. Usage

* from web UI type http://localhost:3000 to access the "AI Operating Officer" app.
* Type your query (e.g., "What is Satya Nadella’s perspective on migrating legacy systems to the cloud and spin up a PoC repo to explore it.").
* Review synthesized answer, source citations, and suggested actions.
* Click action buttons to create tickets, repos, or schedule meetings instantly.

##5. Repository Structure

```
backend/        # FastAPI implementation & multi-agent graph
frontend/       # React + TypeScript UI
.env.example    # Template for environment variables
requirements.txt# Python dependencies
README.md       # This document
```

*Demo Link:* (https://drive.google.com/file/d/1G9W_fTvFu_81_neLoAlGbNhgnRIsx_hx/view?usp=sharing) 

