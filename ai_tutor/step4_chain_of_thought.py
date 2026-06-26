"""
Step 4 — Chain-of-Thought Prompting
Solve maths and logic problems step by step, ending with 'Final Answer:'.
Run standalone: python step4_chain_of_thought.py
"""

import os
from dotenv import load_dotenv
from step1_api_integration import send_single_message

load_dotenv()


def solve_maths(problem: str) -> str:
    prompt = (
        f"Solve the following maths problem step by step. "
        f"Show every calculation clearly, explain each step in plain English, "
        f"and end your response with exactly this line: 'Final Answer: [answer]'\n\n"
        f"Problem: {problem}"
    )
    return send_single_message(prompt)


def solve_logic(problem: str) -> str:
    prompt = (
        f"Solve the following logic problem step by step. "
        f"Work through the reasoning carefully, state each deduction explicitly, "
        f"and end your response with exactly this line: 'Final Answer: [answer]'\n\n"
        f"Problem: {problem}"
    )
    return send_single_message(prompt)


def solve_word_problem(problem: str) -> str:
    prompt = (
        f"You are a patient maths tutor. Solve this word problem step by step:\n\n"
        f"1. First identify what is being asked.\n"
        f"2. List the known information.\n"
        f"3. Choose the right method/formula.\n"
        f"4. Work through each calculation step.\n"
        f"5. Check your answer makes sense.\n"
        f"End with: 'Final Answer: [answer with units]'\n\n"
        f"Problem: {problem}"
    )
    return send_single_message(prompt)


def run_chain_of_thought_menu():
    print("\n=== Step 4: Chain-of-Thought Problem Solver ===")
    print("1. Maths problem")
    print("2. Logic puzzle")
    print("3. Word problem")
    choice = input("\nChoose (1-3): ").strip()

    problem = input("Enter your problem: ").strip()

    if choice == "1":
        print("\n" + solve_maths(problem))
    elif choice == "2":
        print("\n" + solve_logic(problem))
    elif choice == "3":
        print("\n" + solve_word_problem(problem))
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    run_chain_of_thought_menu()
