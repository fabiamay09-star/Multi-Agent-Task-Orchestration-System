# Multi-Agent-Task-Orchestration-System
A lightweight platform where multiple AI agents collaborate to complete a complex task to researching a topic, writing a report, and reviewing it for quality.
# Dependencies
requirements.txt
google-generativeai 
duckduckgo-search (lightweight web search for the Researcher)
python-dotenv (for API keys)
Backend Logic
backend/agents.py
•	Refactor Agents: Rename Coder to WriterAgent.
•	LLM Integration: Update the perform_work method in BaseAgent (or sub-classes) to actually call an LLM API.

