# -*- coding: utf-8 -*-
"""Chatbot_1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1-ofjioBWvwq5mn0JatRQ4kU5FWrT-snH
"""

!pip install streamlit
!pip install langchain_huggingface
!pip install langchain_groq
!pip install langchain_chroma
!pip install langchain_community
!pip install pyPDF
!pip install pytesseract
!pip install pyngrok
!pip install SpeechRecognition
!pip install pydub
!apt update && apt install -y tesseract-ocr
!pip install beautifulsoup4

# Commented out IPython magic to ensure Python compatibility.
# %%writefile app.py
# import streamlit as st
# from langchain.chains import create_history_aware_retriever, create_retrieval_chain
# from langchain.chains.combine_documents import create_stuff_documents_chain
# from langchain_chroma import Chroma
# from langchain_community.chat_message_histories import ChatMessageHistory
# from langchain_core.chat_history import BaseChatMessageHistory
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_groq import ChatGroq
# from langchain_core.documents import Document
# from langchain_core.messages import HumanMessage, AIMessage
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_huggingface import HuggingFaceEmbeddings
# from PIL import Image
# import pytesseract
# import os
# import speech_recognition as sr
# from moviepy.editor import VideoFileClip
# from pydub import AudioSegment
# from langchain.document_loaders import PyPDFLoader
# 
# st.title("🗣️ Conversational AI with Multi-Modal File Uploads & 📝 Chat History")
# st.subheader("Upload 📄PDFs/ 📸Images/ 🎥Video/ 🔊Audio and 💬chat with their content")
# 
# # Sidebar for API Key and Model Selection
# api_key = st.sidebar.text_input("Enter your API key:", type="password")
# model_option = st.sidebar.selectbox("Select an LLM model:", ("Gemma2-9b-It", "llama-3.3", "deepseek-r1"))
# 
# if "store" not in st.session_state:
#     st.session_state.store = {}
# if "session_titles" not in st.session_state:
#     st.session_state.session_titles = {}
# 
# def initialize_llm(api_key, model_option):
#     if model_option == "Gemma2-9b-It":
#         return ChatGroq(groq_api_key=api_key, model_name="Gemma2-9b-It")
#     elif model_option == "llama-3.3":
#         return ChatGroq(groq_api_key=api_key, model_name="llama-3.3-70b-versatile")
#     elif model_option == "deepseek-r1":
#         return ChatGroq(groq_api_key=api_key, model_name="deepseek-r1-distill-qwen-32b")
#     return None
# 
# # Session Management
# def manage_sessions():
#     if st.sidebar.button("Create New Session"):
#         new_session_id = f"Session_{len(st.session_state.store) + 1}"
#         st.session_state.store[new_session_id] = ChatMessageHistory()
#         st.session_state.session_titles[new_session_id] = "New Session"
#     session_options = [f"{st.session_state.session_titles[s]} ({s})" for s in st.session_state.store.keys()]
#     return st.sidebar.selectbox("Select a session", session_options)
# 
# selected_session = manage_sessions()
# selected_session_id = selected_session.split("(")[-1].strip(")") if selected_session else None
# 
# def process_uploaded_files(uploaded_files, file_type):
#     documents = []
#     os.makedirs("temp", exist_ok=True)
#     for uploaded_file in uploaded_files:
#         file_path = os.path.join("temp", uploaded_file.name)
#         with open(file_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())
# 
#         if file_type == "PDF":
#             loader = PyPDFLoader(file_path)
#             documents.extend([Document(page_content=doc.page_content) for doc in loader.load()])
#         elif file_type == "Image":
#             text = pytesseract.image_to_string(Image.open(file_path))
#             documents.append(Document(page_content=text))
#         elif file_type == "Video":
#             audio_text = extract_audio_text(file_path)
#             documents.append(Document(page_content=audio_text))
#         elif file_type == "Audio":
#             audio_text = transcribe_audio(file_path)
#             documents.append(Document(page_content=audio_text))
#         os.remove(file_path)
#     return documents
# 
# def extract_audio_text(video_path):
#     video_clip = VideoFileClip(video_path)
#     if video_clip.audio:
#         audio_path = "temp/temp_audio.wav"
#         video_clip.audio.write_audiofile(audio_path, codec="pcm_s16le")
#         return transcribe_audio(audio_path)
#     return "No audio found in the video."
# 
# def transcribe_audio(audio_path):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_path) as source:
#         audio_data = recognizer.record(source)
#         try:
#             return recognizer.recognize_google(audio_data)
#         except (sr.UnknownValueError, sr.RequestError):
#             return "Audio could not be transcribed."
# 
# file_type = st.sidebar.selectbox("Select file type:", ["PDF", "Image", "Video", "Audio"])
# uploaded_files = st.sidebar.file_uploader("Upload files", type=["pdf", "png", "jpg", "jpeg", "mp4", "wav", "mp3"], accept_multiple_files=True)
# 
# documents = process_uploaded_files(uploaded_files, file_type) if uploaded_files else []
# 
# if api_key:
#     llm = initialize_llm(api_key, model_option)
#     if documents:
#         embeddings = HuggingFaceEmbeddings()
#         text_splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
#         splits = text_splitter.split_documents(documents)
#         vectorstore = Chroma.from_documents(splits, embedding=embeddings)
#         retriever = vectorstore.as_retriever()
# 
#         history_aware_retriever = create_history_aware_retriever(
#             llm, retriever, ChatPromptTemplate.from_messages([
#                 ("system", "Reformulate the question based on chat history"),
#                 MessagesPlaceholder("chat_history"),
#                 ("human", "{input}")
#             ])
#         )
# 
#         question_answer_chain = create_stuff_documents_chain(llm, ChatPromptTemplate.from_messages([
#             ("system", "Answer using retrieved context."),
#             MessagesPlaceholder("chat_history"),
#             ("human", "{input}")
#         ]))
# 
#         rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
# 
#         def get_by_session_id(session_id: str) -> BaseChatMessageHistory:
#             return st.session_state.store[session_id]
# 
#         user_input = st.text_input("Your Question")
#         if user_input:
#             session_history = st.session_state.store[selected_session_id]
#             response = rag_chain.invoke({"input": user_input, "chat_history": session_history.messages})
#             session_history.messages.append(HumanMessage(content=user_input))
#             session_history.messages.append(AIMessage(content=response['answer']))
#             st.write("Assistant:", response['answer'])
#             for message in session_history.messages:
#                 st.write(f"{'User' if isinstance(message, HumanMessage) else 'Assistant'}: {message.content}")
# else:
#     st.warning("Please enter the API key.")
#