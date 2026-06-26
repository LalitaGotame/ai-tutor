# AI-Powered Academic Tutor

A console-based AI tutor built with **Python**, **LangChain**, and **Google Gemini**,
designed to help students learn, revise, and prepare for exams through
intelligent conversation, structured prompting, reasoning, and tool-based
assistance.

This project was built to fulfill a Generative AI course assignment that
required implementing 10 progressive modules — from basic LLM API calls all
the way to a tool-using AI agent with memory — and combining them into one
working application.

---

## Table of Contents

1. [What This Project Does](#what-this-project-does)
2. [Key Features](#key-features)
3. [How It Works (Architecture)](#how-it-works-architecture)
4. [Folder Structure](#folder-structure)
5. [Requirements](#requirements)
6. [Getting a Free API Key](#getting-a-free-api-key)
7. [Setup & Running — Windows](#setup--running--windows)
8. [Setup & Running — macOS](#setup--running--macos)
9. [Setup & Running — Linux](#setup--running--linux)
10. [Running Individual Modules](#running-individual-modules)
11. [Troubleshooting](#troubleshooting)
12. [Assignment Step Mapping](#assignment-step-mapping)
13. [Limitations](#limitations)
14. [Future Enhancements](#future-enhancements)

---

## What This Project Does

The AI Academic Tutor simulates a personalized tutor that can:

- Answer academic questions and explain concepts in simple language
- Summarize study material and simplify complex topics
- Generate quizzes and categorized answers in a consistent format
- Solve reasoning-based problems step-by-step (Chain-of-Thought)
- Switch between different tutor personas: **Teacher, Examiner, Study Coach, Subject Expert**
- Use reusable prompt templates for explanations, quizzes, notes, and study plans
- Run a multi-stage pipeline: **Topic → Explanation → Notes → Quiz**
- Remember a student's identity and learning history across sessions
- Use an AI agent equipped with tools (**calculator**, **study planner**,
  **information summarizer**) that reasons about which tool to use and when

All of this is wired together into one interactive console menu in `main.py`.

---

## Key Features

| Capability                  | Module                      |
|------------------------------|------------------------------|
| LLM API connection + chat history | `step1_api_integration.py` |
| Zero-shot explain/summarize/simplify | `step2_zero_shot.py` |
| Few-shot quiz & categorized answers | `step3_few_shot.py` |
| Chain-of-Thought problem solving | `step4_chain_of_thought.py` |
| Multi-role tutor personas | `step5_role_prompting.py` |
| Reusable prompt template library | `step6_prompt_templates.py` |
| Sequential LangChain pipeline | `step7_langchain_chains.py` |
| Persistent student memory | `step8_memory_system.py` |
| Tool-using AI agent | `step9_agents_tools.py` |
| Unified console application | `main.py` |

---

## How It Works (Architecture)

```
                    ┌─────────────────┐
                    │     main.py      │   <- console menu / entry point
                    └────────┬────────┘
                             │ imports & calls
        ┌────────┬────────┬─┴──┬────────┬────────┬────────┬────────┬────────┐
        ▼        ▼        ▼    ▼        ▼        ▼        ▼        ▼        ▼
     Step 1   Step 2   Step 3 Step 4  Step 5   Step 6   Step 7   Step 8   Step 9
     (API)   (Zero-   (Few-  (CoT)   (Roles) (Templates)(Chains)(Memory) (Agent+
             shot)    shot)                                              Tools)
        │        │        │    │        │        │        │        │        │
        └────────┴────────┴────┴────────┴────────┴────────┴────────┴────────┘
                             │
                             ▼
                   ┌───────────────────┐
                   │     config.py     │  <- loads GOOGLE_API_KEY,
                   └─────────┬─────────┘     builds the shared Gemini LLM
                             ▼
                  Google Gemini API (free tier)
```

Every module gets its LLM instance from `config.py`, so the API key and model
name are configured in exactly one place. `main.py` keeps a single
`TutorSession` (chat memory) and a single `StudentMemory` (learning history)
alive for the whole run, so personalization carries across every feature the
student uses in one sitting.

---

## Folder Structure

```
ai_tutor/
├── .env                        ← GEMINI_API_KEY=your_key_here
├── .gitignore                  ← contains .env and venv/
├── requirements.txt            ← all dependencies
├── step1_api_integration.py    ← Gemini API chat session
├── step2_zero_shot.py          ← Explain / Summarise / Simplify
├── step3_few_shot.py           ← MCQ Quiz Generator
├── step4_chain_of_thought.py   ← Step-by-Step Problem Solver
├── step5_role_prompting.py     ← AI Personas (Teacher / Examiner / Coach / Expert)
├── step6_prompt_templates.py   ← Reusable Prompt Templates
├── step7_langchain_chains.py   ← LangChain Sequential Pipeline
├── step8_memory_system.py      ← Conversation Memory
├── step9_agents_tools.py       ← AI Agent with Tools
└── step10_final_integration.py ← Main App (run this)
```

---

## Requirements

- **Python 3.10 or newer** (Python 3.12 recommended — LangChain 1.x requires
  at least 3.10)
- A free Google Gemini API key (no credit card required)
- Internet connection (the app calls Google's Gemini API)

Python packages (installed via `requirements.txt`):
```
langchain>=1.3.0
langchain-google-genai
google-generativeai
python-dotenv
```

---

## Getting a Free API Key

1. Go to **https://aistudio.google.com/app/apikey**
2. Sign in with a Google account
3. Click **"Create API key"**
4. Copy the key (it looks like `AIzaSy...`)

You'll paste this into your `.env` file in the setup steps below.

---

## Setup & Running — Windows

### 1. Check your Python version
Open **Command Prompt** or **PowerShell**:
```powershell
python --version
```
If it's below 3.10, download the latest installer from
https://www.python.org/downloads/windows/ and install it
(check **"Add python.exe to PATH"** during installation).

### 2. Create a virtual environment
```powershell
cd path\to\ai_tutor
python -m venv venv
```

### 3. Activate it
**PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```
**Command Prompt:**
```cmd
venv\Scripts\activate.bat
```
You should see `(venv)` appear at the start of your prompt.

> If PowerShell blocks the activation script with a permissions error, run:
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
> ```
> then try activating again.

### 4. Install dependencies
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Set up your API key
Copy `.env.example` to `.env` (in File Explorer, or run):
```powershell
copy .env.example .env
```
Open `.env` in Notepad and replace the placeholder with your real key:
```
GOOGLE_API_KEY=AIzaSy_your_actual_key_here
```

### 6. Run the app
```powershell
python step10_final_integration.py
```

---

## Setup & Running — macOS

### 1. Check your Python version
```bash
python3 --version
```
macOS often ships an old system Python (3.9 or earlier). If so, install a
newer version:
```bash
brew install python@3.12
```
(Install Homebrew first from https://brew.sh if you don't have it.)

> **Known Homebrew issue:** Homebrew's Python sometimes fails to create
> virtual environments cleanly (`ensurepip` / `pyexpat` errors). If you hit
> this, the most reliable fix is to instead download the **official
> installer** from https://www.python.org/downloads/macos/ and use that
> Python to create your venv — see Step 2 below.

### 2. Create a virtual environment
Using the official python.org install (recommended, most reliable on Mac):
```bash
cd path/to/ai_tutor
/Library/Frameworks/Python.framework/Versions/3.12/bin/python3.12 -m venv venv
```
(Adjust the version number to whatever you installed.)

### 3. Activate it
```bash
source venv/bin/activate
```

### 4. Verify you're inside the venv correctly
```bash
which python
which pip
```
Both paths should point **inside** your project's `venv/bin/` folder. If
either points somewhere else (e.g. `/opt/homebrew/...` or
`/Library/Frameworks/...`), something is off — recreate the venv before
continuing.

### 5. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Set up your API key
```bash
cp .env.example .env
```
Open `.env` in any text editor and paste your real key:
```
GOOGLE_API_KEY=AIzaSy_your_actual_key_here
```

### 7. Run the app
```bash
python main.py
```

---

## Setup & Running — Linux

### 1. Check your Python version
```bash
python3 --version
```
If below 3.10, install a newer version. On Debian/Ubuntu:
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv
```
On Fedora:
```bash
sudo dnf install python3.12
```

### 2. Create a virtual environment
```bash
cd path/to/ai_tutor
python3.12 -m venv venv
```

### 3. Activate it
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Set up your API key
```bash
cp .env.example .env
nano .env   # or any editor
```
Replace the placeholder with your real key:
```
GOOGLE_API_KEY=AIzaSy_your_actual_key_here
```

### 6. Run the app
```bash
python main.py
```

---

## Running Individual Modules

Once your venv is active and `.env` is set up, every step can be run and
tested on its own — useful for screenshotting clean output for a report:

```bash
python step1_api_integration.py
python step2_zero_shot.py
python step3_few_shot.py
python step4_chain_of_thought.py
python step5_role_prompting.py
python step6_prompt_templates.py
python step7_langchain_chains.py
python step8_memory_system.py
python step9_agents_tools.py
```
(On Windows, use `python` exactly as shown above — same commands.)

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'langchain_core'`**
Your terminal isn't using the venv's Python/pip. Activate the venv first
(`source venv/bin/activate` on Mac/Linux, `venv\Scripts\activate` on
Windows), then confirm with `which python` (Mac/Linux) or `where python`
(Windows) that the path points inside your `venv` folder before installing
or running anything.

**`GOOGLE_API_KEY not found` error on startup**
Make sure `.env` (not `.env.example`) exists in the same folder as
`config.py`, and that it contains a real key with no quotes:
```
GOOGLE_API_KEY=AIzaSy...
```

**`pip install` pulls very old package versions / version conflicts**
This usually means you're on Python < 3.10. Check with `python --version`
inside your activated venv and recreate the venv with a newer Python if
needed.

**Rate limit / `429` errors while running**
You've hit Gemini's free-tier requests-per-minute or requests-per-day limit.
Wait a minute and try again, or reduce how many calls you make in quick
succession.

**On macOS, `pip` says "command not found" but `pip3` works**
This means you're not actually inside an activated venv (you're using the
system Python). Re-activate the venv and use plain `pip`/`python` from then
on, not `pip3`/`python3`.

---

## Assignment Step Mapping

| File | Assignment Step | Marks Area |
|------|------------------|------------|
| `config.py` | Shared setup | — |
| `step1_api_integration.py` | Step 1 — LLM API Integration | API connectivity, response handling, session history |
| `step2_zero_shot.py` | Step 2 — Zero-Shot Prompting | Explanation, summarization, simplification |
| `step3_few_shot.py` | Step 3 — Few-Shot Prompting | Structured output generation and consistency |
| `step4_chain_of_thought.py` | Step 4 — Chain-of-Thought Reasoning | Step-by-step problem solving |
| `step5_role_prompting.py` | Step 5 — Role Prompting | Multi-role behavior implementation |
| `step6_prompt_templates.py` | Step 6 — Prompt Templates | Reusable and dynamic prompt design |
| `step7_langchain_chains.py` | Step 7 — LangChain Chains | Sequential pipeline implementation |
| `step8_memory_system.py` | Step 8 — Memory System | Context retention and personalization |
| `step9_agents_tools.py` | Step 9 — Agents & Tools | Tool usage and multi-step reasoning |
| `main.py` | Step 10 — Final Integration | Complete working application coherence |

---

## Limitations

- Relies on Google Gemini's **free tier**, which has request-per-minute and
  request-per-day caps — fine for coursework, not for production traffic.
- No retrieval-augmented generation (RAG) yet — the tutor can't answer
  questions about documents you upload.
- Memory is a simple local JSON file, not a database — fine for a single
  student on one machine, not multi-user deployment.
- Output formatting from few-shot prompts can occasionally drift even with
  examples provided, since this depends on the underlying model's behavior.

---

## Future Enhancements

- RAG integration so the tutor can answer from uploaded textbooks/notes
- A vector database (e.g. Chroma, FAISS) for document retrieval
- A web-based UI (Flask/Streamlit) instead of a console interface
- Multi-user support with proper authentication and a real database
