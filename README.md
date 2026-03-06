# Agentic AI

General-purpose Python coding agent with the ability to read, write and run files. Utilizes and maintains internal reasoning (chain of thought) across messages, but it can be also turned off to spare tokens on easier tasks. Session logs are automatically saved in a list of JSON objects, capturing every thought, tool call, and result in real-time to `logs/session_[timestamp].jsonl`, allowing you to review exactly why the agent made a specific decision.

Warning: Although there are path-traversal protection and subprocess timeouts in place to ensure the agent remains within the permitted workspace, apart from that, the agent can do anything on your machine.

## 🚀 Quick start

### 1. Prerequisites

- Python 3.10+
- An API key: you can get one at [Google AI Studio](aistudio.google.com) (For now, only Gemini is supported.)

### 2. Clone the repository
```
git clone github.com/nonlinear-vibes/agentic-AI
cd agentic-AI
```

### 3. Set up your environment
Create a `.env` file in the root directory and add your API key:

```
echo "API_KEY=your_key_here" > .env
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Run the Agent

```
python main.py
```


## 🛠️ Project structure
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

## ⚙️ Configuration
The agent's behavior can be toggled in `config.py`:
- `MAX_CHARS` - Maximum number of characters that can be read from a file in a single read function call.
- `WORKING_DIR` - Name of your working directory. Strict path verification ensures that the agent cannot operate outside of this directory.
- `MAX_ITERS` - Maximum number of function call iterations in a single response.
- `VERBOSE` - If set to `True`, function calls and responses are printed to the console.
- `THINKING` - Enables thinking capability.
- `KEEP_THOUGHTS` - Keeps the agent's internal thought process in the session history, enabling better chain of thought context on the expense of higher token traffic.
- `THINKING_TOKEN_LIMIT` - How many tokens can be used for thinking in a single round of messages.

## 🔧 Agentic functions
The agent can call the following functions:

- `get_file_content(file_path, line_start, line_end)` - File-reading tool that allows the agent to read specific line ranges to efficiently handle large codebases.

- `get_files_info(directory)` - List files and directories with metadata.

- `write_file(file_path, content)` - Create or overwrite files with automatic directory creation.

- `run_python_file(file_path, args)` - Run Python scripts and capture STDOUT/STDERR/Tracebacks for self-debugging.





