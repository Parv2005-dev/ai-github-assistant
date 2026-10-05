AI GitHub Assistant

An autonomous CLI assistant built from scratch (no framework) using LLM function calling. It reasons about user questions and dynamically decides when to call a real tool — fetching live GitHub profile data — versus answering directly.

Features
Full tool-calling loop: model reasoning → function execution → result injection → final response
Integrates the GitHub REST API as a callable tool to fetch real user profile data (name, public repos, followers)
Stateful multi-turn conversation management, manually maintained across a fundamentally stateless API
Graceful error handling for invalid usernames, timeouts, and network failures
Secure API key handling via environment variables (.env), never hardcoded
Tech Stack
Python
Groq API (LLM inference)
GitHub REST API
python-dotenv for secure configuration
How It Works
User asks a question in natural language
The model decides whether answering requires real data
If so, it requests a tool call (get_github_user) with the appropriate username
The assistant executes the real API call and returns the result to the model
The model generates a final, natural-language answer using that real data

What I Learned
Implementing function/tool calling directly from a raw LLM API, without relying on a framework
Designing a JSON-based tool schema for reliable parameter extraction from natural language
Managing conversation history manually to maintain context across a stateless API
Secure credential management using environment variables