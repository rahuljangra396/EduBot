import os
import json
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import requests
import PyPDF2
import random
from datetime import datetime

# ------------- CONFIGURATION -------------
CONFIG_FILE = "config.json"
if os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
else:
    config = {"OPENWEATHER_API_KEY": "", "CITY": "Delhi"}
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

OPENWEATHER_API_KEY = config.get("OPENWEATHER_API_KEY", "")
CITY = config.get("CITY", "Delhi")

# ------------- CORE FUNCTIONS -------------

def fetch_weather():
    """Fetch real-time weather using OpenWeather API."""
    if not OPENWEATHER_API_KEY:
        return "⚠️ Weather API key missing in config.json."
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={OPENWEATHER_API_KEY}&units=metric"
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return "❌ Could not fetch weather."
        data = r.json()
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"].capitalize()
        return f"🌤️ Weather in {CITY}: {temp}°C, {desc}"
    except Exception as e:
        return f"⚠️ Error fetching weather: {e}"

def fetch_news():
    """Fetch educational news using a free public API (GNews)."""
    try:
        url = "https://gnews.io/api/v4/top-headlines?lang=en&country=in&max=5&apikey=6f26b3d8b6c63faab9470ed8a56b3d62"
        r = requests.get(url, timeout=8)
        if r.status_code != 200:
            return ["⚠️ Could not fetch news."]
        j = r.json()
        articles = [a["title"] for a in j.get("articles", [])]
        return articles if articles else ["No news articles found."]
    except Exception:
        return ["⚠️ Failed to fetch news."]

def get_quote():
    """Fetch a motivational quote."""
    try:
        r = requests.get("https://api.quotable.io/random", timeout=6)
        if r.status_code == 200:
            j = r.json()
            return f"💡 “{j['content']}” — {j['author']}"
    except Exception:
        pass
    return "💬 Keep going — you’re doing great!"

def read_pdf(file_path):
    """Extract text from a PDF file."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            pdf_reader = PyPDF2.PdfReader(f)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text.strip() if text else "No readable text found in the PDF."
    except Exception as e:
        return f"⚠️ Error reading PDF: {e}"

def explain_topic(topic, pdf_text):
    """Search a topic in the extracted PDF text."""
    topic = topic.lower()
    if topic in pdf_text.lower():
        start = pdf_text.lower().find(topic)
        snippet = pdf_text[start:start+500]
        return f"📘 Explanation snippet:\n\n{snippet}..."
    else:
        return f"🤖 Sorry, I couldn’t find information about '{topic}'. Try another topic."

def generate_quiz(pdf_text, num_q=5):
    """Generate random Q&A pairs from PDF text."""
    sentences = [s.strip() for s in pdf_text.split('.') if len(s.strip()) > 20]
    if len(sentences) < 5:
        return ["⚠️ Not enough content in PDF to create a quiz."]
    quiz = []
    for i in range(min(num_q, len(sentences)//2)):
        q = sentences[i].split(' ')[0:6]
        question = " ".join(q) + "?"
        answer = sentences[i + 1]
        quiz.append((question, answer))
    return quiz

def add_reminder(text):
    """Save a simple reminder locally."""
    reminder_file = "reminders.txt"
    with open(reminder_file, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} - {text}\n")
    return "✅ Reminder saved."

def list_reminders():
    """Display saved reminders."""
    reminder_file = "reminders.txt"
    if not os.path.exists(reminder_file):
        return "🗒️ No reminders found."
    with open(reminder_file, "r", encoding="utf-8") as f:
        reminders = f.read().strip()
    return reminders if reminders else "🗒️ No reminders found."

def set_alarm(time_str):
    """Simulate a basic alarm (prints message at given time)."""
    speak = f"⏰ Alarm set for {time_str}. (Note: Runs only while EduBot is open)"
    return speak


# ------------- GUI (Tkinter) -------------

class EduBotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EduBot - Student Learning Assistant")
        self.root.geometry("900x700")
        self.root.configure(bg="#1E1E1E")

        self.pdf_text = ""

        # Title
        tk.Label(root, text="📚 EduBot Dashboard", font=("Arial", 20, "bold"), fg="#00FFAA", bg="#1E1E1E").pack(pady=10)

        # Buttons Row
        button_frame = tk.Frame(root, bg="#1E1E1E")
        button_frame.pack(pady=5)

        tk.Button(button_frame, text="🌦 Weather", command=self.show_weather, width=15, bg="#333", fg="white").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="📰 News", command=self.show_news, width=15, bg="#333", fg="white").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="🎵 Play Music", command=self.play_music, width=15, bg="#333", fg="white").grid(row=0, column=2, padx=5, pady=5)
        tk.Button(button_frame, text="💬 Quote", command=self.show_quote, width=15, bg="#333", fg="white").grid(row=0, column=3, padx=5, pady=5)
        tk.Button(button_frame, text="📅 Remind Me", command=self.add_reminder_popup, width=15, bg="#333", fg="white").grid(row=0, column=4, padx=5, pady=5)
        tk.Button(button_frame, text="📋 List Reminders", command=self.show_reminders, width=15, bg="#333", fg="white").grid(row=0, column=5, padx=5, pady=5)
        tk.Button(button_frame, text="⏰ Set Alarm", command=self.set_alarm_popup, width=15, bg="#333", fg="white").grid(row=0, column=6, padx=5, pady=5)

        # Chat Display
        self.chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=25, bg="#222", fg="white", font=("Arial", 12))
        self.chat_box.pack(padx=10, pady=10)
        self.chat_box.insert(tk.END, "🤖 EduBot: Hello Rahi! Upload a study PDF to begin.\n\n")
        self.chat_box.configure(state='disabled')

        # PDF Upload + Topic Entry
        upload_frame = tk.Frame(root, bg="#1E1E1E")
        upload_frame.pack(pady=10)

        self.topic_entry = tk.Entry(upload_frame, width=40, font=("Arial", 12))
        self.topic_entry.grid(row=0, column=0, padx=10)
        tk.Button(upload_frame, text="📂 Upload PDF", command=self.load_pdf, bg="#444", fg="white").grid(row=0, column=1, padx=5)
        tk.Button(upload_frame, text="📘 Explain Topic", command=self.explain_topic, bg="#444", fg="white").grid(row=0, column=2, padx=5)
        tk.Button(upload_frame, text="🧠 Start Quiz", command=self.start_quiz, bg="#444", fg="white").grid(row=0, column=3, padx=5)

    # ---------- Event Functions ----------
    def update_chat(self, text):
        self.chat_box.configure(state='normal')
        self.chat_box.insert(tk.END, text + "\n\n")
        self.chat_box.configure(state='disabled')
        self.chat_box.yview(tk.END)

    def load_pdf(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
        if file_path:
            self.pdf_text = read_pdf(file_path)
            self.update_chat("✅ PDF loaded successfully!")

    def explain_topic(self):
        topic = self.topic_entry.get().strip()
        if not topic:
            messagebox.showinfo("Info", "Enter a topic first.")
            return
        if not self.pdf_text:
            self.update_chat("⚠️ Upload a PDF first.")
            return
        explanation = explain_topic(topic, self.pdf_text)
        self.update_chat("🤖 EduBot: " + explanation)

    def start_quiz(self):
        if not self.pdf_text:
            self.update_chat("⚠️ Upload a PDF first.")
            return
        quiz = generate_quiz(self.pdf_text)
        for q, a in quiz:
            self.update_chat(f"❓ {q}\n✅ {a}")

    def show_weather(self):
        self.update_chat(fetch_weather())

    def show_news(self):
        news = fetch_news()
        self.update_chat("📰 Top Headlines:\n" + "\n".join(f"• {n}" for n in news))

    def show_quote(self):
        self.update_chat(get_quote())

    def play_music(self):
        web_url = "https://www.youtube.com/watch?v=1OAjeECW90E&list=PLqILqWBSl__cmvpF8xikaJSoOdRUhPthi"
        os.system(f"start {web_url}")
        self.update_chat("🎵 Playing your YouTube playlist in browser...")

    def add_reminder_popup(self):
        text = tk.simpledialog.askstring("Reminder", "What should I remind you about?")
        if text:
            msg = add_reminder(text)
            self.update_chat(msg)

    def show_reminders(self):
        self.update_chat(list_reminders())

    def set_alarm_popup(self):
        time_str = tk.simpledialog.askstring("Set Alarm", "Enter time (HH:MM 24hr):")
        if time_str:
            msg = set_alarm(time_str)
            self.update_chat(msg)


# ------------- MAIN LAUNCH -------------

if __name__ == "__main__":
    root = tk.Tk()
    app = EduBotApp(root)
    root.mainloop()
