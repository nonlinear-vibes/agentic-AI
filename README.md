# Gemini-based coding agent in Python

A lightweight, robust, and highly transparent Python-based agentic loop powered by Gemini 2.5 Flash.

## 🚀 Key Features
- Native "Thinking" Integration: Utilizes Gemini 2.5's internal reasoning chain (Chain-of-Thought) to simulate and verify plans before execution.

- Stateful Memory: Maintains a clean conversation history with automated "thought pruning" to optimize token usage.

- Safety Guardrails: Implements path-traversal protection and subprocess timeouts to ensure the agent remains within the permitted workspace.

- JSONL Session Logging: Automatically generates unique, machine-readable logs for every session, capturing every thought, tool call, and result.

- Surgical File Access: Advanced file-reading tools allow the agent to read specific line ranges, enabling it to handle large codebases efficiently.

## 🛠️ Project structure


## ⚙️ Configuration
The agent's behavior can be toggled in `config.py`:
- `MAX_CHARS` - Maximum number of characters that can be read from a file in a single read function call.
- `WORKING_DIR` - Name of your working directory. Strict path verification ensures that the agent cannot operate outside of this directory.
- `MAX_ITERS` - Maximum number of function call iterations in a single response.
- `VERBOSE` - If set to `True`, function calls and responses are printed to the console.
- `THINKING` - Enables thinking capability.
- `KEEP_THOUGHTS` - Keeps the agent's internal thought process in the session history, enabling better chain of thought context on the expense of higher token traffic.
- `THINKING_TOKEN_LIMIT` - How many tokens can be used for thinking in a single round of messages.

## 🔧 Available agentic functions
The agent currently has the following capabilities out of the box:

- File Exploration: List files and directories with metadata.

- Surgical Read: Read specific line ranges of files.

- File Writing: Create or overwrite files with automatic directory creation.

- Code Execution: Run Python scripts and capture STDOUT/STDERR/Tracebacks for self-debugging.

