import os
import json
from datetime import datetime

# --- Constants & Settings ---
MAX_CHARS = 10000
WORKING_DIR = "./calculator"
MAX_ITERS = 20
VERBOSE = False
THINKING = True
KEEP_THOUGHTS = True
THINKING_TOKEN_LIMIT = 512



# --- Session & Logging Setup ---
SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Unique filename for this specific run
LOG_FILE = os.path.join(LOG_DIR, f"session_{SESSION_ID}.jsonl")

def log_event(event_type, data):
    """Appends a JSON-formatted event to the session-specific log file."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "data": data
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")