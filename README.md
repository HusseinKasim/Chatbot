
# RAG-Based LLM Chatbot
A full-stack LLM chatbot that lets users chat with an AI assistant and optionally ground its answers in their own uploaded PDFs, using a RAG pipeline built on LangChain and pgvector. Supports both guest sessions (no login required) and authenticated users with persistent chat history and document context.

Live demo:
https://chatbot-r1ui.onrender.com

-----

## Tech Stack
  - Frontend: React, Tailwind CSS, shadcn/ui
  - Backend: FastAPI
  - LLM: Groq API
  - RAG: LangChain, pgvector
  - DB: PostgreSQL
  - Authentication: JWT (PyJWT), password hashing (pwdlib)
  - Object Storage: AWS S3 (uploaded PDFs)
  - Testing: pytest
  - CI/CD: GitHub Actions (automated testing + Render deployment)
  - Containerization: Docker (+ Docker Compose)
  - Deployment: Render (frontend + backend), Supabase (DB)

-----

## Features
- Guest chat sessions without requiring authentication
- Authenticated users with persistent chat history
- PDF document upload and document-based question answering using RAG
- Semantic retrieval of relevant document chunks using pgvector
- Context-aware responses generated using retrieved document chunks
- AWS S3 storage for uploaded documents
- REST API for authentication, prompts, chat management, and document uploads
- JWT authentication using HTTP-only cookies
- Access and refresh token support
- Secure password hashing

-----

## Architecture Models
### Architecture Overview Diagram
The architecture overview shows the main components of the web application and how the frontend, backend, database, RAG system, authentication, object storage, and external services interact. Diagram created using Eraser.io.

<img width="1379" height="1036" alt="rag-based-llm-chatbot-architecture-diagram" src="https://github.com/user-attachments/assets/fc03f723-1273-4e65-9463-3f73628a331d" />

### RAG System Overview
The RAG system consists of two stages: ingestion and retrieval.
#### RAG Ingestion Diagram
During ingestion, uploaded documents are loaded, split into chunks, converted into embeddings, and stored in PostgreSQL using pgvector. Diagram created using Eraser.io.

<img width="434" height="696" alt="rag-based-llm-chatbot-rag-ingestion-diagram" src="https://github.com/user-attachments/assets/b56c0843-2b0a-4042-b1b0-95124b0e2b98" />


#### RAG Retrieval Diagram
During retrieval, relevant document chunks are retrieved based on semantic similarity. An updated prompt is then built using the user's original prompt and the most similar (top k) chunks as context and is passed to the LLM to generate a response. Diagram created using Eraser.io.

<img width="783" height="774" alt="rag-based-llm-chatbot-rag-retrieval-diagram" src="https://github.com/user-attachments/assets/c810db90-5ee6-4061-a7ed-0e9f71e2f404" />

-----

## API Reference
### REST API 
#### `prompt` Router
  - `POST /api/prompt/guest` -> passes the guest user's prompt to the Groq model and retrieves the generated response
  - `POST /api/prompt/user` -> passes the logged in user's prompt to the Groq model and retrieves the generated response, with optional RAG-based context retrieval

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

##  Testing
The automated tests are run on GitHub Actions as part of the CI pipeline.

### `auth`
#### Integration Tests
- `test_user_registration` -> Test `/api/auth/register` endpoint
- `test_user_login` -> Test `/api/auth/login` endpoint

#### Unit Tests
- `test_access_token_creation` -> Test successful access token creation
- `test_access_token_verification` -> Test successful access token verification 
- `test_refresh_token_creation` -> Test successful refresh token creation
- `test_refresh_token_verification` -> Test successful refresh token verification
- `test_password_hashing` -> Test successful password hashing
- `test_password_verification` -> Test successful password verification
- `test_access_token_cookie_security` -> Test successful access token cookie creation with correct security requirements
- `test_refresh_token_cookie_security` -> Test successful refresh token cookie creation with correct security requirements

### `prompt`
#### Integration Tests
- `test_guest_user_prompt_response` -> Test `/api/prompt/guest` endpoint
- `test_guest_user_prompt_empty` -> Test behavior of `/api/prompt/guest` endpoint when a user passes in an empty prompt
- `test_logged_in_user_prompt_response_new_chat` -> Test `/api/prompt/user` endpoint for a brand new chat (creating a new chat correctly)
- `test_logged_in_user_prompt_response_existing_chat` -> Test `/api/prompt/user` endpoint for an already existing chat (adding a new message correctly to an existing chat)
- `test_logged_in_user_prompt_empty` -> Test behavior of `/api/prompt/user` endpoint when a user passes in an empty prompt

### `chats`
#### Integration Tests
- `test_user_chats_fetch` -> Test `/api/chats/` endpoint
- `test_user_chats_fetch_invalid_user` -> Test behavior of `/api/chats/` endpoint when a guest user attempts to retrieve chats
- `test_user_chat_messages_fetch` -> Test `/api/chats/{chatID}/messsages/` endpoint
- `test_user_chat_delete ` -> Test `/api/chats/{chatID}/` delete endpoint

-----

## Infrastructure & Deployment
- Containerization: Docker (and Docker Compose)
- Frontend and Backend Deployment: Render
- PostgreSQL DB Deployment: Supabase
- Document Storage: AWS S3
- CI/CD Pipeline: GitHub Actions

-----

## Running Locally
### Option 1: Run the entire project using Docker Compose (Recommended)

```bash
docker compose up --build
```

This option will run the backend at: 
`http://localhost:8003`

This option will run the frontend at: 
`http://localhost:5173`

This option will run the database at: 
`localhost:5432`

-----

### Option 2: Run each separately

#### Frontend

```bash
cd frontend
npm run dev
```

#### Backend
```bash
cd backend
python -m uvicorn src.app:app --host 0.0.0.0 --port 8003
```

-----

## Assets
- [Send Prompt] (https://www.flaticon.com/free-icon/send_876777?term=send&page=1&position=9&origin=search&related_id=876777)

- [New Chat] (https://www.flaticon.com/free-icon/add_3416075?term=add&page=1&position=6&origin=search&related_id=3416075)

- [Add] (https://www.flaticon.com/free-icon/add_3416075?term=add&page=1&position=5&origin=search&related_id=3416075)

- [Upload] (https://www.flaticon.com/free-icon/up-loading_10009684?term=upload&page=1&position=7&origin=search&related_id=10009684)
