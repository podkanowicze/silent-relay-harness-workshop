# Context Telephone — runnable application

## What is implemented

- Dependency-free Python browser application, optional FastAPI adapter, and optional terminal client.
- Nickname login. The browser stores only the nickname in `localStorage`; SQLite stores identity, sessions, assignments, prompts, replies, handoffs, and every before/after file snapshot.
- Re-entering the same normalized nickname restores the same participant and current assignment.
- Lobby capacity is 12 by default. Reaching capacity does not auto-start: the protected host page locks the current roster and starts one exercise per joined participant.
- New nicknames are rejected after start; existing nicknames continue to restore their state.
- One directory per exercise with exactly `index.html`, `styles.css`, and `app.js`.
- The real Deep Agents Code (`dcode`) non-interactive harness for every prompt.
- Every prompt starts a new DCode process and fresh thread. A disposable profile prevents memory, skills, hooks, config, and conversation history from crossing turns.
- `SPEC-0` is exposed as an image only to the author during `DELTA-1`.
- The participant sees only the current delta and the latest public agent reply. Neither is injected into the model automatically.
- While a prompt is running, the terminal panel receives Deep Agents Code stdout/stderr incrementally and the run button shows elapsed seconds.
- Repeat prompts, terminal-style public activity, code view, sandboxed live preview, handoff, DELTA-12 interpretation, and original-author review.
- No pedagogical prompt-length cap. The shared round timer does not reset, but it is advisory only: prompts, retries, preview, and handoff remain available at `00:00`; the moderator controls rotation.
- `circular` routing for a two-person manual test and `skip_author` routing for the workshop.
- Transactional staging outside the repository, a SQLite publication journal, and startup recovery. The agent cannot publish a fourth file, a missing file, a symlink, binary data, or an oversized file.

## File boundary

DCode runs with shell, interpreter, MCP, inherited memory, and inherited skills disabled. Every run receives a disposable copy and a host policy naming only `index.html`, `styles.css`, and `app.js`. The server validates that exact directory shape and commits only those three allowlisted files.

Local DCode's filesystem backend is not an OS sandbox: an adversarial model could attempt an absolute path outside staging even though the turn policy forbids it. The transactional layer guarantees what reaches the workshop project, not every possible host write. Use a per-turn container or separate OS identity when the DevPod threat model requires hard host isolation.

The generated project runs inside a sandboxed preview with network, forms, parent navigation, cookies, and API access blocked. Run one server process on a trusted workshop network or DevPod (or one Uvicorn worker when using the optional FastAPI adapter). A public internet deployment needs per-run container isolation and real authentication.

Nickname login is workshop identity, not secure authentication. Anyone who knows another participant's nickname can resume that identity.

## API key

Keep the key only in the server process environment. Do not put it in this repository, SQLite, or an exercise directory.

PowerShell:

```powershell
$env:DEEPAGENTS_CODE_OPENAI_API_KEY = "<key>"
```

Linux:

```bash
export DEEPAGENTS_CODE_OPENAI_API_KEY="<key>"
```

The server reads it only from its environment. It is not copied into SQLite, prompts, staging directories, project files, or browser responses.

## Local test

With Python 3.11+:

```bash
python -m pip install -e ".[agent]"
python -m workshop_runner
```

The default configuration uses:

```text
capacity 12, minimum start 2
up to 12 exercises; active exercise count equals the roster at host start
circular routing
Deep Agents Code, gpt-5.6-luna, high reasoning
http://0.0.0.0:8000 (open http://127.0.0.1:8000 locally)
```

Open participant windows at `/` and join with different nicknames. Open `/admin`, enter `WORKSHOP_ADMIN_CODE`, review the roster, and click **Start with N**. Participants remain in the polling lobby until that click.

To test one application only:

```powershell
$env:WORKSHOP_DATA_DIR = ".\workshop_data\single-exercise"
$env:WORKSHOP_PARTICIPANTS = "1"
$env:WORKSHOP_MIN_PARTICIPANTS = "1"
$env:WORKSHOP_EXERCISES = "01-small-town-wings"
python -m workshop_runner
```

Use a new `WORKSHOP_DATA_DIR` for every fresh rehearsal or workshop. Its SQLite database and active project directories then start together; the blank `workshop_projects/` tree remains a reference/template bank.

For a no-cost UI/state test, explicitly set `WORKSHOP_AGENT_MODE=mock`.

## Deep Agents Code execution

```bash
python -m pip install -e ".[agent]"
```

PowerShell:

```powershell
$env:WORKSHOP_AGENT_MODE = "dcode"
$env:WORKSHOP_MODEL = "gpt-5.6-luna"
$env:WORKSHOP_REASONING_EFFORT = "high"
$env:DEEPAGENTS_CODE_OPENAI_API_KEY = "<key>"
python -m workshop_runner
```

Each request is piped through stdin to `python -m deepagents_code --stdin -q --no-stream --no-mcp --no-interpreter`. No shell allow-list is supplied, so DCode disables local shell access. Linux uses the same variable names with `export`.

## Full workshop on a Linux DevPod

```bash
export WORKSHOP_PARTICIPANTS=12
export WORKSHOP_MIN_PARTICIPANTS=2
export WORKSHOP_DATA_DIR=/workspace/context-telephone-run
export WORKSHOP_EXERCISES=
export WORKSHOP_ROUTING_MODE=skip_author
export WORKSHOP_AGENT_MODE=dcode
export WORKSHOP_MODEL=gpt-5.6-luna
export WORKSHOP_REASONING_EFFORT=high
export WORKSHOP_HOST=0.0.0.0
export WORKSHOP_OPEN_BROWSER=false
export WORKSHOP_COOKIE_SECURE=true
export WORKSHOP_ADMIN_CODE="<host-code>"
export DEEPAGENTS_CODE_OPENAI_API_KEY="<key>"
python -m workshop_runner
```

Run exactly one server worker. Put TLS and access control in the DevPod ingress/reverse proxy.

## Terminal client

With the server running:

```bash
python -m workshop_runner.cli --server http://127.0.0.1:8000 --nick alex
```

The terminal client uses the same backend state and fresh-session semantics. The browser remains the recommended surface because it shows the SPEC-0 image and sandboxed preview.

## Tests

The application-level smoke path needs only Python itself:

```bash
python -m compileall -q workshop_runner tests
```

For the pytest suite, install the optional test dependencies:

```bash
python -m pip install -e ".[test]"
python -m pytest
```

Tests force mock mode. No automated test calls the OpenAI API unless an explicit live smoke test is requested.
