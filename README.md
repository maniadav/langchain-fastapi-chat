### LangChain Chat with Streaming Response over FastAPI Websockets

This project is a streaming chatbot web app using FastAPI, LangChain, and Gemini (Google Generative AI) via websockets. It features a modern frontend and supports real-time chat with LLMs.

---

## Features
- Real-time chat with Gemini (Google Generative AI) or OpenAI models
- Streaming responses over websockets
- Modern, responsive frontend (Tailwind CSS)
- Logging of user input and agent output

---

## Setup

### 1. Clone and Prepare Environment
```sh
git clone <this-repo-url>
cd langchain-chat-websockets-main
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```sh
pip install -r requirements.txt
```

> **Note:**
> - `requirements.txt` does NOT update automatically when you install new packages. If you add packages with `pip install <package>`, run `pip freeze > requirements.txt` to update the file.

### 3. Configure API Keys
- Copy `.env-example` to `.env`:
  ```sh
  cp dotenv-example .env
  ```
- Add your API keys to `.env`:
  - For Gemini: `GOOGLE_API_KEY=your_google_api_key`
  - For OpenAI: `OPENAI_API_KEY=your_openai_api_key`

---

## Running the App

### Locally
```sh
uvicorn main:app --reload
```
Visit [http://localhost:8000](http://localhost:8000) in your browser.

### With Docker Compose
```sh
docker-compose up --build
```

---

## Logging
- User input and agent output are logged to the console at INFO level.
- If you do not see logs, ensure you are not running the app in the background or with output redirected.

---

## Updating Dependencies
- To add a new package: `pip install <package>`
- To update requirements.txt: `pip freeze > requirements.txt`

---

## Credits
Thanks to [@hwchase17](https://github.com/hwchase17) for inspiration from [chat-langchain](https://github.com/hwchase17/chat-langchain/tree/master)
