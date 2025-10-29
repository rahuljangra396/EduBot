🤖 EduBot – AI Learning Assistant by Rahi

EduBot is an AI-powered desktop assistant built with Python that helps students learn smarter by explaining topics from PDFs, generating quizzes, giving weather updates, news headlines, motivational quotes, reminders, and more — all in a friendly chat-style GUI.

🧠 Features

📘 PDF Topic Explainer – Upload study PDFs and ask EduBot to explain any concept

🧩 AI Quiz Generator – Automatically creates quiz questions from your notes

🌦 Weather Info – Get live weather using the OpenWeatherMap API

📰 News Headlines – Stay updated with top news stories

💬 Motivational Quotes – Get inspired while studying

🎵 YouTube Music Player – Plays your favorite study playlist

⏰ Reminders & Alarm Support – Set reminders or launch your alarm script

💻 Simple GUI Dashboard – Easy-to-use chat interface with quick-access buttons

🧍‍♂️ Built by: Rahi (rahuljangra396)

⚙️ Installation & Setup
1️⃣ Clone this Repository
git clone https://github.com/rahuljangra396/EduBot.git
cd EduBot

2️⃣ Install Required Libraries

Use pip to install all dependencies:

pip install -r requirements.txt


Or manually:

pip install requests PyPDF2 tkinter

🔑 API Configuration

Create a file named config.json in the project folder with your API key details:

{
  "OPENWEATHER_API_KEY": "YOUR_API_KEY",
  "CITY": "Delhi"
}


Get your free OpenWeather API key from:
👉 https://openweathermap.org/api

🚀 How to Run

Run EduBot by typing:

python EduBot.py

🧩 Example Commands
Action	Example Command
Explain a topic	Explain photosynthesis
Generate quiz	Start quiz
Show weather	Weather today
Show news	Show latest news
Get a quote	Motivate me
Play music	Play music
Add a reminder	Remind me to call friend
List reminders	List my reminders
Launch alarm	Start alarm
📂 Folder Structure
EduBot/
│
├── EduBot.py
├── config.json
├── smartlife_data.json
├── README.md
├── requirements.txt
└── (optional) alarm_deluxe.py

🧰 Technologies Used

Python 3.13

Tkinter (GUI)

Requests (APIs)

PyPDF2 (PDF parsing)

OpenWeatherMap API

💡 Future Improvements

Integration with ChatGPT API for deeper explanations

Voice-enabled commands

Study progress tracking

👨‍💻 Developer

Made with ❤️ by Rahi (rahuljangra396)

A Python + AI project for smart learning.
