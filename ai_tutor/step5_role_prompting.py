"""
Step 5 — Role Prompting
Switch between Teacher, Examiner, Study Coach, and Subject Expert personas.
Run standalone: python step5_role_prompting.py
"""

import os
from dotenv import load_dotenv
import google.genai as genai
from google.genai import types

load_dotenv()

PERSONAS = {
    "1": {
        "name": "Teacher",
        "system": (
            "You are an encouraging, patient classroom teacher. Help students understand "
            "concepts clearly using simple language, relatable analogies, and a warm, supportive "
            "tone. Break down complex ideas into manageable steps. Always offer to clarify."
        ),
    },
    "2": {
        "name": "Examiner",
        "system": (
            "You are a strict but fair academic examiner. Ask probing questions, assess responses "
            "critically using mark scheme language. Highlight what earns marks and what loses them. "
            "Be direct and formal. Point out gaps and suggest exactly what needs improving."
        ),
    },
    "3": {
        "name": "Study Coach",
        "system": (
            "You are an energetic, motivating study coach specialising in learning strategies and "
            "exam technique. Help students plan revision, manage exam anxiety, and use techniques "
            "like spaced repetition and active recall. Give practical, actionable advice."
        ),
    },
    "4": {
        "name": "Subject Expert",
        "system": (
            "You are a world-class academic subject expert speaking to an advanced student. "
            "Go deep into nuances and complexities, reference research and real-world applications, "
            "use advanced terminology (with explanation), and challenge assumptions critically."
        ),
    },
}


def run_role_prompting_menu():
    print("\nStep 5: Role Prompting — AI Personas")
    for key, persona in PERSONAS.items():
        print(f"{key}. {persona['name']}")

    choice = input("\nChoose a persona (1-4): ").strip()
    if choice not in PERSONAS:
        print("Invalid choice.")
        return

    persona = PERSONAS[choice]
    print(f"\n--- Now speaking as: {persona['name']} ---")
    print("Type 'quit' to exit or 'switch' to change persona.\n")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=persona["system"],
        ),
    )

    while True:
        user_input = input(f"You → {persona['name']}: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if user_input.lower() == "switch":
            run_role_prompting_menu()
            return
        if not user_input:
            continue

        response = chat.send_message(user_input)
        print(f"\n{persona['name']}: {response.text}\n")


if __name__ == "__main__":
    run_role_prompting_menu()
