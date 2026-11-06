# 🎬 Tamil Cinema Desktop Soundboard (Python)

A lightweight, low-latency background Python daemon that maps Windows system events, keyboard hotkeys, and hardware triggers to iconic Tamil cinema dialogues and songs!

## ✨ Features Live
- **`Ctrl + C`**: Goundamani Copy Dialogue
- **`Ctrl + V`**: Goundamani Suriyan Dialogue
- **`Ctrl + W`**: Vadivelu *"Pothum Pothum"* Dialogue
- **Brightness Boost**: Remo Song Clip (`remo.mp3`)
- **Brightness Dim**: Goundamani *"Light-a Amathu ley"* (`light_off.mp3`)
- **Wi-Fi Disconnect**: *"Amaithi Amaithi"* (shinchan )
- **Wi-Fi Reconnect**: Melody Clip (`ithu_pothum.mp3`)

## 🛠️ Technical Implementation
- **Zero-Latency RAM Caching:** Preloads `.mp3` buffers directly into `pygame.mixer.Sound` objects to eliminate disk-read lag.
- **Thread Synchronization:** Single-channel thread locks (`playing_lock`) prevent audio stuttering during rapid keypresses.
- **Silent Background Execution:** Configured via `pythonw.exe` and `CREATE_NO_WINDOW` flags to run silently without flashing terminal windows.

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone [https://github.com/Srimaha02/tamil-cinema-desktop-soundboard.git]
   cd tamil-cinema-desktop-soundboard
Install dependencies:

Bash
pip install pygame keyboard screen_brightness_control
Run silently in background:

Bash
pythonw desktop_main.pyw
Built as a fun weekend experiment exploring Python system automation, threading, and OS event handling! 🐍
