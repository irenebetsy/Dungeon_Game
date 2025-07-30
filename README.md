# 🧩 Dungeon Game (Terminal, Web & Kivy UI)

📜 License: [Apache 2.0](./LICENSE)

🔗 [▶️ Play the Dungeon Game Online]


(https://betsys-dungeon-game.onrender.com/)     —     no installation needed!


A retro-style dungeon crawler game built in Python. Navigate through a dungeon filled with enemies, traps, coins, and hidden items — all displayed using colorful emoji symbols!

## 🎮 Features

- Three modes of play:
  - Terminal-based (text)
  - Web-based using Flask
  - GUI version using Kivy
- Save and load your game with a file
- Footstep tracking, item-based abilities (candle, compass, map tracker)
- Enemies that move, traps that surprise, and artifacts with powers

## 📁 Folder Structure

```
dungeon_game/
│
├── game/
│   ├── constants.py
│   ├── display.py
│   ├── engine.py
│   ├── map.py
│   ├── save_load.py
│   └── __init__.py
│
├── templates/
│   └── game.html
│
├── static/
│   └── style.css (optional)
│
├── app.py            # Flask app
├── kivi_app.py       # Kivy app
├── main_terminal.py  # CLI terminal version
├── save.txt
├── requirements.txt
└── README.md
```

## 🛠️ Setup

### 1. Create virtual environment and install packages

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ How to Run

### Terminal version

```bash
python main_terminal.py
```

### Web version (Flask)

```bash
python app.py
```

### Kivy version (GUI)

```bash
python kivi_app.py
```

visit the live web version here:  
👉 **https://betsys-dungeon-game.onrender.com/**

## 📦 Requirements

Use requirements.txt
```
flask
kivy
```

## 🧑‍💻 Author

Developed by: Irene Betsy D


