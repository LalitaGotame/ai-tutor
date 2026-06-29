"""
Step 8 — Memory System
Personalised tutoring session with persistent conversation history.
Run standalone: python step8_memory_system.py
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic.chains import ConversationChain
from langchain_core.prompts import PromptTemplate

load_dotenv()


class TutorMemorySession:
    def __init__(self):
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=api_key,
            temperature=0.7,
        )
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            human_prefix="Student",
            ai_prefix="Tutor",
        )
        self.user_profile = {"name": "Student", "subject": "General", "level": "A-Level"}

    def set_profile(self, name: str, subject: str, level: str):
        self.user_profile = {"name": name, "subject": subject, "level": level}

    def chat(self, user_input: str) -> str:
        p = self.user_profile
        prompt = PromptTemplate(
            input_variables=["chat_history", "input"],
            template=(
                f"You are a helpful AI tutor. The student's name is {p['name']}. "
                f"They study {p['subject']} at {p['level']} level. "
                f"Always address them by name and remember previous discussion.\n\n"
                "Conversation so far:\n{chat_history}\n\n"
                "Student: {input}\nTutor:"
            ),
        )
        chain = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            prompt=prompt,
            verbose=False,
        )
        return chain.predict(input=user_input)

    def show_history(self):
        messages = self.memory.chat_memory.messages
        if not messages:
            print("No conversation history yet.")
            return
        print(f"\n--- Conversation History ({len(messages)} messages) ---")
        for msg in messages:
            role = "Student" if msg.type == "human" else "Tutor"
            # msg.content can be str or list — convert to str safely
            content = (
                msg.content
                if isinstance(msg.content, str)
                else " ".join(
                    part if isinstance(part, str) else str(part)
                    for part in msg.content
                )
            )
            preview = content[:100].replace("\n", " ")
            print(f"  [{role}]: {preview}{'...' if len(content) > 100 else ''}")

    def clear_history(self):
        self.memory.clear()
        print("Conversation history cleared.")


def run_memory_session():
    print("\nStep 8: Memory System — Personalised Tutoring Session")

    session = TutorMemorySession()
    name    = input("What's your name? ").strip() or "Student"
    subject = input("What subject are you studying? ").strip() or "General Studies"
    level   = input("Level (e.g. GCSE, A-Level, University): ").strip() or "A-Level"
    session.set_profile(name, subject, level)

    print(f"\nWelcome, {name}! I'll remember our conversation as we go.")
    print("Commands: 'history' | 'clear' | 'quit'\n")

    while True:
        user_input = input(f"{name}: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("Session ended. Goodbye!")
            break
        elif user_input.lower() == "history":
            session.show_history()
        elif user_input.lower() == "clear":
            session.clear_history()
        elif user_input:
            print(f"\nTutor: {session.chat(user_input)}\n")


if __name__ == "__main__":
    run_memory_session()