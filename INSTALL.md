# Installation

## Requirements

- Python 3.11+
- Git
- an OpenAI API key available to Deep Agents Code

## Linux / DevPod

```bash
git clone https://github.com/podkanowicze/silent-relay-harness-workshop.git
cd silent-relay-harness-workshop

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[agent]"

export DEEPAGENTS_CODE_OPENAI_API_KEY="<key>"
export WORKSHOP_ADMIN_CODE="<private-host-code>"
export WORKSHOP_HOST=0.0.0.0
export WORKSHOP_PARTICIPANTS=12
export WORKSHOP_MIN_PARTICIPANTS=2
export WORKSHOP_ROUTING_MODE=skip_author
export WORKSHOP_DATA_DIR="$PWD/workshop_data/current-run"

python -m workshop_runner
```

Open `http://<devpod-host>:8000/` for participants and
`http://<devpod-host>:8000/admin` for the moderator. Configure the DevPod
ingress or port forwarding for port `8000` when required.

The lobby accepts up to 12 people. It never starts automatically. Once at
least two people have joined, the moderator starts the current roster from
`/admin`.

Use a new `WORKSHOP_DATA_DIR` for every fresh workshop. Do not commit that
directory, the API key, or the moderator code.

## Windows / PowerShell

```powershell
git clone https://github.com/podkanowicze/silent-relay-harness-workshop.git
Set-Location silent-relay-harness-workshop

py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[agent]"

$env:DEEPAGENTS_CODE_OPENAI_API_KEY = "<key>"
$env:WORKSHOP_ADMIN_CODE = "<private-host-code>"
$env:WORKSHOP_HOST = "0.0.0.0"
$env:WORKSHOP_PARTICIPANTS = "12"
$env:WORKSHOP_MIN_PARTICIPANTS = "2"
$env:WORKSHOP_ROUTING_MODE = "skip_author"
$env:WORKSHOP_DATA_DIR = ".\workshop_data\current-run"

python -m workshop_runner
```

Open `http://127.0.0.1:8000/` and `http://127.0.0.1:8000/admin` locally.

## Smoke test without API usage

```bash
python -m pip install -e ".[test]"
python -m pytest
```

To inspect the UI without calling a model, set
`WORKSHOP_AGENT_MODE=mock` before starting the server.

For all settings and operational notes, see [WORKSHOP-APP.md](WORKSHOP-APP.md).
