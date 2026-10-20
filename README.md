<<<<<<< HEAD
**Goal:** Build a local AI agent that takes tasks via CLI, reasons about them, uses tools to execute actions on your machine, and optionally speaks the response. Ties together LLM usage, tool building, and agent architecture — core AI Engineering skills.

**Skills:** Ollama, agent loop, tool use, text-to-speech, Python.

### Configuration

The agent name and LLM model are configurable — swap models without changing code.

| Setting | Default | How to change |
|---------|---------|---------------|
| Agent name | `Spark` | `config.yaml` → `agent_name` or `--name` flag |
| LLM model | `llama3.1:8b` | `config.yaml` → `model` or `--model` flag |
| TTS voice | `en_US-lessac-medium` | `config.yaml` → `tts_voice` |
| TTS enabled | `false` | `--speak` flag or `config.yaml` → `tts_enabled` |

### Architecture

```
You type a task (CLI)
        │
        ▼
┌──────────────────────────┐
│   Agent Loop             │  think → pick tool → observe → repeat
│   (Ollama, any model)    │
└──┬─────┬─────────────────┘
   │     │
   ▼     ▼
┌──────┐ ┌──────────────┐
│Tools │ │   Response    │
└──────┘ └──────┬───────┘
                │
        ┌───────┴───────┐
        │               │
   Print to CLI    Piper TTS (--speak flag)
                        │
                    Speaker 🔊
```

### Tools

| Tool | What it does | Connects to |
|------|-------------|-------------|
| `query_db` | Run SQL against PostgreSQL | P2 database |
| `search_files` | Find files by name/pattern | Local filesystem |
| `read_file` | Read a file's contents | Local filesystem |
| `run_python` | Execute a Python snippet | Local Python |
| `web_search` | Search the internet | DuckDuckGo API (free, no key) |
| `system_info` | CPU/GPU/RAM/disk status | Local system |

### Short scope (2-3 weekends)

#### 1. Set up Ollama, verify tool calling works
- [x] Install Ollama if not already installed (`ollama.com`, Windows native)
- [x] Pull the default model: `ollama pull llama3.1:8b`
- [x] Verify basic chat: `ollama run llama3.1:8b "Hello"`
- [x] Install Ollama Python SDK: `pip install ollama`
- [x] Test tool calling — send a message with a `tools` parameter, confirm the model returns `tool_calls` instead of plain text
- [x] Parse the response format: `{"function": {"name": "...", "arguments": {...}}}`

#### 2. Create config system for easy model/name switching
- [x] Create `config.yaml` with `agent_name`, `model`, `tts_voice`, `tts_enabled`
- [ ] Write config loader with fallback defaults (agent works even without config file)
- [ ] Add CLI overrides via `argparse`: `--model`, `--name` flags take precedence over config
- [ ] Verify switching models works: pull a second model (e.g. `mistral:7b`), run agent with `--model mistral:7b`

#### 3. Define 3 tools as Python functions with JSON schemas
- [x] Pick first 3 tools (suggested: `search_files`, `read_file`, `system_info` — no external deps)
- [x] Write each as a plain Python function that returns a string
- [ ] Write the JSON schema for each tool (name, description, parameters with types and `required`)
- [ ] Build a tool registry — a dict mapping tool name → Python function for dynamic dispatch
- [ ] Test each tool independently before wiring into the agent loop

#### 4. Build the agent loop
- [ ] Implement the core loop: user message → send to Ollama with tools → check response
- [ ] If response has `tool_calls` → execute the matching tool → append result to conversation → loop back
- [ ] If response is plain text (no tool call) → that's the final answer → return it
- [ ] Maintain a `messages` list accumulating the full conversation (user, assistant, tool roles)
- [ ] Write a system prompt: who the agent is, what tools it has, when to use them vs. answer directly
- [ ] Add max iterations guard (e.g. 10) to prevent infinite tool-calling loops

#### 5. CLI interface
- [ ] Build interactive input loop: `while True` with `input()`, exit on "quit"/"exit"
- [ ] Wire in `argparse` for flags: `--speak`, `--verbose`, `--model`, `--name`
- [ ] `--verbose` flag prints each tool call (name, arguments, result) as it happens
- [ ] Handle Ctrl+C gracefully with `try/except KeyboardInterrupt`
- [ ] Optional: add colour to output with `colorama` (distinguish user / tool activity / agent response)

#### 6. Add Piper TTS for spoken output
- [ ] Install Piper: `pip install piper-tts`
- [ ] Download a voice model (`.onnx` file, e.g. `en_US-lessac-medium`)
- [ ] Write a `speak(text: str)` function using Piper CLI or Python API
- [ ] Wire into main loop: if `--speak` flag is set, call `speak(response)` after printing
- [ ] Test with short and long responses — long ones may need chunking

#### 7. Handle edge cases
- [ ] Tool execution fails (file not found, bad SQL, etc.) → catch exception, send error back to LLM as tool result
- [ ] LLM returns malformed tool call → validate against schema, return clear error message
- [ ] LLM calls a tool not in the registry → return "Unknown tool" with available tool list
- [ ] LLM answers directly (no tool needed) → just print, no loop iteration
- [ ] LLM gets stuck calling same tool repeatedly → max iterations guard + optional duplicate detection

#### 8. Push to GitHub with README
- [ ] Init repo, create `.gitignore` (exclude `__pycache__`, `.env`, voice model `.onnx` files)
- [ ] Write README: what it is, architecture diagram, prerequisites, install, how to run, example session
- [ ] Create `requirements.txt` with pinned versions
- [ ] Create GitHub repo, push

### Long scope (extends by 3-4 weeks)

Everything above, plus:

#### 1. Wake word detection ("Hey Spark") using `openwakeword`
- [ ] Install `openwakeword` and `sounddevice`
- [ ] Set up continuous microphone listening in a background thread
- [ ] Train or download a wake word model for your chosen phrase
- [ ] On wake word detection → start recording → pass audio to STT (step 2) → feed text into agent loop
- [ ] Add visual/audio feedback when wake word is detected (e.g. a beep or terminal indicator)
- [ ] Handle false positives gracefully — add a confirmation timeout (silence = cancel)

#### 2. Speech-to-text input with `faster-whisper` behind `--listen` flag
- [ ] Install `faster-whisper` (runs on GPU via CTranslate2)
- [ ] Pick a model size: `base` for speed, `small` or `medium` for accuracy
- [ ] Implement voice activity detection (VAD) — detect when the user stops speaking
- [ ] Record audio from microphone → transcribe with Whisper → pass transcript into agent loop
- [ ] Print the transcribed text so the user can see what the agent heard
- [ ] Handle ambient noise: test in quiet and noisy environments, tune VAD sensitivity

#### 3. Conversation memory — remember previous exchanges within a session
- [ ] Keep the full `messages` list across turns (already partially done in short scope)
- [ ] Add a `/clear` command to reset conversation history
- [ ] Implement context window management — when messages grow too long, summarise older turns
- [ ] Add a `/history` command to print the current conversation
- [ ] Optional: persist conversation to a JSON file, load on startup with `--resume` flag

#### 4. Connect to P2's PostgreSQL — natural language → SQL → results → spoken summary
- [ ] Add `psycopg2` to dependencies, configure DB connection in `config.yaml`
- [ ] Enhance the `query_db` tool: accept natural language, let the LLM generate SQL
- [ ] Add a `list_tables` tool so the agent can discover the schema before writing queries
- [ ] Add a `describe_table` tool that returns column names, types, and sample rows
- [ ] Safety: run queries as read-only (`SET default_transaction_read_only = on`) to prevent accidental writes
- [ ] Format query results as a readable table before passing to TTS or printing

#### 5. Streaming responses — agent speaks before the full response is generated
- [ ] Switch Ollama calls to streaming mode (`stream=True`)
- [ ] Print tokens to terminal as they arrive (character-by-character output)
- [ ] Buffer streamed text into sentences for TTS — send each sentence to Piper as soon as it's complete
- [ ] Handle tool calls in streaming mode — detect when a tool call starts mid-stream and pause output
- [ ] Ensure `--verbose` mode still works correctly with streaming

#### 6. Build a Streamlit UI
- [ ] Create a basic chat interface with `st.chat_message` and `st.chat_input`
- [ ] Display tool calls in expandable sections (show tool name, arguments, result)
- [ ] Add a sidebar with config options: model selector, TTS toggle, verbose toggle
- [ ] Show a "thinking" spinner while the agent loop runs
- [ ] Display conversation history with clear visual distinction between user, agent, and tool messages
- [ ] Optional: add a visual timeline of tool calls for each agent response

#### 7. Build tools as an MCP server — reusable with any MCP-compatible agent
- [ ] Understand MCP transport: stdio (local) vs HTTP/SSE (remote)
- [ ] Refactor existing tools into MCP-compatible format (each tool = a JSON-RPC handler)
- [ ] Implement the MCP server using `mcp` Python SDK (`pip install mcp`)
- [ ] Register all tools with proper JSON schemas via the MCP protocol
- [ ] Test the MCP server with an external client (e.g. Claude Code, another MCP-compatible agent)
- [ ] Optionally make Spark itself an MCP client — it can call tools hosted on other MCP servers

#### 8. Containerize the full stack
- [ ] Write a `Dockerfile` for the Spark agent (Python + dependencies)
- [ ] Handle Ollama: either run it on the host and connect via network, or include it in Docker Compose
- [ ] Write `docker-compose.yml`: Spark agent + PostgreSQL (from P2) + Ollama (optional)
- [ ] Mount `config.yaml` as a volume so settings are editable without rebuilding
- [ ] Handle audio I/O in Docker — TTS output needs access to host audio device (or skip TTS in container mode)
- [ ] Test the full stack: `docker-compose up` → agent is running and can query the database