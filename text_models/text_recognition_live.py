import pyttsx3
import PyPDF2
from tkinter import filedialog
import tkinter as tk

def perform_live_text():
    """Uploads a PDF file, extracts the text using PyPDF2, and reads it aloud."""

    # Initialize text-to-speech engine
    engine = pyttsx3.init()

    # Open file dialog to select PDF
    root = tk.Tk()
    root.withdraw()
    pdf_path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF Files", "*.pdf")]
    )

    if not pdf_path:
        print("❌ No file selected.")
        return

    # Read PDF using PyPDF2
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            full_text = ""

            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                full_text += page.extract_text() or ""
                full_text += "\n"

        if full_text.strip():
            print("📄 Reading PDF content aloud...")
            engine.say(full_text)
            engine.runAndWait()
        else:
            print("⚠️ No readable text found in the PDF.")

    except Exception as e:
        print(f"❌ Error reading PDF: {e}")
