
# Chatbot
Basic LLM Chatbot made with React and LangChain. 

-----

## Tech Stack
  - Frontend: HTML, CSS, JavaScript, React
  - Backend: FastAPI
  - Real-Time Communication: REST-APIs
  - GenAI Model: LangChain (TO BE ADDED)
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
- Processes user prompts via a LangChain model (TO BE ADDED)
- REST API for handling prompts
- Docker containerization support (TO BE ADDED)
