
# Chatbot
Basic LLM Chatbot made with React and Groq. 

-----

## Tech Stack
  - Frontend: HTML, CSS, JavaScript, React
  - Backend: FastAPI
  - LLM: Groq API
  - DB: PostgreSQL
  - Authentification: JWT (via PyJWT)
  - Containerization: Docker (+ Docker Compose)
  - Password Hashing: pwdlib

-----

## How to Run

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

## API Endpoints

### REST API
  - `POST /api/process-user-prompt` -> passes the logged in user's prompt to the Groq model and retrieves the generated response
  - `POST /api/process-guest-prompt` -> passes the guest user's prompt to the Groq model and retrieves the generated response
  - `POST /api/register` -> registers user account
  - `POST /api/login` -> authentificates user
  - `POST /api/logout` -> logs user out of account
  - `GET /api/me` -> retrieves user info
  - `GET /api/get-user-chats` -> retrieves user chats info

-----

## Features
- Processes user prompts via Groq API
- REST API for handling prompts and user registration/authentification
- PostgreSQL DB for user login data and user chats data
- JWT Authentification
- Password hashing
- Docker containerization support
-----

## Assets Used
- [Sidepanel] (https://www.flaticon.com/free-icon/side-menu_5405818?term=side+bar&page=1&position=9&origin=search&related_id=5405818)

- [Send] (https://www.flaticon.com/free-icon/send_876777?term=send&page=1&position=9&origin=search&related_id=876777)
