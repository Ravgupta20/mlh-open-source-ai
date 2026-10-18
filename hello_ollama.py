"""Local model with the Ollama Python library.

Setup:  ollama pull gemma4:e2b   and   pip install ollama
Run:    python hello_ollama.py
"""
import ollama

reply = ollama.chat(
    model="gemma4:e2b",
    messages=[{"role": "user", "content": "Explain what an open-weight AI model is in two sentences."}],
)
print(reply["message"]["content"])
