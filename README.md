# 🎓 Smart Learning Companion

Smart Learning Companion is a Python-based command-line application that helps students track their learning progress, manage grades, monitor study sessions, and gain insights through analytics and reports. It's designed as an interactive assistant for improving academic performance and building better study habits.

---

## 🚀 Features

- 📚 **Subject & Goal Setup**  
  Add any number of subjects and assign monthly study goals.

- 📝 **Grade Management**  
  - Add single or multiple grades  
  - View all grades and calculate averages  
  - Analyze performance trends

- ⏱ **Study Session Tracker**  
  - Record new sessions with hours, activity types, and notes  
  - View session history and monthly progress  
  - Identify study patterns and time distribution

- 📈 **Analytics Dashboard**  
  - Performance overview  
  - Study efficiency analysis 
  - Subject comparison and trend prediction  
  - Personalized recommendations  
  - Export performance report to JSON

- 💾 **Persistent Data Storage**  
  Automatically saves and loads progress across sessions via `student_summary.json`

---

## 💡 How It Works

Upon launch, the program will:
1. Load existing student data from `student_summary.json` *(if available)*  
2. Or prompt the user to set up a new profile  
3. Show a professional main dashboard with personalized insights  
4. Let you navigate through organized menus to manage grades, sessions, and view reports

---

## 📁 Project Structure

```
📦 Smart Learning Companion
├── main.py
├── mainfunctions.py
├── data_handler.py
├── dashboard.py
├── student_summary.json  # automatically created after first run
├── SOCRATIC.md  # Questions and Answers
└── README.md
```

---

## 🛠 Technologies Used

- Python 3
- JSON for data storage
- modules for logic & stats
- Modular design with function-based architecture

---

## ✅ Requirements

- Python 3.8+
- No external libraries required

---


## 🧠 Inspiration

This app was developed as a project for a programming course, combining real-world features like user profile management, analytics, persistent storage, and input validation in a structured, user-friendly way.