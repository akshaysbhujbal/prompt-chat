import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random
import datetime
from PIL import Image
import pytesseract
import PyPDF2
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from collections import Counter
from response_data_dictionary import responses_dict  # <-- Imported from file

# nltk.download('punkt')

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

EXTRACTED_TEXT_FILE = "extracted_text.txt"

def extract_text_from_pdf(path):
    try:
        with open(path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"Error reading PDF: {e}"

def extract_text_from_image(path):
    try:
        img = Image.open(path).convert("RGB")
        return pytesseract.image_to_string(img).strip()
    except Exception as e:
        return f"Error reading image: {e}"

def extract_text_from_txt(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading text file: {e}"

def extract_text_from_files(file_paths):
    all_text = ""
    for file_path in file_paths:
        ext = file_path.lower().split('.')[-1]
        if ext == 'pdf':
            all_text += extract_text_from_pdf(file_path) + "\n"
        elif ext in ['jpg', 'jpeg', 'png']:
            all_text += extract_text_from_image(file_path) + "\n"
        elif ext == 'txt':
            all_text += extract_text_from_txt(file_path) + "\n"
    with open(EXTRACTED_TEXT_FILE, 'w', encoding='utf-8') as f:
        f.write(all_text)
    return all_text

# --- Chat Logic using external dictionary ---
def get_response(message):
    message = message.lower().strip()

    if "time" in message:
        return f"The current time is {datetime.datetime.now().strftime('%I:%M %p')}."
    if "date" in message:
        return f"Today's date is {datetime.datetime.now().strftime('%B %d, %Y')}."

    for key in responses_dict:
        if key in message:
            return random.choice(responses_dict[key])
    
    return random.choice(responses_dict.get("default", ["I don't understand."]))

def find_answer(question, text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    question_words = word_tokenize(question.lower())
    word_count = Counter(words)

    relevant = [s for s in sentences if any(w in s.lower() for w in question_words)]
    if not relevant:
        return "Sorry, I couldn't find anything related."

    best = max(relevant, key=lambda s: sum(word_count[w] for w in word_tokenize(s.lower()) if w in question_words))
    return best

# --- Chat Mode UI ---
def run_chat_mode(prev_window):
    prev_window.destroy()
    window = tk.Tk()
    window.title("PROMPT Chat | By Mr.Bhujbal A.S. & Miss.Jankar D.G.")
    window.geometry("600x400")

    def send():
        user_msg = user_input.get()
        if user_msg.strip() == "":
            return
        chat_display.insert(tk.END, f"You: {user_msg}\n")
        reply = get_response(user_msg)
        chat_display.insert(tk.END, f"Bot: {reply}\n")
        user_input.delete(0, tk.END)
        chat_display.yview(tk.END)

    def go_back():
        window.destroy()
        main_window()

    tk.Label(window, text="Chat Mode - Ask Anything!", font=("Arial", 14)).pack(pady=10)
    chat_display = tk.Text(window, width=70, height=15)
    chat_display.pack()
    user_input = tk.Entry(window, width=50)
    user_input.pack(pady=5)

    tk.Button(window, text="Send", command=send).pack(pady=5)
    tk.Button(window, text="Go Back", command=go_back, fg="red").pack(pady=10)

    window.mainloop()

# --- Study Assistant Mode UI ---
def run_study_assistant_mode(prev_window):
    prev_window.destroy()
    window = tk.Tk()
    window.title("PROMPT Chat | By Mr.Bhujbal A.S. & Miss.Jankar D.G.")
    window.geometry("700x600")

    extracted_text = ""
    uploaded_files = []

    def upload_files():
        nonlocal extracted_text, uploaded_files
        files = filedialog.askopenfilenames(filetypes=[("Supported", "*.pdf *.txt *.jpg *.jpeg *.png")])
        if not files:
            return
        uploaded_files = list(files)
        extracted_text = extract_text_from_files(files)
        file_names_display.config(state=tk.NORMAL)
        file_names_display.delete("1.0", tk.END)
        for f in uploaded_files:
            file_names_display.insert(tk.END, f"{os.path.basename(f)}\n")
        file_names_display.insert(tk.END, f"\nTotal Files Uploaded: {len(uploaded_files)}")
        file_names_display.config(state=tk.DISABLED)
        messagebox.showinfo("Success", "Text extracted and saved!")

    def ask():
        nonlocal extracted_text
        question = question_entry.get()
        if not question.strip():
            return
        if not extracted_text:
            if os.path.exists(EXTRACTED_TEXT_FILE):
                with open(EXTRACTED_TEXT_FILE, 'r', encoding='utf-8') as f:
                    extracted_text = f.read()
            else:
                answer_display.config(state=tk.NORMAL)
                answer_display.delete("1.0", tk.END)
                answer_display.insert(tk.END, "Please upload files first.")
                answer_display.config(state=tk.DISABLED)
                return
        answer = find_answer(question, extracted_text)
        answer_display.config(state=tk.NORMAL)
        answer_display.delete("1.0", tk.END)
        answer_display.insert(tk.END, answer)
        answer_display.config(state=tk.DISABLED)

    def go_back():
        window.destroy()
        main_window()

    tk.Label(window, text="Study Assistant Mode", font=("Arial", 14)).pack(pady=10)
    tk.Button(window, text="Upload Files", command=upload_files).pack(pady=5)

    tk.Label(window, text="Uploaded Files:", font=("Arial", 12)).pack()
    file_names_display = tk.Text(window, height=6, width=80, state=tk.DISABLED)
    file_names_display.pack(pady=5)

    tk.Label(window, text="Enter your question:", font=("Arial", 12)).pack(pady=10)
    question_entry = tk.Entry(window, width=120)
    question_entry.pack(pady=5)

    tk.Button(window, text="Ask", command=ask).pack(pady=10)

    answer_display = tk.Text(window, height=8, width=80, wrap=tk.WORD, font=("Arial", 12), state=tk.DISABLED)
    answer_display.pack(pady=10)

    tk.Button(window, text="Go Back", command=go_back, fg="red").pack(pady=20)

    window.mainloop()

# --- Main Window UI ---
def main_window():
    root = tk.Tk()
    root.title("PROMPT Chat | By Mr.Bhujbal A.S. & Miss.Jankar D.G.")
    root.geometry("500x400")

    tk.Label(root, text="Choose a Mode", font=("Arial", 16)).pack(pady=20)
    tk.Button(root, text="Chat Mode", command=lambda: run_chat_mode(root), font=("Arial", 15), width=25, height=2).pack(pady=10)
    tk.Button(root, text="Study Assistant Mode", command=lambda: run_study_assistant_mode(root), font=("Arial", 15), width=25, height=2).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main_window()
