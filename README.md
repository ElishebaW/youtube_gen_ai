# YouTube Video Transcription and Q&A with LLM

This project allows you to transcribe audio from a YouTube video using AssemblyAI and interact with the transcript using a local Large Language Model (LLM) like Ollama. You can ask questions about the video content, and the LLM will provide answers based on the transcript.

---

## **Features**
- Download audio from a YouTube video.
- Transcribe the audio using AssemblyAI's API.
- Interact with the transcript using a local LLM (e.g., `llama3.2`).
- Simple chat interface for asking questions about the video content.

---

## **Requirements**
- Python 3.8 or later
- AssemblyAI API key
- Local LLM server (e.g., Ollama) running on `http://localhost:11434`
- Required Python packages:
  - `pytube`
  - `requests`
  - `langchain_ollama`
  - `yt-dlp`

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository-url>
cd youtube_gen_ai