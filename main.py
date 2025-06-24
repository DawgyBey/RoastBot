import tkinter as tk
from tkinter import messagebox, ttk
import requests
import pyttsx3
import os
from dotenv import load_dotenv

# ==== Load API Key ====
load_dotenv()
API_KEY = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# ==== Text-to-Speech Setup ====
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# ==== Splash Screen ====
def show_splash_screen():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x300+500+250")
    splash.configure(bg="black")
    
    try:
        image = tk.PhotoImage(file="assets/splash.png")
        label = tk.Label(splash, image=image, bg="black")
        label.image = image  # Keep reference
    except:
        label = tk.Label(splash, text="RoastBot Loading...", font=("Arial", 18), fg="white", bg="black")
    
    label.pack(expand=True)
    root.after(2500, splash.destroy)

# ==== Hugging Face Request ====
def get_roast_response(user_input, style, temperature):
    system_msg = "You are a sarcastic assistant"
    if style != "Default":
        system_msg += f" with a {style.lower()} attitude"

    full_prompt = f"<|system|>{system_msg}<|user|>{user_input}<|assistant|>"

    data = {
        "inputs": full_prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 50,
            "repetition_penalty": 1.1,
            "stop": ["<|assistant|>", "<|user|>", "<|system|>"]
        }
    }

    try:
        res = requests.post(API_URL, headers=HEADERS, json=data)
        res.raise_for_status()
        full_text = res.json()[0]["generated_text"]
        return full_text.split("<|assistant|>")[-1].strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ==== Roast Action ====
roast_history = []
saved_roasts = []

def roast_me():
    text = user_entry.get().strip()
    if not text:
        messagebox.showinfo("Oops!", "Please enter something.")
        return

    style = style_choice.get()
    temp = float(temp_slider.get())

    roast = get_roast_response(text, style, temp)

    roast_output.config(state="normal")
    roast_output.delete(1.0, tk.END)
    roast_output.insert(tk.END, roast)
    roast_output.config(state="disabled")

    history_listbox.insert(tk.END, f"🔥 {roast}")
    saved_roasts.append(roast)

    if voice_toggle.get():
        engine.say(roast)
        engine.runAndWait()

# ==== Save to File ====
def save_roast_favorites():
    with open("RoastBot_Favorites.txt", "w", encoding="utf-8") as file:
        for roast in saved_roasts:
            file.write(roast + "\n")
    messagebox.showinfo("Saved!", "Favorites saved to file.")

# ==== Main App Window ====
root = tk.Tk()
show_splash_screen()

root.title("RoastBot Ultimate")
root.geometry("680x560")
root.configure(bg="black")

# ==== Title ====
tk.Label(root, text="💅 RoastBot Ultimate", font=("Arial", 20, "bold"), fg="#FF69B4", bg="black").pack(pady=10)

# ==== User Input ====
user_entry = tk.Entry(root, font=("Arial", 12), width=50)
user_entry.pack(pady=5, ipady=5)

# ==== Voice Toggle ====
voice_toggle = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Enable Voice", font=("Arial", 12), variable=voice_toggle,
               bg="black", fg="white", selectcolor="black").pack()

# ==== Temperature Slider ====
tk.Label(root, text="Sarcasm Level", font=("Arial", 12), fg="white", bg="black").pack(pady=(10, 0))
temp_slider = tk.Scale(root, from_=0.3, to=1.5, resolution=0.05, orient="horizontal",
                       length=300, bg="black", fg="#FF69B4")
temp_slider.set(1.45)
temp_slider.pack()

# ==== Style Dropdown ====
tk.Label(root, text="Roast Style", font=("Arial", 12), fg="white", bg="black").pack()
style_choice = ttk.Combobox(root, values=["Default", "Nerd", "Gamer", "Boomer", "Savage"])
style_choice.set("Default")
style_choice.pack(pady=5)

# ==== Output Box ====
roast_output = tk.Text(root, font=("Arial", 12), height=6, width=70, wrap="word",
                       bg="#1e1e1e", fg="white", state="disabled")
roast_output.pack(pady=10)

# ==== History Box ====
tk.Label(root, text="Roast History", font=("Arial", 12), fg="white", bg="black").pack()
history_listbox = tk.Listbox(root, font=("Courier", 10), height=6, width=70, bg="#2b2b2b", fg="white")
history_listbox.pack(pady=5)

# ==== Buttons ====
tk.Button(root, text="Roast Me", command=roast_me, font=("Arial", 12), bg="#FF69B4").pack(pady=5)
tk.Button(root, text="Save Favorites", command=save_roast_favorites, font=("Arial", 12),
          bg="#444", fg="white").pack(pady=5)

# ==== Run App ====
root.mainloop()
