
# Chatbot
An LLM Chatbot made with React, FastAPI, PostgreSQL, LangChain, and Groq API.

The website can be accessed here:
https://chatbot-r1ui.onrender.com

-----

## Tech Stack
  - Frontend: HTML, CSS, JavaScript, React
  - Backend: FastAPI
  - LLM: Groq API
  - RAG: LangChain
  - DB: PostgreSQL + pgvector
  - Authentication: JWT (via PyJWT)
  - Containerization: Docker (+ Docker Compose)
  - Password Hashing: pwdlib
  - Testing: pytest (IN PROGRESS)
  - CI/CD: GitHub Actions (automated testing and Render deployment)
  - Deployment: Render (Frontend + Backend), Supabase (DB)

-----

## Features
- Processes user prompts via Groq API
- RAG System for document-based knowledge retrieval and context-aware chatbot responses via LangChain (IN PROGRESS)
- REST API for handling prompts, user registration/authentication, and chat management
- PostgreSQL DB for user login data, user chats data, and vector storage using pgvector for RAG retrieval (IN PROGRESS)
- JWT Authentication
- Password hashing
- Docker containerization support
- Testing using pytest (IN PROGRESS)
- CI/CD Pipeline using GitHub Actions for automated testing and Render deployment
- Deployed on Render + Supabase

-----

## API Endpoints

### REST API 
#### `prompt` Router
  - `POST /api/prompt/guest` -> passes the guest user's prompt to the Groq model and retrieves the generated response
  - `POST /api/prompt/user` -> passes the logged in user's prompt to the Groq model and retrieves the generated response 

#### `auth` Router
  - `GET /api/auth/me` -> retrieves user info
  - `POST /api/auth/register` -> registers user account
  - `POST /api/auth/login` -> authenticates user
  - `POST /api/auth/logout` -> logs user out of account
  - `POST /api/auth/refresh` -> creates a new access token via refresh token

#### `chats` Router
  - `GET /api/chats/` -> retrieves user chats
  - `GET /api/chats/{chatID}/messages` -> retrieves chat messages
  - `DELETE /api/chats/{chatID}` -> deletes chat messages

#### `upload` Router
  - `POST /api/upload/` -> uploads a PDF file

-----

## How to Run Locally

### Option 1: Run the entire project using Docker Compose (Recommended)

```bash
docker compose up --build
```

This option will run the backend at: 
`http://localhost:8003`

This option will run the frontend at: 
`http://localhost:5173`

This option will run the database at: 
`http://localhost:5432`

-----

### Option 2: Run each seperately

#### Frontend

```bash
cd frontend/src
npm run dev
```

#### Backend
```bash
cd backend/src
python -m uvicorn app:app --host 0.0.0.0 --port 8003
```
-----

## Assets Used
- [Sidepanel] (https://www.flaticon.com/free-icon/side-menu_5405818?term=side+bar&page=1&position=9&origin=search&related_id=5405818)

- [Send Prompt] (https://www.flaticon.com/free-icon/send_876777?term=send&page=1&position=9&origin=search&related_id=876777)

- [New Chat] (https://www.flaticon.com/free-icon/add_3416075?term=add&page=1&position=6&origin=search&related_id=3416075)

- [Add] (https://www.flaticon.com/free-icon/add_3416075?term=add&page=1&position=5&origin=search&related_id=3416075)

- [Upload] (https://www.flaticon.com/free-icon/up-loading_10009684?term=upload&page=1&position=7&origin=search&related_id=10009684)
