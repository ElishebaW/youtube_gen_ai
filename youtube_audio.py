import os
import openai
import sys
from langchain_community.document_loaders.blob_loaders.youtube_audio import (
    YoutubeAudioLoader,
)
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers.audio import (
    OpenAIWhisperParser,
    OpenAIWhisperParserLocal,
)


os.environ["OPENAI_API_KEY"] = "none"
os.environ["LOCAL_API_KEY"] = "true"

model_name = os.environ.get("OLLAMA_MODEL", "ollama/llama2")
base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

llm = LLM(model=model_name, base_url=base_url)


local = False


#Big O Lecture
urls = ["https://youtu.be/D6xkbGLQesk?si=IeWLgzyNF2kJni40"]

# Directory to save audio files
save_dir = "~/Downloads/YouTube"