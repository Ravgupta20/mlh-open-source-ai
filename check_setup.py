"""Check your setup and say what to fix. Standard library only, so it runs before pip install.

  python check_setup.py                  check Python and local Ollama
  python check_setup.py --model gemma4:e4b
  python check_setup.py --hosted         also test the hosted endpoint from BASE_URL, API_KEY, MODEL
"""
import argparse
import importlib.util
import json
import os
import sys
import urllib.error
import urllib.request

OLLAMA = "http://localhost:11434"
OK, BAD = "PASS", "FAIL"


def get_json(url, headers=None, data=None, timeout=10):
    req = urllib.request.Request(url, headers=headers or {}, data=data)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def check_python():
    v = sys.version_info
    if v >= (3, 10):
        print(f"{OK}  Python {v.major}.{v.minor}")
    else:
        print(f"{BAD}  Python {v.major}.{v.minor} is too old. Install Python 3.10 or newer from https://www.python.org/downloads/ (Windows: tick Add to PATH).")
    print(f"      Running: {sys.executable}")
    missing = [m for m in ("ollama", "openai") if importlib.util.find_spec(m) is None]
    if missing:
        print(f"{BAD}  Not installed for this Python: {', '.join(missing)}.")
        print("      Install them for THIS Python (not a different one), then rerun:")
        print(f'      "{sys.executable}" -m pip install -r requirements.txt')
    else:
        print(f"{OK}  ollama and openai Python packages are installed")


def check_ollama(model):
    try:
        tags = get_json(f"{OLLAMA}/api/tags")
    except (urllib.error.URLError, OSError):
        print(f"{BAD}  Can't reach Ollama at {OLLAMA}.")
        print("      Not installed? Get it from https://ollama.com")
        print("      Installed? Open the Ollama app, or run: ollama serve")
        return
    names = [m["name"] for m in tags.get("models", [])]
    print(f"{OK}  Ollama is running ({len(names)} model(s) downloaded: {', '.join(names) or 'none'})")
    if not any(n == model or n.split(":")[0] == model for n in names):
        print(f"{BAD}  Model {model} isn't downloaded. Run: ollama pull {model}")
        return
    print(f"{OK}  {model} is downloaded")
    body = json.dumps({"model": model, "messages": [{"role": "user", "content": "Say hi in 3 words."}],
                       "stream": False}).encode()
    try:
        out = get_json(f"{OLLAMA}/api/chat", {"Content-Type": "application/json"}, body, timeout=180)
        print(f"{OK}  {model} replied: {out['message']['content'].strip()[:80]!r}")
    except Exception as e:  # noqa: BLE001 - show the reason to a beginner
        print(f"{BAD}  {model} didn't reply ({e}).")
        print("      Often out of memory: try a smaller model (qwen3:1.7b), or use the hosted path.")


HOSTED_HINTS = {
    401: "Wrong or missing API key. Check for a stray space, or the wrong variable name.",
    403: "The key isn't allowed to do this. Check its permissions (token type on Hugging Face).",
    404: "Wrong BASE_URL or MODEL name. Ollama's URL must end in /v1.",
    429: "Rate limit or free credits used up. Wait, switch provider, or run local.",
}


def check_hosted():
    base = os.environ.get("BASE_URL")
    key = os.environ.get("API_KEY")
    model = os.environ.get("MODEL")
    if not (base and key and model):
        print(f"{BAD}  Set BASE_URL, API_KEY and MODEL first (see hello_openai_style.py).")
        return
    body = json.dumps({"model": model, "max_tokens": 5,
                       "messages": [{"role": "user", "content": "Hi"}]}).encode()
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    try:
        get_json(base.rstrip("/") + "/chat/completions", headers, body, timeout=60)
        print(f"{OK}  Hosted endpoint answered ({base}, model {model})")
    except urllib.error.HTTPError as e:
        print(f"{BAD}  Hosted endpoint returned HTTP {e.code}. {HOSTED_HINTS.get(e.code, 'See the provider docs.')}")
    except (urllib.error.URLError, OSError) as e:
        print(f"{BAD}  Can't reach {base} ({e}). Check Wi-Fi and the URL.")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--model", default="gemma4:e2b")
    p.add_argument("--hosted", action="store_true")
    a = p.parse_args()
    check_python()
    check_ollama(a.model)
    if a.hosted:
        check_hosted()
