import os
import sys
import time
import threading
import subprocess

# Standard output & error redirection
sys.stdout = open(os.devnull, 'w')
sys.stderr = open(os.devnull, 'w')

import pygame
import keyboard
import screen_brightness_control as sbc

# Auto-detect sample rate
pygame.init()
pygame.mixer.init()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SOUNDS_DIR = os.path.join(BASE_DIR, 'sounds')

# Sound Cache memory-la load panni vachukalam (Zero disk lag)
SOUND_CACHE = {}

def preload_sounds():
    if os.path.exists(SOUNDS_DIR):
        for file in os.listdir(SOUNDS_DIR):
            if file.endswith('.mp3') or file.endswith('.wav'):
                path = os.path.join(SOUNDS_DIR, file)
                try:
                    SOUND_CACHE[file] = pygame.mixer.Sound(path)
                except Exception:
                    pass

preload_sounds()

playing_lock = False

def play_audio(filename, duration=None):
    global playing_lock
    if playing_lock:
        return False

    playing_lock = True

    def _play():
        global playing_lock
        try:
            if filename in SOUND_CACHE:
                sound = SOUND_CACHE[filename]
                channel = sound.play()
                if duration:
                    time.sleep(duration)
                    sound.stop()
                else:
                    while channel and channel.get_busy():
                        time.sleep(0.05)
            else:
                sound_path = os.path.join(SOUNDS_DIR, filename)
                if os.path.exists(sound_path):
                    sound = pygame.mixer.Sound(sound_path)
                    channel = sound.play()
                    if duration:
                        time.sleep(duration)
                        sound.stop()
                    else:
                        while channel and channel.get_busy():
                            time.sleep(0.05)
        except Exception:
            pass
        finally:
            playing_lock = False

    threading.Thread(target=_play, daemon=True).start()
    return True

# --- HOTKEY HANDLERS ---
def on_ctrl_c():
    play_audio("_Goundamani_Rt_14_Ringtone_(by Fringster.com).mp3")

def on_ctrl_v():
    play_audio("_Goundamani_Suriyan_Tamil_Dialogue_Ringtone_(by Fringster.com).mp3")

def on_ctrl_w():
    play_audio("pothum_pothum.mp3")

# --- BRIGHTNESS MONITOR ---
# --- BRIGHTNESS MONITOR (FIXED LOOPING ISSUE) ---
def monitor_brightness():
    try:
        current_brightness = sbc.get_brightness()[0]
    except Exception:
        current_brightness = 50

    while True:
        try:
            new_brightness = sbc.get_brightness()[0]
            diff = new_brightness - current_brightness

            # Brightness Increase (Boost) -> Remo
            if diff >= 5:
                if not playing_lock:
                    current_brightness = new_brightness  # Update brightness immediately
                    play_audio("remo.mp3", duration=6)
                    time.sleep(6.5)  # Lock loop during playback
                    
            # Brightness Decrease (Dim) -> Goundamani "Light Off"
            elif diff <= -5:
                if not playing_lock:
                    current_brightness = new_brightness  # Update brightness immediately to break the loop!
                    play_audio("light_off.mp3", duration=3)[cite: 6]
                    time.sleep(3.5)  # Lock loop during playback
                    
            else:
                current_brightness = new_brightness

        except Exception:
            pass
        
        time.sleep(0.5)

# --- NETWORK MONITOR ---
def check_internet():
    try:
        CREATE_NO_WINDOW = 0x08000000
        response = subprocess.run(
            ["ping", "-n", "1", "8.8.8.8"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW
        )
        return response.returncode == 0
    except Exception:
        return False

def monitor_network():
    was_connected = check_internet()
    while True:
        is_connected = check_internet()
        if was_connected and not is_connected:
            play_audio("amaithi_amaithi.mp3")
            was_connected = False
        elif not was_connected and is_connected:
            play_audio("ithu_pothum.mp3")
            was_connected = True
        time.sleep(1.0)

if __name__ == "__main__":
    threading.Thread(target=monitor_network, daemon=True).start()
    threading.Thread(target=monitor_brightness, daemon=True).start()

    keyboard.add_hotkey('ctrl+c', on_ctrl_c, suppress=False)
    keyboard.add_hotkey('ctrl+v', on_ctrl_v, suppress=False)
    keyboard.add_hotkey('ctrl+w', on_ctrl_w, suppress=False)

    keyboard.wait()