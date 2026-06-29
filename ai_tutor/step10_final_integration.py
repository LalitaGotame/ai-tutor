"""
Step 10 — Final Integration
The main console app combining all 10 features in one numbered menu.
Run this file to launch the AI Academic Tutor:  python step10_final_integration.py
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

# ── Global user name (set once at startup) ────────────────────────────────────
USER_NAME = ""

# ── Validate API key before doing anything ────────────────────────────────────
def check_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key or key == "your_key_here":
        print("\n  GEMINI_API_KEY not set!")
        print("   Open the .env file and replace 'your_key_here' with your actual key.")
        print("   Get a free key at: https://aistudio.google.com/app/apikey\n")
        sys.exit(1)

# ── Import all step modules ───────────────────────────────────────────────────
def import_steps():
    """Lazy-import all step modules so startup is fast and errors are local."""
    global step1, step2, step3, step4, step5, step6, step7, step8, step9
    try:
        import step1_api_integration as step1
        import step2_zero_shot as step2
        import step3_few_shot as step3
        import step4_chain_of_thought as step4
        import step5_role_prompting as step5
        import step6_prompt_templates as step6
        import step7_langchain_chains as step7
        import step8_memory_system as step8
        import step9_agents_tools as step9
    except ImportError as e:
        print(f"\n     Import error: {e}")
        print("   Make sure you've run:  pip install -r requirements.txt\n")
        sys.exit(1)

# ── Ask for user's name at startup ────────────────────────────────────────────
def greet_user():
    """Prompt for the user's name and store it globally."""
    global USER_NAME
    print("     Welcome to the AI Academic Tutor! ")
    while True:
        name = input("\n  What's your name? ").strip()
        if name:
            USER_NAME = name
            break
        print("  Please enter your name to continue.")
    print(f"\n  Hello, {USER_NAME}! Great to have you here.")
    print(f"  I'll remember your name throughout our session.\n")

# ── Personalised banner ───────────────────────────────────────────────────────
def get_banner():
    return f"""
    Hi, {USER_NAME}! Choose one from menu:
 
   1   Chat with Tutor
   2   Explain / Summarise / Simplify
   3   Multiple Choice Quiz Generator
   4   Step-by-Step Problem Solver
   5   Switch AI Persona
   6   Templates
   7   Full Topic Pipeline
   8   Personalised Session Memory
   9   AI Agent (Calc / Planner / Sum.)
  10   About
   0   Exit
"""

ABOUT_TEXT_TEMPLATE = """
  About This App  ({name}'s session)
  
  Demonstrates 9 prompting and LangChain techniques,
  all powered by Google Gemini.

  1   Just start chatting. Great for quick Q&As.
  2   Paste notes for a summary, or explain any topic.
  3   Enter a subject + level to get a full MCQ quiz.
  4   Paste a maths problem — see every step.
  5   Pick Teacher, Examiner, Coach, or Expert.
  6   Structured templates for notes and study plans.
  7   One topic → explanation + revision notes + quiz.
  8   The AI remembers your name, subject, and level.
  9   Free-form questions; the agent picks the right tool.
"""


def separator(title: str = ""):
    if title:
        print(f"\n  {title}\n  " + "─" * 40)
    else:
        print()


def pause():
    input(f"\n  [Press Enter to continue, {USER_NAME}]")


# ── Inject user name into step modules ───────────────────────────────────────
def inject_user_name():
    """
    Pass the user's name into any step module that exposes a set_user_name()
    function.  Modules that don't have it are silently skipped.
    """
    for mod in (step1, step2, step3, step4, step5, step6, step7, step8, step9):
        if hasattr(mod, "set_user_name"):
            mod.set_user_name(USER_NAME)


# ── Feature wrappers ──────────────────────────────────────────────────────────
def feature_1():
    separator(f"Chat with Gemini  —  {USER_NAME}'s session")
    step1.run_chat_session()

def feature_2():
    separator(f"Zero-Shot Prompting  —  {USER_NAME}'s session")
    step2.run_zero_shot_menu()

def feature_3():
    separator(f"Quiz Generator  —  {USER_NAME}'s session")
    step3.run_few_shot_menu()

def feature_4():
    separator(f"Problem Solver  —  {USER_NAME}'s session")
    step4.run_chain_of_thought_menu()

def feature_5():
    separator(f"AI Personas  —  {USER_NAME}'s session")
    step5.run_role_prompting_menu()

def feature_6():
    separator(f"Prompt Templates  —  {USER_NAME}'s session")
    step6.run_prompt_templates_menu()

def feature_7():
    separator(f"LangChain Pipeline  —  {USER_NAME}'s session")
    step7.run_langchain_menu()

def feature_8():
    separator(f"Memory Session  —  {USER_NAME}'s session")
    step8.run_memory_session()

def feature_9():
    separator(f"Agent with Tools  —  {USER_NAME}'s session")
    step9.run_agents_menu()

def feature_about():
    print(ABOUT_TEXT_TEMPLATE.format(name=USER_NAME))


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    check_api_key()

    # 1. Ask for the user's name BEFORE anything else
    greet_user()

    # 2. Load step modules
    import_steps()

    # 3. Share the name with every step module that wants it
    inject_user_name()

    feature_map = {
        "1": feature_1,
        "2": feature_2,
        "3": feature_3,
        "4": feature_4,
        "5": feature_5,
        "6": feature_6,
        "7": feature_7,
        "8": feature_8,
        "9": feature_9,
        "10": feature_about,
    }

    while True:
        print(get_banner())
        choice = input(f"  {USER_NAME}, enter a number (0–10): ").strip()

        if choice == "0":
            print(f"\n  Goodbye, {USER_NAME}! Keep learning! \n")
            break

        if choice in feature_map:
            try:
                feature_map[choice]()
            except KeyboardInterrupt:
                print(f"\n\n  [Interrupted — returning to menu, {USER_NAME}]")
            except Exception as e:
                print(f"\n  Error in feature {choice}: {e}")
                print("  Check your .env file and internet connection.")
            pause()
        else:
            print("  Invalid choice. Enter a number from 0 to 10.")


if __name__ == "__main__":
    main()