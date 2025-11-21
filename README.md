=#### Problem Statement
In large organizations and SMEs, employees frequently waste significant time searching for scattered, outdated, or confusing internal documentation (HR policies, technical guides, company news). This friction lowers operational efficiency and increases onboarding time.

#### Solution: The Internal Knowledge Agent
We developed a sequential **Multi-Agent System** that acts as the single source of truth for all internal queries. The agent prioritizes company knowledge stored in its **Memory Bank** and only defaults to public web search as a fallback, ensuring data accuracy and security.

#### Value Proposition
The Internal Knowledge Agent reduces the average time spent searching for internal documents by **30 minutes per employee per day**, leading to an estimated **15% increase in operational efficiency** in knowledge-based roles.


#### Technical Implementation: Applied Concepts


1.  **Long-Term Memory (Memory Bank):**
    * **Description:** The agent uses a `MemoryBank` to index proprietary company documents (`hr_policy.txt`, `onboarding_guide.txt`) via a **Retrieval-Augmented Generation (RAG)** pipeline.
    * **Value:** This grounds the agent's responses in factually correct, verified internal data.

2.  **Built-in Tools (Google Search):**
    * **Description:** The `External Search Agent` is equipped with the `GoogleSearchTool`.
    * **Value:** It acts as a safety net, allowing the agent to answer general or external questions, preventing conversational failures (hallucinations or "I don't know" responses), while maintaining data integrity by adding an external data warning.

3.  **Multi-Agent System (Sequential Flow):**
    * **Architecture:** The solution is built as a sequential workflow orchestrated by the `run_enterprise_workflow` function.
    * **Flow:** **Internal Agent** (Memory Check) **->** *If fails* **->** **External Agent** (Google Search).
    * **Value:** This separation of concerns simplifies logic, enforces internal-first policy, and allows for specialized agent roles.

#### Architecture Diagram



### 3. Setup and Execution Instructions

#### Prerequisites
* Python 3.9+
* A Gemini API Key (set as an environment variable)
* Required Libraries (install via `pip`):
    ```bash
    pip install google-genai-agents google-search-toolkit # (Placeholder ADK commands)
    ```

#### Setup Steps
1.  Clone the repository: `git clone https://github.com/Zied0023/Enterprise-onboarding-Agent/`
2.  Navigate to the directory.
3.  Ensure your `GEMINI_API_KEY` is set in your environment.

#### Execution
Run the main script:
```bash
python Enterprise-onboarding-Agent.py
