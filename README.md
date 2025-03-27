# 🤖 Deep Thought AI

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)



> "The Answer to Life, the Universe, and Everything" - powered by modern AI

<img width="960" alt="Screenshot 2025-03-27 at 13 09 21" src="https://github.com/user-attachments/assets/7ae81dcd-3bee-44ae-857a-e46f2037c73e" />


A web application inspired by "The Hitchhiker's Guide to the Galaxy", featuring Deep Thought - now enhanced with actual AI capabilities through ChatGPT integration.

## 🌐 Live-Version

Besuchen Sie die Live-Version der Anwendung:
[Deep Thought - Live Demo](https://deepthought-omega.vercel.app/)

## ✨ Features

- 🎨 Modern glassmorphism UI design
- 🤖 AI-powered responses via RapidAPI ChatGPT integration
- 🌌 Sci-fi themed user interface
- 💬 Real-time question answering
- 🎭 Character-based responses in Deep Thought's style
- 🚀 13-Sekunden Ladeanimation für authentisches Erlebnis
- 📱 Responsive Design für alle Geräte
- 🤖 Authentische Deep Thought Persönlichkeit

## 🚀 Quick Start

1. Clone the repository:
```bash
git clone git@github.com:densenden/deep_thought.git
cd deep-thought
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your RapidAPI key:
   - Get your API key from [RapidAPI](https://rapidapi.com)
   - Update the `x-rapidapi-key` in `app_rapid_api.py`

4. Run the application:
```bash
python app_rapid_api.py
```

5. Visit `http://localhost:5001` in your browser

## 🛠️ Technologies

- Python 3.12
- Flask 3.0.2
- RapidAPI ChatGPT Integration
- HTML5/CSS3 with Glassmorphism UI
- Vercel Deployment

## 📝 API Configuration

The application uses the ChatGPT API through RapidAPI. Configure your API key in `app_rapid_api.py`:

```python
headers = {
    "x-rapidapi-key": "YOUR_API_KEY",
    "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    "Content-Type": "application/json"
}
```

## 🎯 Usage

1. Open the web interface
2. Type your question in the input field
3. Click "Calculate Answer"
4. Receive Deep Thought's wisdom

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request or open an Issue for suggestions.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by Douglas Adams' "The Hitchhiker's Guide to the Galaxy"
- Built with Flask and modern web technologies
- Powered by ChatGPT through RapidAPI

---
Made with ❤️ in masterschool
