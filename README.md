# MLH Open Source AI

The smallest working setup for talking to an open-weight AI model, locally or
through a hosted endpoint. Made for the Hacktoberfest Hack Day, Bethesda x
Code & Coffee (theme: "AI Belongs to Everyone"). MIT licensed: copy it, change it,
build on it.

## Quick start

1. **Pick a path.**
   - 8 GB of RAM or more: run a small model on your own computer (Local).
   - Less RAM, or you don't want a big download: use a hosted endpoint (Hosted).
2. **Check your setup any time:** `python check_setup.py` tells you what to fix.

### Local (Ollama)

```
ollama pull qwen3:4b        # 2.5 GB, do this on good Wi-Fi
pip install -r requirements.txt
python hello_ollama.py
```

Get Ollama from https://ollama.com. Other models to try: `gemma4:e4b`,
`qwen3:1.7b` (smaller), `qwen2.5-coder:7b` (code). Rule of thumb: 8 GB RAM runs
about a 4B model, 16 GB runs 7 to 8B.

### Hosted (any OpenAI-compatible endpoint)

`hello_openai_style.py` reads three environment variables, so you change
providers without touching the code. It defaults to local Ollama.

| Variable | Ollama (default) | Hugging Face |
|---|---|---|
| `BASE_URL` | `http://localhost:11434/v1` | `https://router.huggingface.co/v1` |
| `API_KEY` | `ollama` (any text) | your token from huggingface.co/settings/tokens |
| `MODEL` | `qwen3:4b` | a model id from huggingface.co/models |

```
pip install -r requirements.txt
# Mac/Linux
BASE_URL=https://router.huggingface.co/v1 API_KEY=hf_xxx MODEL=<model-id> python hello_openai_style.py
# Windows PowerShell
$env:BASE_URL="https://router.huggingface.co/v1"; $env:API_KEY="hf_xxx"; $env:MODEL="<model-id>"; python hello_openai_style.py
```

Never put a real key in a file you commit. Use environment variables, and keep
a `.env` file out of git (this repo's `.gitignore` already does).

Free tiers are small (Hugging Face free accounts get about $0.10 a month in
credits), so a hosted demo can run out. Have the local path ready as a backup.

## Debugging

Run `python check_setup.py` first (`--hosted` also tests your hosted endpoint).
Then match your symptom:

| Symptom | Likely cause and fix |
|---|---|
| Connection refused on port 11434 | Ollama isn't running. Open the Ollama app, or run `ollama serve`. |
| Model not found | `ollama pull <name>`, then check with `ollama list`. |
| Very slow, or the computer freezes | Model too big for your RAM. Use a 1 to 4B model (`qwen3:1.7b`), or go hosted. |
| `401` from a hosted API | Wrong or missing key. Look for a stray space or the wrong variable name. |
| `403` | The key lacks permission. On Hugging Face, check the token type. |
| `404` | Wrong `BASE_URL` or `MODEL`. For Ollama the URL must end in `/v1`. |
| `429` or "credits used up" | Free tier exhausted. Wait, switch provider, or run local. |
| `ModuleNotFoundError: ollama` or `openai` | `pip install -r requirements.txt`, in the same Python you run the script with. |
| `pip` not found | Try `python -m pip install -r requirements.txt` (or `python3`). |
| Download crawls | Shared Wi-Fi. Use a phone hotspot, or start the download at home. |

Tip: the OpenAI-style call works with Ollama, Hugging Face and many others. Write
your code once and change only `BASE_URL`, `API_KEY` and `MODEL`.

## For the hackathon

- Prizes: Best Open-Source AI Project runs at every Hack Day. "Best Use of Gemma 4"
  needs a Gemma model through the Gemini API (Gemma in Ollama doesn't count).
  Confirm the other challenges at kickoff.
- Submit by pencils-down on the event page (Challenges, Add Submission): project
  name, one-line description, repo link.
- Your repo needs a license and a README that names the model you used.
- Help: ask in `#moco-general` on the Code & Coffee Discord, or find a host.

## Files

- `hello_ollama.py`: chat with a local model.
- `hello_openai_style.py`: same idea, any OpenAI-compatible endpoint.
- `check_setup.py`: standard-library script that diagnoses your setup.
