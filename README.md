# Chat_Bot
A Conversational AI Chatbot with Multi File Processing &amp; Chat History
This chatbot is designed to enhance document-based interactions by allowing users to upload PDFs, images, videos, and audio files and chat with their content using Large language models like Gemma2-9b-It, Llama-3.3, and DeepSeek-R1.

# Features:
1. Multi File Processing: Allow user to intract with videos, images, PDFs, and Audio. 
2. Chat History Management: Maintains session-based chat history for a seamless conversational experience.
3. Custom LLM Selection: Users can choose from top LLMs (Gemma2-9b-It, Llama-3.3, and DeepSeek-R1).

# Frame works used:
1. Streamlit – Web interface for an interactive and user-friendly experience.
2. LangChain – Enables context-aware retrieval and response generation.
3. ChromaDB – Vector database for efficient document search.
4. OCR (Tesseract) – Extracts text from images.
5. Speech Recognition – Converts audio/video speech to text.
6. HuggingFace Embeddings – Used for high-quality text vectorization.
7. MoviePy & Pydub – Handles video/audio file processing.

# Future Work & Improvements:
While the chatbot successfully processes PDFs, images, audio, and video files, there are certain limitations that need to be addressed in future updates:
1. **Support for Silent Videos:** Currently, the system relies on extracting audio for video processing and not work Videos without audio.
2. **Handling Large Files Efficiently:** The chatbot struggles with very large files, leading to slow processing times or memory limitations. 
