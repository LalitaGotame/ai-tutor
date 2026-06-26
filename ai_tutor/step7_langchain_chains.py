"""
Step 7 — LangChain Chains
Sequential pipeline: Topic → Explanation → Revision Notes → Quiz.
Run standalone: python step7_langchain_chains.py
"""

import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

load_dotenv()


def build_tutor_chain(llm):
    """Build a 3-step LCEL pipeline: explain → notes → quiz."""

    # ── Prompt templates ──────────────────────────────────────────────────────
    explanation_prompt = PromptTemplate(
        input_variables=["topic", "level"],
        template=(
            "Explain '{topic}' clearly for a {level} student.\n"
            "Cover: what it is, why it matters, and the 3 most important ideas.\n"
            "Keep it under 250 words."
        ),
    )

    notes_prompt = PromptTemplate(
        input_variables=["topic", "explanation"],
        template=(
            "Using the explanation below, create concise revision notes for '{topic}'.\n\n"
            "EXPLANATION:\n{explanation}\n\n"
            "Format:\n"
            "• Key definitions (2-3)\n"
            "• Main points (bullet list)\n"
            "• A memorable summary sentence"
        ),
    )

    quiz_prompt = PromptTemplate(
        input_variables=["topic", "revision_notes"],
        template=(
            "Based on these revision notes for '{topic}', create a 3-question MCQ quiz.\n\n"
            "REVISION NOTES:\n{revision_notes}\n\n"
            "Each question: 4 options (A-D), correct answer marked ✓, brief explanation."
        ),
    )

    parser = StrOutputParser()

    # ── LCEL chains ───────────────────────────────────────────────────────────
    explanation_chain = explanation_prompt | llm | parser
    notes_chain       = notes_prompt       | llm | parser
    quiz_chain        = quiz_prompt        | llm | parser

    return explanation_chain, notes_chain, quiz_chain


def run_langchain_pipeline(topic: str, level: str = "A-Level") -> dict:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0.7,
    )

    explanation_chain, notes_chain, quiz_chain = build_tutor_chain(llm)

    explanation   = explanation_chain.invoke({"topic": topic, "level": level})
    revision_notes = notes_chain.invoke({"topic": topic, "explanation": explanation})
    quiz          = quiz_chain.invoke({"topic": topic, "revision_notes": revision_notes})

    return {
        "explanation": explanation,
        "revision_notes": revision_notes,
        "quiz": quiz,
    }


def run_langchain_menu():
    print("\n=== Step 7: LangChain Sequential Pipeline ===")
    print("Pipeline: Topic → Explanation → Revision Notes → Quiz\n")

    topic = input("Topic to study: ").strip()
    level = input("Student level (default: A-Level): ").strip() or "A-Level"

    print(f"\nRunning full pipeline for '{topic}' at {level}...\n")

    result = run_langchain_pipeline(topic, level)

    print("\n📖 EXPLANATION\n" + "─" * 60)
    print(result["explanation"])

    print("\n📝 REVISION NOTES\n" + "─" * 60)
    print(result["revision_notes"])

    print("\n❓ QUIZ\n" + "─" * 60)
    print(result["quiz"])


if __name__ == "__main__":
    run_langchain_menu()
