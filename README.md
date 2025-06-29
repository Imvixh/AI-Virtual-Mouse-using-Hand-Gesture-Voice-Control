# AI-Virtual-Mouse-using-Hand-Gesture-Voice-Control
This project allows users to control their computer mouse using hand gestures and voice commands — no physical contact required. It's ideal for touchless control in presentations, accessibility solutions, or futuristic HCI (Human-Computer Interaction) experiments.

# 🖥️ AI Virtual Mouse using Hand Gesture & Voice Control

This project allows you to control your computer mouse using **hand gestures** and **voice commands** in real-time through your webcam. It is deployed on **Hugging Face Spaces** using **Gradio**, allowing easy access and sharing.

---

## 💡 Features

- 🎯 Cursor movement using **left-hand middle finger**
- 🖱️ Single click, hold/drag, and **double click using pinch gesture** (thumb + index finger)
- 📜 Scroll up/down using **right-hand gestures**
- 📋 Right-click using 4 fingers on the right hand
- 🗣️ Voice commands to open apps, search Google/Wikipedia, and answer common questions
- 🔴 Live webcam feed with **gesture feedback** for both hands
- 🧠 AI-powered and real-time interaction

---

## 🧰 Technologies Used

- **Python 3.10**
- [MediaPipe](https://github.com/google/mediapipe) for hand landmark tracking
- OpenCV for video streaming
- PyAutoGUI for mouse control
- pyttsx3 + SpeechRecognition for offline voice input/output
- Gradio for web interface and deployment
- Hugging Face Spaces for live sharing

---

## ✋ Hand Gesture Controls

| Gesture                                | Action             |
|----------------------------------------|--------------------|
| Middle finger (left hand)              | Move Cursor        |
| Pinch (thumb + index) short            | Single Click       |
| Pinch Hold                             | Drag & Drop        |
| Fast Double Pinch                      | Double Click       |
| Right hand 2 fingers                   | Scroll Down        |
| Right hand 3 fingers                   | Scroll Up          |
| Right hand 4 fingers                   | Right Click        |

---

## 🗣️ Voice Command Examples

- “Open Notepad”
- “Open Paint”
- “What is the time?”
- “Search AI on Google”
- “Tell me a joke”

---

## 🚀 How to Run

### ✅ Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/virtual-mouse-gesture-voice
cd virtual-mouse-gesture-voice
