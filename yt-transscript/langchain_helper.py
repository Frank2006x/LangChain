import os
import sys
from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from youtube_transcript_api import YouTubeTranscriptApi
import re

video_url="https://youtu.be/lG7Uxts9SXs?si=8Ixw2CFNyEd0T_eG"

def load_api_key()->str:
    load_dotenv()
    key=os.getenv("GOOGLE_API_KEY")
    if not key:
        print("Key not found in env")
        sys.exit()
    return key

def extract_video_id(url: str) -> str:
    """Extract YouTube video ID from URL"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    raise ValueError("Could not extract video ID from URL")

def get_youtube_transcript(video_url: str) -> str:
    """Get transcript from YouTube video using youtube-transcript-api directly"""
    try:
        video_id = extract_video_id(video_url)
        
        # Create an instance and use the fetch method
        api = YouTubeTranscriptApi()
        transcript = api.fetch(video_id)
        
        # Get the transcript text
        full_transcript = ""
        for entry in transcript:
            full_transcript += entry['text'] + " "
        
        return full_transcript.strip()
        
    except Exception as e:
        print(f"Error getting transcript: {e}")
        return None

def create_vectorDB_fromyt(video_url:str)->FAISS:
    try:
        # Configure API key
        api_key = load_api_key()
        genai.configure(api_key=api_key)
        
        # Initialize embeddings with API key
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        # Get YouTube transcript using direct API
        transcript_text = get_youtube_transcript(video_url)
        
        if not transcript_text:
            print("Could not retrieve transcript")
            return None
        
        # Create a document from the transcript
        doc = Document(page_content=transcript_text, metadata={"source": video_url})
        
        # Split the transcript into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        docs = text_splitter.split_documents([doc])
        
        # Create vector database
        db = FAISS.from_documents(docs, embeddings)
        return db
        
    except Exception as e:
        print(f"Error creating vector database: {e}")
        return None

if __name__ == "__main__":
    result = create_vectorDB_fromyt(video_url)
    if result:
        print("Vector database created successfully!")
        print(f"Number of documents: {result.index.ntotal}")
    else:
        print("Failed to create vector database")