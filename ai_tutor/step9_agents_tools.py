"""
Step 9 — Agents & Tools
AI agent with Calculator, Study Planner, and Info Summarizer tools,
using ZERO_SHOT_REACT_DESCRIPTION.
Run standalone: python step9_agents_tools.py
"""

import os
import math
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_classic.agents import initialize_agent, AgentType, Tool

load_dotenv()


# Calculator 

def calculator_tool(expression: str) -> str:
    try:
        safe_dict = {
            "sqrt": math.sqrt, "sin": math.sin, "cos": math.cos,
            "tan": math.tan, "log": math.log, "log10": math.log10,
            "abs": abs, "round": round, "pi": math.pi, "e": math.e,
            "pow": pow, "__builtins__": {},
        }
        result = eval(expression.strip(), {"__builtins__": {}}, safe_dict)
        return f"Result: {result}"
    except Exception as ex:
        return f"Calculator error: {ex}. Use a valid expression like 'sqrt(144) + 5 * 3'."


#Study Planner 

def study_planner_tool(query: str) -> str:
    parts    = [p.strip() for p in query.split(",")]
    duration = parts[0] if len(parts) > 0 else "4 weeks"
    subject  = parts[1] if len(parts) > 1 else "the subject"
    level    = parts[2] if len(parts) > 2 else "A-Level"
    hours    = parts[3] if len(parts) > 3 else "2 hours/day"

    return (
        f"STUDY PLAN — {subject} | {level} | {duration} | {hours}\n\n"
        f"Week 1: Foundation — core concepts, key definitions, read chapters 1-3\n"
        f"Week 2: Depth — past paper questions, identify weak areas\n"
        f"Week 3: Consolidation — flashcards, mind maps, timed practice\n"
        f"Week 4+: Mock exams — full timed papers, review mistakes, final notes\n\n"
        f"Daily: 20 min review → 60 min new material → 20 min active recall\n"
        f"Technique: Spaced repetition + Pomodoro (25 min work / 5 min break)"
    )


# ── Tool 3: Info Summarizer ───────────────────────────────────────────────────

def info_summarizer_tool(text: str) -> str:
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if len(s.strip()) > 20]
    if not sentences:
        return "No meaningful content found to summarise."

    picks = [sentences[0]]
    if len(sentences) > 2:
        picks.append(sentences[len(sentences) // 2])
    if len(sentences) > 1:
        picks.append(sentences[-1])

    out = "KEY POINTS:\n"
    for i, s in enumerate(picks, 1):
        out += f"  {i}. {s}.\n"
    out += f"\n(Processed {len(sentences)} sentences)"
    return out


#Agent

def build_agent():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0,
    )

    tools = [
        Tool(
            name="Calculator",
            func=calculator_tool,
            description=(
                "Use for mathematical calculations. "
                "Input must be a math expression string, e.g. 'sqrt(144) + 5 * 3'. "
                "Supports: +, -, *, /, **, sqrt(), sin(), cos(), log(), abs(), round(), pi, e."
            ),
        ),
        Tool(
            name="StudyPlanner",
            func=study_planner_tool,
            description=(
                "Creates a study plan. Input a comma-separated string: "
                "'duration, subject, level, daily hours'. "
                "Example: '4 weeks, Biology, GCSE, 1.5 hours/day'"
            ),
        ),
        Tool(
            name="InfoSummarizer",
            func=info_summarizer_tool,
            description=(
                "Summarises academic text into key points. "
                "Input the plain text you want summarised."
            ),
        ),
    ]

    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )


def run_agents_menu():
    print("\nStep 9: AI Agent with Tools")
    print("Tools: Calculator, StudyPlanner, InfoSummarizer")
    print("Try: 'What is sqrt(256) + 10?' or 'Make a 4-week plan for Chemistry A-Level'")
    print("Type 'quit' to exit.\n")

    agent = build_agent()

    while True:
        query = input("Your request: ").strip()
        if query.lower() in ("quit", "exit", "q"):
            break
        if not query:
            continue
        try:
            result = agent.run(query)
            print(f"\nAgent Result:\n{result}\n")
        except Exception as e:
            print(f"Agent error: {e}\n")


if __name__ == "__main__":
    run_agents_menu()
