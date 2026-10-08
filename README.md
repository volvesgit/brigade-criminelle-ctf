# Brigade Criminelle — Voice AI Social Engineering CTF

A social-engineering CTF challenge where players phone an AI-powered police inspector and try to talk their way into confidential information — by voice or by text.

The inspector is an LLM agent with a strict persona: it only reveals the target information to players who build a credible pretext and ask the right questions. Brute-force prompting gets you nowhere.

## How it works

```
Player (browser mic / text)
        │
        ▼
React + TypeScript frontend ──► FastAPI backend ──► Gemini (persona + game logic)
        ▲                            │
        └──── synthesized voice ◄────┴──► OpenAI TTS
                                     │
                                     └──► SQLite / PostgreSQL (conversation logs, flags found)
```

- **Voice interface** — speech recognition in the browser, natural French voice synthesis on the way back.
- **Persona agent** — a system prompt plus mission-state tracking keeps the inspector in character and decides when information can be disclosed.
- **Admin panel** — live view of every conversation, flag statistics, database cleanup.
- **Abuse protection** — per-IP rate limiting (`slowapi`), message length limits, input validation.

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Web Speech API |
| Backend | Python, FastAPI, Uvicorn, slowapi |
| AI | Google Gemini, OpenAI text-to-speech |
| Storage | SQLite (local) / PostgreSQL (Railway) |
| Deployment | Docker Compose, Railway |

## Run it locally

Requirements: Docker, a [Gemini API key](https://aistudio.google.com/apikey) and an OpenAI API key.

```bash
git clone https://github.com/volvesgit/brigade-criminelle-ctf.git
cd brigade-criminelle-ctf
cp .env.example .env   # then fill in GEMINI_API_KEY, OPENAI_API_KEY and ADMIN_PASSWORD
docker compose up --build
```

The frontend is served on http://localhost:3000 and the API on http://localhost:8000.
The admin panel stays disabled until `ADMIN_PASSWORD` is set.

On Windows you can also run `deploy.bat`, on Linux/macOS `./deploy.sh`.

## Project layout

```
backend/    FastAPI app, AI agent, database layer
frontend/   React voice interface and admin panel
docs/       deployment, Railway, distribution and admin guides
tests/      manual API and scenario test scripts (run from the repo root, e.g. python -m tests.test_gemini)
```

## Documentation

- [Deployment guide](docs/DEPLOYMENT.md)
- [Railway setup](docs/RAILWAY_SETUP.md)
- [Admin guide](docs/ADMIN_GUIDE.md)
- [Distributing the challenge](docs/DISTRIBUTION_GUIDE.md)

## Author

Built by [@volvesgit](https://github.com/volvesgit) for the Hack'olyte CTF community.
