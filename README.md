# PROMPT-CHAT

PROMPT-CHAT is a Python-based desktop chatbot application developed using Tkinter and Natural Language Processing (NLP).  
The project provides two main modes:

- Chat Mode → General chatbot conversation
- Study Assistant Mode → Upload files and ask questions from their content

The application can extract text from PDF, TXT, and Image files and answer questions based on uploaded study material.

---

## Features

- Desktop GUI using Tkinter
- NLP-based chatbot responses
- Study Assistant Mode
- PDF text extraction
- OCR support for images using Tesseract
- TXT file reading support
- Date and time responses
- Multiple custom chatbot responses
- Beginner-friendly Python project

---

## Technologies Used

- Python
- Tkinter
- NLTK
- PyPDF2
- Pytesseract
- Pillow (PIL)
- JSON / Dictionary-based responses

---

## Project Structure

```bash
PROMPT-CHAT/
│
├── __pycache__/                 # Cache files
├── app.py                       # Main application
├── extracted_text.txt           # Extracted text storage
├── output.txt                   # Output file
├── prompt_chat.spec             # PyInstaller spec file
├── RCB vs MI.jpg                # Sample image file
├── README.md                    # Project documentation
├── requirements.txt             # Dependencies
├── response_data_dictionary.py  # Chatbot responses dictionary
└── SE.pdf                       # Sample PDF file