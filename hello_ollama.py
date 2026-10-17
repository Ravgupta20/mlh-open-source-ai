"""Local model with the Ollama Python library.

Setup:  ollama pull qwen3:4b   and   pip install ollama
Run:    python hello_ollama.py
"""
import ollama

reply = ollama.chat(
    model="qwen3:4b",
    messages=[{"role": "user", "content": "Give me three fun facts about Montgomery County, MD."}],
)
print(reply["message"]["content"])
