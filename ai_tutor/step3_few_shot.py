"""
Step 3 — Few-Shot Prompting
Generate multiple choice quizzes using embedded examples to guide the model.
Run standalone: python step3_few_shot.py
"""

import os
from dotenv import load_dotenv
from step1_api_integration import send_single_message

load_dotenv()

# Embedded few-shot examples that teach the model the exact format we want
FEW_SHOT_EXAMPLES = """
Example 1 — Topic: Photosynthesis, Level: GCSE
Q1. What is the primary pigment used in photosynthesis?
A) Chlorophyll ✓
B) Melanin
C) Haemoglobin
D) Carotene
Explanation: Chlorophyll, found in chloroplasts, absorbs sunlight to drive the light-dependent reactions.

Q2. Which gas is released as a by-product of photosynthesis?
A) Carbon dioxide
B) Nitrogen
C) Oxygen ✓
D) Hydrogen
Explanation: Water molecules are split during the light-dependent stage, releasing oxygen as a by-product.

---

Example 2 — Topic: World War II, Level: A-Level
Q1. The Molotov–Ribbentrop Pact (1939) was a non-aggression treaty between which two countries?
A) Germany and Italy
B) Germany and the Soviet Union ✓
C) Japan and the Soviet Union
D) Italy and the Soviet Union
Explanation: The pact secretly divided Eastern Europe into spheres of influence, enabling Germany to invade Poland without Soviet interference.

Q2. Operation Barbarossa (1941) was Germany's invasion of which country?
A) France
B) Britain
C) the Soviet Union ✓
D) Poland
Explanation: Barbarossa opened the Eastern Front — the largest land theatre of the war — and ultimately overstretched German supply lines.
"""


def generate_quiz(topic: str, level: str = "GCSE", num_questions: int = 5) -> str:
    prompt = (
        f"You are a quiz generator. Using the examples below as your format guide, "
        f"create a {num_questions}-question multiple choice quiz.\n\n"
        f"FORMAT EXAMPLES:\n{FEW_SHOT_EXAMPLES}\n\n"
        f"---\n\n"
        f"Now generate a quiz for:\n"
        f"Topic: {topic}\n"
        f"Level: {level}\n"
        f"Number of questions: {num_questions}\n\n"
        f"Rules:\n"
        f"- 4 options per question (A, B, C, D)\n"
        f"- Mark the correct answer with ✓\n"
        f"- Add a 1-2 sentence explanation after each question\n"
        f"- Questions should progress from easier to harder"
    )
    return send_single_message(prompt)


def run_few_shot_menu():
    print("\n=== Step 3: Few-Shot Prompting — Quiz Generator ===")
    topic = input("Quiz topic: ").strip()
    level = input("Level (e.g. GCSE, A-Level, University): ").strip() or "GCSE"
    num_q = input("Number of questions (default 5): ").strip()
    num_questions = int(num_q) if num_q.isdigit() else 5

    print(f"\nGenerating {num_questions}-question quiz on '{topic}' at {level} level...\n")
    print(generate_quiz(topic, level, num_questions))


if __name__ == "__main__":
    run_few_shot_menu()
