"""Any OpenAI-compatible endpoint: Ollama (local) or a hosted provider.

Switch providers by setting three environment variables, no code changes.
Defaults talk to Ollama on your own computer.

  Ollama (default):
    BASE_URL=http://localhost:11434/v1  API_KEY=ollama  MODEL=qwen3:4b
  Hugging Face (hosted):
    BASE_URL=https://router.huggingface.co/v1  API_KEY=<your HF token>  MODEL=<a model id from huggingface.co/models>

Run:  pip install openai   then   python hello_openai_style.py
Mac/Linux: BASE_URL=... API_KEY=... MODEL=... python hello_openai_style.py
Windows PowerShell: $env:BASE_URL="..."; $env:API_KEY="..."; $env:MODEL="..."; python hello_openai_style.py
"""
import os

from openai import OpenAI

client = OpenAI(
    base_url=os.environ.get("BASE_URL", "http://localhost:11434/v1"),
    api_key=os.environ.get("API_KEY", "ollama"),
)
reply = client.chat.completions.create(
    model=os.environ.get("MODEL", "qwen3:4b"),
    messages=[{"role": "user", "content": "Hello!"}],
)
print(reply.choices[0].message.content)
