# MLH Open Source AI

Talk to an open-weight AI model on your own computer, or through a hosted
service, in about 10 minutes. Made for the Hacktoberfest Hack Day, Bethesda x
Code & Coffee ("AI Belongs to Everyone"). MIT licensed: copy it, change it, build on it.

## Pick a path

| | Local | Hosted |
|---|---|---|
| Runs on | your computer (free, private, works offline) | someone else's servers |
| You need | 8 GB+ RAM and a ~4 GB download | an account and an API key |
| Watch out for | slow on older laptops | free credits run out |

Not sure? Start with Local. Do the downloads at home, not on shared Wi-Fi.

## Step 1: Python

You need Python 3.10 or newer. Check what you have:

```
python --version
```

On Mac/Linux try `python3 --version`. On Windows try `py --version`.

**Not found, or older than 3.10?** Install it from https://www.python.org/downloads/.
On Windows, tick **Add python.exe to PATH** in the installer, then open a new terminal.

**`python` says "not found" or "not recognized"?** Your computer may call it something
else. Try these, and use whichever one prints a version:

| Your computer | Use this instead of `python` | And this instead of `pip` |
|---|---|---|
| Mac / Linux | `python3` | `python3 -m pip` |
| Windows | `py` | `py -m pip` |

Then use that name everywhere in this guide, for both installing and running, and always write `-m pip` instead of bare `pip`. Computers with two Pythons install into one and run the other. For example, on Windows:

```
py -m pip install -r requirements.txt
py hello_ollama.py
```

## Step 2: Get the code

```
git clone https://github.com/Ravgupta20/mlh-open-source-ai
cd mlh-open-source-ai
pip install -r requirements.txt
```

(Use `python3` or `py` here if `python` didn't work in Step 1.)

No git? On the repo page choose **Code, Download ZIP**, unzip it, and open a
terminal in that folder.

## Step 3A: Local (Ollama)

**1. Install Ollama** from https://ollama.com/download, then open a new terminal and check:

```
ollama --version
```

**2. Download the model** (about 4 GB, a few minutes on good Wi-Fi):

```
ollama pull gemma4:e2b
```

**3. Chat with it** in the terminal:

```
ollama run gemma4:e2b
```

You'll see a `>>>` prompt. Type a question and press Enter, for example:

```
>>> Explain what an open-weight AI model is in two sentences.
```

The first answer can take a minute while the model loads into memory. Later answers
are faster. When you're done, type `/bye` to quit. This step works even if you skip Python.

**4. Call it from Python:**

```
python hello_ollama.py
```

(`python3` or `py` if that's what worked in Step 1.)

Other models: `gemma4:e4b` (bigger, better), `qwen3:4b`, `qwen3:1.7b` (smaller).
`gemma4:e2b` is Google's small open model and fits a laptop with 8 GB of RAM.

## Step 3B: Hosted

`hello_openai_style.py` works with any OpenAI-compatible service. You switch
providers with three environment variables, and the code doesn't change.

| Variable | Ollama (default) | Hugging Face |
|---|---|---|
| `BASE_URL` | `http://localhost:11434/v1` | `https://router.huggingface.co/v1` |
| `API_KEY` | `ollama` (any text) | your token from huggingface.co/settings/tokens |
| `MODEL` | `gemma4:e2b` | a model id from huggingface.co/models |

Mac/Linux:

```
BASE_URL=https://router.huggingface.co/v1 API_KEY=hf_xxx MODEL=<model-id> python hello_openai_style.py
```

Windows PowerShell:

```
$env:BASE_URL="https://router.huggingface.co/v1"
$env:API_KEY="hf_xxx"
$env:MODEL="<model-id>"
python hello_openai_style.py
```

Never commit a real key. Use environment variables, and keep any `.env` file out
of git (this repo's `.gitignore` already does). Free tiers are small (Hugging
Face gives about $0.10 a month), so keep the Local path as a backup.

## Something broke?

Run this first. It checks your setup and tells you what to fix:

```
python check_setup.py
python check_setup.py --hosted     # also tests your hosted endpoint
```

Then find your symptom:

| Symptom | Fix |
|---|---|
| `python` or `pip` "not found" or "not recognized" | Try `python3` (Mac/Linux) or `py` (Windows) instead of `python`, and `python3 -m pip` or `py -m pip` instead of `pip`. Still nothing? Install Python (Step 1), tick Add to PATH on Windows, and open a new terminal. |
| `No module named pip` | That Python was installed without pip. Run `py -m ensurepip --upgrade` (Windows) or `python3 -m ensurepip --upgrade` (Mac/Linux), then `py -m pip install -r requirements.txt` again. |
| `ModuleNotFoundError: No module named 'ollama'` (or `openai`) | You installed the packages into a different Python than the one running the script. Install with the same name you run with: `py -m pip install -r requirements.txt` (Windows) or `python3 -m pip install -r requirements.txt` (Mac/Linux). Avoid bare `pip`. `python check_setup.py` prints the exact command for the Python you're using. |
| Connection refused on port 11434 | Ollama isn't running. Open the Ollama app, or run `ollama serve`. |
| Model not found | Run `ollama pull gemma4:e2b`, then `ollama list` to check. |
| Very slow, or the computer freezes | Model too big for your RAM. Try `qwen3:1.7b`, or go hosted. |
| `401` from a hosted API | Wrong or missing key. Look for a stray space or a misspelled variable name. |
| `403` | The key lacks permission. On Hugging Face, check the token type. |
| `404` | Wrong `BASE_URL` or `MODEL`. For Ollama the URL must end in `/v1`. |
| `429` or "credits used up" | Free tier is empty. Wait, switch provider, or run Local. |
| Download crawls | Shared Wi-Fi. Use a phone hotspot, or start it at home. |

## Files

| File | What it does |
|---|---|
| `hello_ollama.py` | Chat with a local model |
| `hello_openai_style.py` | Same, for any OpenAI-compatible service |
| `check_setup.py` | Diagnoses your setup (standard library only) |
