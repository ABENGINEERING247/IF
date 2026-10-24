# IF — INTELLIGENCE FACTORY

**Tagline:** Ideas In. Intelligence Out.

IF is a web-based AI coding-agent proof of concept built with Python and Streamlit. It turns a natural-language software idea into a project with complete files, a Python syntax check, and a downloadable ZIP.

## Features
- Premium dark, IDE-inspired interface
- Demo Mode that works without an API key
- Optional OpenAI API Mode for prompt-based project generation
- Multi-file output including `app.py`, `requirements.txt`, and `README.md`
- File preview workspace and ZIP export
- Python syntax compilation check (does not execute generated code)
- Setup and deployment guidance

## Requirements
- Python 3.10+
- Optional OpenAI API key for API Mode

## Run locally — Windows PowerShell
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Run locally — macOS/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run app.py
```

## Configure API Mode
Create `.streamlit/secrets.toml` locally:
```toml
OPENAI_API_KEY = "your-api-key-here"
OPENAI_MODEL = "gpt-4o-mini"
```
Do not commit this file to GitHub. On Streamlit Community Cloud, add these values in the app's Secrets settings. Use a model available to your API account. Demo Mode requires no key.

## Deploy on Streamlit Community Cloud
1. Upload these project files to a GitHub repository.
2. Connect the repository in Streamlit Community Cloud.
3. Set the main file path to `app.py`.
4. Add API secrets in the app's Secrets panel if using API Mode.
5. Deploy and test Demo Mode first.

## 90-second hackathon demo
1. Introduce IF as an AI coding-agent workspace.
2. Enter: “Build a CSV analytics dashboard with filters, charts, and downloadable reports.”
3. Show Demo Mode to demonstrate the build workflow without API dependency.
4. If configured, switch to API Mode for a tailored multi-file project.
5. Preview `app.py`, `requirements.txt`, and `README.md`.
6. Show the syntax-check result and download the ZIP.
7. Close with: **“IF — Ideas In. Intelligence Out.”**

## Architecture
- UI/orchestration: Streamlit
- Language: Python
- Optional generation provider: OpenAI Chat Completions API
- ZIP export: Python `zipfile`
- Syntax check: Python `compile()` only; generated code is not executed

## Safety and limitations
Generated code is untrusted. Review it before running or deploying it. The syntax check does not prove runtime correctness or security. Demo Mode creates a starter template rather than arbitrary custom features. Never expose API keys in source control or public demos.

## Future milestones
- Project templates and reusable skills
- Unit-test generation and test reports
- Isolated sandbox for running code
- GitHub export with explicit approval
- Persistent project history
- Planner, coder, reviewer, and tester agent workflow
