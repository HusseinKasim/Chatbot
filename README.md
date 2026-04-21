
# Chatbot
Basic LLM Chatbot made with React and Groq. 

-----

## Tech Stack
  - Frontend: HTML, CSS, JavaScript, React
  - Backend: FastAPI
  - GenAI Model: Groq
  - Containerization: Docker (+ Docker Compose) (TO BE ADDED)

-----

## How to Run
### Frontend

```bash
npm run dev
```

### Backend
```bash
python -m uvicorn app:app --host 0.0.0.0 --port 8003
```

-----

## API Endpoints

### REST API
  - `POST /api/process-prompt` -> sends the user's prompt to the backend and retrieves response
-----

## Features
- Processes user prompts via Groq LLM
- REST API for handling prompts
- Docker containerization support (TO BE ADDED)
-----

## Assets Used
- [Sidepanel] (https://www.flaticon.com/free-icon/side-menu_5405818?term=side+bar&page=1&position=9&origin=search&related_id=5405818)

- [Send] (https://www.flaticon.com/free-icon/send_876777?term=send&page=1&position=9&origin=search&related_id=876777)
