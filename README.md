# Agentic AI

General-purpose Python coding agent with the ability to read, write and run files. Utilizes and maintains internal reasoning (chain of thought) across messages, but it can be also turned off to spare tokens on easier tasks. Session logs are automatically saved in a list of JSON objects, capturing every thought, tool call, and result in real-time to `logs/session_[timestamp].jsonl`, allowing you to review exactly why the agent made a specific decision.

> ⚠️ **Security notes:**
> - `run_python_file` executes scripts inside an isolated, network-disabled Docker container (no filesystem access outside the workspace, capped memory/process count, non-root user) **if Docker is installed and running**. If Docker isn't available, the agent falls back to running scripts directly on your machine, with only a timeout and path-traversal checks in place.
> - All file tools (`get_file_content`, `get_files_info`, `write_file`) enforce path-traversal protection, but nothing prevents the agent from reading, overwriting, or deleting any file *within* the working directory.
> - Like any LLM agent that reads external content (files, script output), this agent is potentially susceptible to **prompt injection**. Sandboxing limits the damage such manipulation could cause, but does not prevent the manipulation itself.

## 🚀 Quick start

### 1. Prerequisites
- Python 3.10+
- An API key from [OpenRouter](https://openrouter.ai/)
- Optional but recommended: [Docker](https://docs.docker.com/get-docker/) — sandboxes `run_python_file` execution (see Security notes above). Without it, scripts run directly on your machine with no isolation.
  - Windows/macOS: install [Docker Desktop](https://www.docker.com/products/docker-desktop/) and make sure it's running before starting the agent.
  - Linux: install [Docker Engine](https://docs.docker.com/engine/install/) and add your user to the `docker` group (`sudo usermod -aG docker $USER`) so it runs without `sudo`.
- Optional: [uv](https://docs.astral.sh/uv/) package manager, install with:
  - Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

### 2. Clone the repository
```
git clone https://github.com/nonlinear-vibes/agentic-AI
cd agentic-AI
```

### 3. Set up your environment
Create a `.env` file in the root directory and add your API key:

```
echo "API_KEY=your_key_here" > .env
```

### 4. Install dependencies
If you have `uv` installed:
```
uv sync
```
If not:
```
pip install -r requirements.txt
```

### 5. Run the Agent
If you have `uv` installed:
```
uv run main.py
```
If not:
```
python main.py
```
Note: the first time the agent runs a Python file with Docker available, it will pull the `python:3.12-slim` sandbox image (a few hundred MB) — this may take a moment.

## ⚙ Project structure
```
.  
├─ functions
│  ├─ get_file_content.py
│  ├─ get_files_info.py
|  ├─ run_python_file.py
|  └─ write_file.py
├─ logs
|  └─ [saved session logs]
├─ workspace
|  └─ [your project folder]
├─ call_function.py
├─ config.py
├─ main.py
└─ prompts.py
```

Upon a user request, the agent can decide either to generate a response or call for function execution. Each function execution's result is returned to the agent and it can decide again which action to take, and so on in a loop. Once it decides to respond with a text, the user can prompt it again.

## 🛠️ Configuration
The agent and its behavior can be set in `config.py`:
- `MODEL_ID` - Name of the model, prefixed with the provider, for example `google/gemini-2.5-flash`
- `MAX_CHARS` - Maximum number of characters that can be read from a file in a single read function call.
- `WORKING_DIR` - Name of your working directory. Strict path verification ensures that the agent cannot operate outside of this directory.
- `MAX_ITERS` - Maximum number of function call iterations in a single response.
- `VERBOSE` - If set to `True`, function calls and responses are printed to the console.
- `REASONING_EFFORT` - Sets reasoning effort, trading off latency and tokens for deeper thinking. (possible values: `"minimal"`, `"low"`, `"medium"`, `"high"`)

## 🔧 Agentic functions
The agent can call the following functions:

- `get_file_content(file_path, line_start, line_end)` - File-reading tool that allows the agent to read specific line ranges to efficiently handle large codebases.

- `get_files_info(directory)` - List files and directories with metadata.

- `write_file(file_path, content)` - Create or overwrite files with automatic directory creation.

- `run_python_file(file_path, args)` - Run Python scripts and capture STDOUT/STDERR/exit codes for self-debugging. Runs inside a sandboxed Docker container when available, otherwise falls back to direct execution (see Security notes).





