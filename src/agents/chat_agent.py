import streamlit as st
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import os


class ChatAgent:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        self.client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        self.model_name = "llama-3.3-70b-versatile"

    def initialize_vector_store(self, text_content):
        """Create vector store from text content."""
        if not text_content or text_content.strip() == "":
            # Create a minimal vector store with a placeholder
            text_content = "No report context available."

        texts = self.text_splitter.split_text(text_content)
        if not texts:
            # If splitting results in empty list, add at least one text
            texts = [text_content]

        vectorstore = FAISS.from_texts(texts, self.embeddings)
        return vectorstore

    def _format_chat_history(self, chat_history):
        """Format chat history for Groq API."""
        messages = []
        for msg in chat_history:
            messages.append({"role": msg["role"], "content": msg["content"]})
        return messages