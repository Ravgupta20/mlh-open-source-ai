"""Local model with the Ollama Python library.

Setup:  ollama pull gemma4:e2b   and   pip install ollama
Run:    python hello_ollama.py
"""
import ollama

reply = ollama.chat(
    model="gemma4:e2b",
    messages=[{"role": "user", "content": "Give me three fun facts about Montgomery County, MD."}],
)
print(reply["message"]["content"])
