# Claude CLI Agent

A conversational CLI agent powered by Claude (Anthropic API) that uses tool-use to solve math expressions. Implements the ReAct loop — Claude reasons about when to call a tool, executes it, and returns a final answer.

## Features

- Multi-turn conversation with memory
- Calculator tool using Claude's native tool-use API
- ReAct loop implementation (Reason + Act)
- Safe math expression evaluation

## Setup

1. Clone the repo
```bash
   git clone https://github.com/Manishmarri11/CLI-Agent.git
   cd CLI-Agent
```

2. Install dependencies
```bash
   pip install anthropic python-dotenv
```

3. Create a `.env` file
