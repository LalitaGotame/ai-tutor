"""
Step 2 — Zero-Shot Prompting
Explain topics, summarise material, simplify complex text — no examples needed.
Run standalone: python step2_zero_shot.py
"""

import os
from dotenv import load_dotenv
from step1_api_integration import send_single_message

load_dotenv()


def explain_topic(topic: str, level: str = "high school student") -> str:
    prompt = (
        f"Explain the following topic clearly and concisely for a {level}.\n"
        f"Topic: {topic}\n\n"
        f"Structure your explanation with: a one-sentence definition, "
        f"the key ideas (3-5 bullet points), and a real-world analogy."
    )
    return send_single_message(prompt)


def summarise_material(text: str) -> str:
    prompt = (
        f"Summarise the following academic material into clear, concise revision notes.\n"
        f"Include: main ideas, key terms (bold them), and 3-5 takeaway points.\n\n"
        f"Material:\n{text}"
    )
    return send_single_message(prompt)


def simplify_text(text: str) -> str:
    prompt = (
        f"Rewrite the following complex text so a 14-year-old can understand it easily.\n"
        f"Use simple words, short sentences, and an everyday analogy if helpful.\n\n"
        f"Text:\n{text}"
    )
    return send_single_message(prompt)


def run_zero_shot_menu():
    print("\n Step 2: Zero-Shot Prompting ")
    print("1. Explain a topic")
    print("2. Summarise material")
    print("3. Simplify complex text")
    choice = input("\nChoose (1-3): ").strip()

    if choice == "1":
        topic = input("Enter topic: ").strip()
        level = input("Target level (e.g. 'high school student', 'beginner'): ").strip() or "high school student"
        print("\n" + explain_topic(topic, level))

    elif choice == "2":
        print("Paste your text (type END on a new line when done):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        print("\n" + summarise_material("\n".join(lines)))

    elif choice == "3":
        print("Paste complex text (type END on a new line when done):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        print("\n" + simplify_text("\n".join(lines)))

    else:
        print("Invalid choice.")


if __name__ == "__main__":
    run_zero_shot_menu()
