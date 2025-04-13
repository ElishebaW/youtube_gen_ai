import os
import requests
from pytube import YouTube
import subprocess
from langchain_ollama import ChatOllama

# Step 1: Download audio from YouTube
def download_youtube_audio(youtube_url, output_path="audio.mp3"):
    subprocess.run([
        "yt-dlp",
        "-x", "--audio-format", "mp3",
        "-o", output_path,
        youtube_url
    ])
    return output_path

# Step 2: Upload audio to AssemblyAI
def upload_to_assemblyai(filename, api_key):
    headers = {'authorization': api_key}
    with open(filename, 'rb') as f:
        response = requests.post(
            'https://api.assemblyai.com/v2/upload',
            headers=headers,
            files={'file': f}
        )
    return response.json()['upload_url']

# Step 3: Request transcription
def request_transcription(audio_url, api_key):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {"audio_url": audio_url}
    headers = {"authorization": api_key}
    response = requests.post(endpoint, json=json, headers=headers)
    return response.json()['id']

# Step 4: Poll until transcription is complete
def wait_for_completion(transcript_id, api_key):
    endpoint = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    headers = {"authorization": api_key}
    
    while True:
        response = requests.get(endpoint, headers=headers).json()
        if response['status'] == 'completed':
            return response['text']
        elif response['status'] == 'error':
            raise RuntimeError(f"Transcription failed: {response['error']}")
        else:
            print("Transcribing...")  # or use time.sleep(3)

# Main function
def transcribe_youtube_video(youtube_url, api_key):
    print(f"Youtube URL {youtube_url}")
    audio_file = download_youtube_audio(youtube_url)
    print(f"Audio File {audio_file}")
    audio_url = upload_to_assemblyai(audio_file, api_key)
    transcript_id = request_transcription(audio_url, api_key)
    transcript_text = wait_for_completion(transcript_id, api_key)
    return transcript_text


# Example usage
if __name__ == "__main__":

    youtube_url = "https://www.youtube.com/watch?v=D6xkbGLQesk"
    assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")

    if not assemblyai_api_key:
        raise ValueError("Please set your ASSEMBLYAI_API_KEY environment variable.")

    # Step 1: Transcribe the YouTube video
    text = transcribe_youtube_video(youtube_url, assemblyai_api_key)

    # Step 2: Initialize local LLM (Ollama)
    llm = ChatOllama(model="llama3.2", base_url="http://localhost:11434")

    # Step 3: Start chat loop
    print("\n✅ Transcript ready. You can now ask questions about the video.")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        prompt = f"""This is a transcript from a YouTube video:

{text[:2000]}  # trim if too long

User's question: {user_input}
Answer:"""

        response = llm.invoke(prompt)
        print("\nLLM:", response.content)
