# 🎥 YouTube Video Q&A — RAG Application

A text-based **YouTube Video Question Answering** application built with **Python, Flask, LangChain, Gemini, FAISS, and YouTube Transcript API**.

The application fetches a YouTube video's transcript, converts it into searchable vector embeddings, and allows users to ask questions about the video. The AI answers questions using the relevant information retrieved from the video's transcript.

---

## 🚀 Features

- 🔗 Enter a YouTube video URL
- 📝 Automatically fetch the video's transcript
- 🌍 Supports available transcripts/languages
- ✂️ Splits the transcript into smaller chunks
- 🧠 Generates embeddings using Gemini
- 🔎 Uses FAISS for similarity search
- 🤖 Uses Gemini 2.5 Flash to generate answers
- 💬 Ask multiple questions about the loaded video
- 🎯 Answers are based only on the video transcript
- 🌐 Flask backend with a web-based frontend
- ⚡ Fast retrieval using a vector database

---

## 🛠️ Tech Stack

### Backend
- Python
- Flask
- Flask-CORS

### AI / LLM
- Google Gemini
- `gemini-2.5-flash`
- `gemini-embedding-001`

### RAG
- LangChain
- FAISS
- Recursive Character Text Splitter

### YouTube
- YouTube Transcript API

### Frontend
- HTML
- CSS
- JavaScript

---

## 🧠 How It Works

The project follows a **Retrieval-Augmented Generation (RAG)** architecture.

```text
YouTube URL
     ↓
Extract Video ID
     ↓
Fetch Transcript
     ↓
Split Transcript into Chunks
     ↓
Generate Embeddings
     ↓
Store Embeddings in FAISS
     ↓
User Asks Question
     ↓
Similarity Search
     ↓
Retrieve Relevant Transcript Chunks
     ↓
Send Context + Question to Gemini
     ↓
Generate Answer
     ↓
Display Answer
```

---

## 📂 Project Structure

```text
youtube-video-qa/
│
├── app.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/youtube-video-qa.git
```

```bash
cd youtube-video-qa
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 API Key Setup

Create a `.env` file in the project directory:

```env
GOOGLE_API_KEY=your_google_api_key
```

Load the environment variable in Python:

```python
from dotenv import load_dotenv

load_dotenv()
```

**Never upload your API key to GitHub.**

Add `.env` to `.gitignore`:

```text
.env
venv/
__pycache__/
```

---

## ▶️ Run the Application

Start the Flask server:

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000
```

---

## 💬 Example

Enter a YouTube video URL:

```text
https://www.youtube.com/watch?v=XXXXXXXXXXX
```

Then ask questions such as:

```text
What is this video about?
```

```text
What topics were discussed?
```

```text
Explain the main concept discussed in the video.
```

```text
What did the speaker say about Generative AI?
```

The application retrieves the relevant parts of the transcript and uses Gemini to generate an answer.

---

## 🔍 RAG Implementation

The project uses the following RAG pipeline:

### 1. Document Loading

The YouTube Transcript API fetches the transcript.

### 2. Text Splitting

The transcript is divided into chunks using:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

### 3. Embeddings

Gemini generates vector representations of the transcript chunks:

```python
GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)
```

### 4. Vector Database

FAISS stores the embeddings and performs similarity search.

### 5. Retrieval

When the user asks a question, the retriever finds the most relevant transcript chunks.

### 6. Generation

Gemini 2.5 Flash receives the retrieved context and question and generates the final answer.

---

## 🔗 API Endpoints

### Load Video

```text
POST /load-video
```

Request:

```json
{
    "video_link": "https://www.youtube.com/watch?v=XXXXXXXXXXX"
}
```

Response:

```json
{
    "success": true,
    "message": "Video loaded successfully"
}
```

---

### Ask Question

```text
POST /ask
```

Request:

```json
{
    "question": "What is the video about?"
}
```

Response:

```json
{
    "success": true,
    "answer": "..."
}
```

---

## 🎯 Project Goal

The main goal of this project is to make long YouTube videos easier to understand by allowing users to interact with the video's transcript using natural language.

Instead of manually watching the entire video to find specific information, users can ask questions and retrieve relevant information directly.

---

## 📚 Concepts Learned

Through this project, I worked with:

- Retrieval-Augmented Generation (RAG)
- Large Language Models
- Vector Embeddings
- Vector Databases
- Semantic Search
- FAISS
- LangChain
- Gemini API
- YouTube Transcript API
- Flask REST APIs
- Prompt Engineering
- LCEL / LangChain Runnables
- Frontend ↔ Backend communication

---

## 🔮 Future Improvements

- 🎙️ Support videos without transcripts using speech-to-text
- 🌍 Better multilingual transcript selection
- 💾 Save previously processed videos
- 📌 Timestamp-based answers
- 📄 Export answers as PDF
- 🧠 Conversation memory
- 📊 Show relevant transcript sources
- 🎥 Jump directly to the relevant part of the YouTube video
- 🚀 Deploy the application online

---

## 👨‍💻 Author

**Anas**

B.Tech Computer Science Engineering Student

Interested in **Generative AI, RAG, AI Agents, and Backend Development**.
