# 🤖 Arnav AI — Personal AI Chatbot

**Arnav AI** is a personal AI chatbot built using **Python, Flask, JavaScript, HTML, CSS, and Google's Gemini API**.

The chatbot provides a simple web-based interface where users can interact with an AI assistant and receive intelligent responses in real time.

---

## ✨ Features

* 🤖 AI-powered conversations using Gemini API
* 💬 Real-time chat interface
* 🌐 Flask-based backend
* 🎨 Custom HTML & CSS frontend
* ⚡ JavaScript-based chat interaction
* 💾 SQLite database integration
* 🗂️ Conversation/data storage
* 🔐 Secure API key management using environment variables
* 📱 Clean and responsive chatbot interface

---

## 🛠️ Technologies Used

| Technology        | Purpose                         |
| ----------------- | ------------------------------- |
| Python            | Backend programming             |
| Flask             | Web framework                   |
| Google Gemini API | AI responses                    |
| HTML5             | Web structure                   |
| CSS3              | UI styling                      |
| JavaScript        | Frontend interaction            |
| SQLite            | Database                        |
| python-dotenv     | Environment variable management |

---

## 📁 Project Structure

```text
Personal-Ai-chatboat/
│
├── app.py
│
├── database/
│   ├── chatboad.db
│   ├── chatbot.db
│   └── setup.sql
│
├── static/
│   ├── script.js
│   ├── style.css
│   └── Untitled-4.sql
│
├── templates/
│   └── index.html
│
├── .gitignore
├── README.md
└── .env                 # Not uploaded to GitHub
```

---

## 🔑 API Key Setup

Arnav AI uses the **Google Gemini API** to generate AI responses.

For security, the API key is stored in a `.env` file and is **not committed to GitHub**.

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_api_key_here
```

Make sure `.env` is included in `.gitignore`:

```gitignore
.env
.venv/
__pycache__/
```

**Never share or commit your actual API key.**

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/arnavkuchhal9-lang/Personal--Ai-chatboat.git
```

### 2. Open the project

```bash
cd Personal--Ai-chatboat
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

For Windows PowerShell:

```powershell
.venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install flask python-dotenv google-genai
```

---

## 🔐 Configure Gemini API

Create your `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

The application loads the API key through environment variables rather than hard-coding it in the source code.

---

## ▶️ Run the Application

Start the Flask server:

```bash
python app.py
```

You should see the Flask application running locally.

Open the local address shown by Flask in your browser.

---

## 🔄 How It Works

```text
        User
         │
         ▼
   Chatbot Interface
    HTML + CSS + JS
         │
         ▼
      Flask API
         │
         ▼
    Gemini API
         │
         ▼
    AI Response
         │
         ▼
   Chatbot Interface
```

The user sends a message through the web interface.

JavaScript sends the message to the Flask backend, which communicates with the Gemini API and returns the generated response to the frontend.

---

## 💾 Database

The project includes an SQLite database setup for storing chatbot-related data.

Database files are located inside:

```text
database/
├── chatboad.db
├── chatbot.db
└── setup.sql
```

The SQL setup file contains the database structure required by the application.

---

## 🎯 Project Objective

The goal of this project is to build a **personal AI assistant from scratch** while learning how different technologies work together:

* Frontend development
* Backend development
* REST/API communication
* AI API integration
* Database management
* Environment variable security
* Full-stack application development

---

## 🚀 Future Improvements

Some possible improvements include:

* 🧠 Long-term conversation memory
* 👤 User authentication
* 🗣️ Voice input and output
* 📄 File/document interaction
* 🖼️ Image understanding
* 💬 Multiple conversation sessions
* 🌙 Dark/light mode
* 📊 Chat history dashboard
* 🔎 Conversation search
* ⚡ Streaming AI responses

---
## UI
<img width="1867" height="997" alt="image" src="https://github.com/user-attachments/assets/863defb0-9bb9-4a1d-8207-295dd2e3b6df" />


## 🔒 Security

Sensitive credentials are stored using environment variables.

The `.env` file is intentionally excluded from Git using `.gitignore`.

```gitignore
.env
```

Never publish your Gemini API key publicly.

---

## 👨‍💻 Author

**Arnav Kuchhal**

B.Tech CSE
Jaypee Institute of Information Technology

---

## 📜 License

This project is created for **educational and personal development purposes**.
