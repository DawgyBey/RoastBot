import tkinter as tk
from tkinter import messagebox, ttk
import requests
import pyttsx3
import os
from dotenv import load_dotenv

# ==== Load API Key from .env ====
load_dotenv()
API_KEY = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# ==== Text-to-Speech Engine ====
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# ==== Splash Screen ====
def show_splash():
    splash = tk.Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x300+500+250")
    splash.config(bg="black")
    try:
        img = tk.PhotoImage(file="assets/splash.png")
        label = tk.Label(splash, image=img, bg="black")
        label.pack()
        splash.image = img
    except:
        label = tk.Label(splash, text="RoastBot Loading...", fg="white", bg="black", font=("Arial", 18))
        label.pack(expand=True)
    root.after(2500, splash.destroy)

# ==== Roast Generator ====
def get_response(user_input, style, temperature):
    system_prompt = f"You are a sarcastic assistant"
    if style != "Default":
        system_prompt += f" with a {style.lower()} attitude"

    prompt = f"<|system|>{system_prompt}<|user|>{user_input}<|assistant|>"

    payload = {
        "inputs": prompt,
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
        r = requests.post(API_URL, headers=HEADERS, json=payload)
        r.raise_for_status()
        return r.json()[0]["generated_text"].split("<|assistant|>")[-1].strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# ==== App Logic ====
history = []
saved_roasts = []

def roast_user():
    user_input = entry.get().strip()
    if not user_input:
        messagebox.showinfo("Empty?", "Enter something to get roasted.")
        return

    style = style_box.get()
    temp = float(temp_slider.get())

    response = get_response(user_input, style, temp)

    output.config(state="normal")
    output.delete(1.0, tk.END)
    output.insert(tk.END, response)
    output.config(state="disabled")

    history_box.insert(tk.END, f"🔥 {response}")
    saved_roasts.append(response)

    if voice_var.get():
        engine.say(response)
        engine.runAndWait()

def save_roasts():
    with open("RoastBot_Favorites.txt", "w", encoding="utf-8") as f:
        for roast in saved_roasts:
            f.write(roast + "\n")
    messagebox.showinfo("Saved!", "Roasts saved to RoastBot_Favorites.txt")

# ==== GUI ====
root = tk.Tk()
show_splash()
root.title("RoastBot Ultimate")
root.geometry("680x560")
root.configure(bg="black")

tk.Label(root, text="💅 RoastBot Ultimate", font=("Arial", 20, "bold"), fg="#FF69B4", bg="black").pack(pady=10)

entry = tk.Entry(root, font=("Arial", 12), width=50)
entry.pack(pady=5, ipady=5)

voice_var = tk.BooleanVar(value=True)
tk.Checkbutton(root, text="Enable Voice", font=("Arial", 12), variable=voice_var, bg="black", fg="white", selectcolor="black").pack()

tk.Label(root, text="Sarcasm Level", font=("Arial", 12), fg="white", bg="black").pack(pady=(10, 0))
temp_slider = tk.Scale(root, from_=0.3, to=1.5, resolution=0.05, orient="horizontal", length=300, bg="black", fg="#FF69B4")
temp_slider.set(1.45)
temp_slider.pack()

tk.Label(root, text="Roast Style", font=("Arial", 12), fg="white", bg="black").pack()
style_box = ttk.Combobox(root, values=["Default", "Nerd", "Gamer", "Boomer", "Savage"])
style_box.set("Default")
style_box.pack(pady=5)

output = tk.Text(root, font=("Arial", 12), height=6, width=70, wrap="word", bg="#1e1e1e", fg="white")
output.pack(pady=10)
output.config(state="disabled")

tk.Label(root, text="Roast History", font=("Arial", 12), fg="white", bg="black").pack()
history_box = tk.Listbox(root, font=("Courier", 10), height=6, width=70, bg="#2b2b2b", fg="white")
history_box.pack(pady=5)

tk.Button(root, text="Roast Me", command=roast_user, font=("Arial", 12), bg="#FF69B4").pack(pady=5)
tk.Button(root, text="Save Favorites", command=save_roasts, font=("Arial", 12), bg="#444", fg="white").pack(pady=5)

root.mainloop()
