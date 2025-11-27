maiper — ReAct-based Agentic LLM Pipeline using Groq LLaMA

maiper is an agentic AI project that uses the ReAct (Reason + Act) prompting framework with Groq’s ultra-fast LLaMA models to build structured, tool-using AI workflows.
This project demonstrates how to generate structured outputs such as roadmaps, JSON results, and agent-driven reasoning using custom prompts.

⸻

🚀 Features

✅ ReAct-Style AI Agent
	•	Implements the ReAct (Think → Act → Observe → Answer) pattern.
	•	Uses a custom prompt from reAct_prompt/reAct.py.

⚡ Groq LLaMA Integration
	•	Calls meta-llama/llama-4-maverick-17b-128e-instruct through Groq API.
	•	Extremely low latency and high-throughput inference.

📦 Structured Output Handling
	•	Extracts pure JSON from messy model outputs.
	•	Parses roadmaps, mermaid diagrams, lists, and nested structures.

🧪 Custom Query Pipeline
	•	Example prompt: “Give me the roadmap for GATE 2026 DA exam.”
	•	Automatically returns structured study plans.

📌 Future Improvements
	•	Add Streamlit UI for roadmap visualization
	•	Add multiple agents (search agent, reasoning agent)
	•	Add proper tool-use execution engine
	•	Add CLI runner

⸻

🤝 Contributing

Contributions and pull requests are welcome!
Feel free to open issues for bugs, discussions, or feature requests.
