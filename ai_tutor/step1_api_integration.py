"""
Step 1 — API Integration
Connects to Gemini, sends messages, and maintains session conversation history.
Run standalone: python step1_api_integration.py
"""

import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()


def get_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    return genai.Client(api_key=api_key)


def run_chat_session():
    """Interactive chat session with full conversation history."""
    print("\n=== Step 1: API Integration — Chat Session ===")
    print("Type 'quit' to exit.\n")

    client = get_client()
    chat = client.chats.create(model="gemini-2.5-flash")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Session ended.")
            break
        if not user_input:
            continue

        response = chat.send_message(user_input)
        print(f"\nGemini: {response.text}\n")

    history = chat.get_history()
    print(f"\n--- Session History ({len(history)} turns) ---")
    for i, msg in enumerate(history, 1):
        role = "You" if msg.role == "user" else "Gemini"
        text = (msg.parts[0].text or "") if msg.parts else ""
        preview = text[:80].replace("\n", " ")
        print(f"  {i}. [{role}]: {preview}{'...' if len(text) > 80 else ''}")


def send_single_message(prompt: str) -> str:
    """Send a single message and return the response text. Used by other steps."""
    client = get_client()
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text or "" 


if __name__ == "__main__":
    run_chat_session()