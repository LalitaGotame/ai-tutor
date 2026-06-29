"""
Step 6 — Prompt Templates
Reusable fill-in-the-blank templates for explanation, quiz, notes, and study plan.
Run standalone: python step6_prompt_templates.py
"""

import os
from dotenv import load_dotenv
from step1_api_integration import send_single_message

load_dotenv()

# ── Template definitions ──────────────────────────────────────────────────────

TEMPLATES = {
    "explanation": (
        "You are an expert tutor. Explain the topic '{topic}' to a {level} student.\n"
        "Focus on: {focus}.\n"
        "Use a real-world analogy involving {analogy_context}.\n"
        "Keep the explanation under {max_words} words."
    ),
    "quiz": (
        "Create a {num_questions}-question multiple choice quiz about '{topic}' "
        "for a {level} student.\n"
        "Difficulty: {difficulty}.\n"
        "Topic area to focus on: {subtopic}.\n"
        "Format: Question, then A/B/C/D options, correct answer marked with ✓, "
        "and a brief explanation."
    ),
    "notes": (
        "Create structured revision notes for '{topic}' suitable for a {level} student "
        "preparing for {exam_type} exams.\n"
        "Include: key definitions, main concepts, important formulas or dates (if any), "
        "common exam questions, and a 5-point summary.\n"
        "Style: clear headings, bullet points, concise."
    ),
    "study_plan": (
        "Create a {duration}-week study plan for a {level} student preparing for "
        "their {exam_type} exam in '{subject}'.\n"
        "Available study time per day: {hours_per_day} hours.\n"
        "Weak areas to focus on: {weak_areas}.\n"
        "Include: weekly goals, daily topics, revision techniques, and mock exam timing."
    ),
}


def fill_template(template_name: str, **kwargs) -> str:
    """Fill a named template with keyword arguments and return the prompt."""
    if template_name not in TEMPLATES:
        raise ValueError(f"Unknown template: {template_name}. Available: {list(TEMPLATES.keys())}")
    return TEMPLATES[template_name].format(**kwargs)


def run_template_interactively(template_name: str) -> str:
    """Walk the user through filling in a template interactively."""
    print(f"\n--- Template: {template_name.upper()} ---")

    if template_name == "explanation":
        topic = input("Topic: ").strip()
        level = input("Student level (e.g. GCSE, A-Level): ").strip() or "GCSE"
        focus = input("Focus area (e.g. 'causes and effects'): ").strip() or "core concepts"
        analogy_context = input("Analogy context (e.g. 'everyday cooking'): ").strip() or "everyday life"
        max_words = input("Max words (default 300): ").strip() or "300"
        prompt = fill_template("explanation", topic=topic, level=level,
                               focus=focus, analogy_context=analogy_context, max_words=max_words)

    elif template_name == "quiz":
        topic = input("Topic: ").strip()
        level = input("Student level: ").strip() or "GCSE"
        num_questions = input("Number of questions (default 5): ").strip() or "5"
        difficulty = input("Difficulty (easy/medium/hard): ").strip() or "medium"
        subtopic = input("Specific subtopic to focus on (or 'general'): ").strip() or "general"
        prompt = fill_template("quiz", topic=topic, level=level,
                               num_questions=num_questions, difficulty=difficulty, subtopic=subtopic)

    elif template_name == "notes":
        topic = input("Topic: ").strip()
        level = input("Student level: ").strip() or "A-Level"
        exam_type = input("Exam type (e.g. GCSE, A-Level, University): ").strip() or "A-Level"
        prompt = fill_template("notes", topic=topic, level=level, exam_type=exam_type)

    elif template_name == "study_plan":
        subject = input("Subject: ").strip()
        level = input("Student level: ").strip() or "A-Level"
        exam_type = input("Exam type: ").strip() or "A-Level"
        duration = input("Number of weeks until exam (default 6): ").strip() or "6"
        hours_per_day = input("Study hours per day (default 2): ").strip() or "2"
        weak_areas = input("Weak areas to focus on: ").strip() or "all topics"
        prompt = fill_template("study_plan", subject=subject, level=level,
                               exam_type=exam_type, duration=duration,
                               hours_per_day=hours_per_day, weak_areas=weak_areas)
    else:
        print("Unknown template.")
        return ""

    return send_single_message(prompt)


def run_prompt_templates_menu():
    print("\n Step 6: Prompt Templates")
    print("1. Explanation template")
    print("2. Quiz template")
    print("3. Revision notes template")
    print("4. Study plan template")
    choice = input("\nChoose (1-4): ").strip()

    template_map = {"1": "explanation", "2": "quiz", "3": "notes", "4": "study_plan"}
    if choice not in template_map:
        print("Invalid choice.")
        return

    result = run_template_interactively(template_map[choice])
    print("\n" + result)


if __name__ == "__main__":
    run_prompt_templates_menu()
