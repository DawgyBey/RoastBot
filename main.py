import tkinter as tk
from tkinter import messagebox
import requests

# ==== Load API Key ====
API_KEY = "your_api_key_here"  # Replace with your actual API key
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

# ==== Roast Generator ====
def get_response(user_input):
    prompt = f"You are a sarcastic assistant. Roast this: {user_input}"
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 100, "temperature": 1.0}
    }
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        return response.json()[0]["generated_text"].strip()
    except Exception as e:
        return f"Error: {str(e)}"

# ==== App Logic ====
def roast_user():
    user_input = entry.get().strip()
    if not user_input:
        messagebox.showinfo("Empty?", "Enter something to get roasted.")
        return
    response = get_response(user_input)
    output.config(state="normal")
    output.delete(1.0, tk.END)
    output.insert(tk.END, response)
    output.config(state="disabled")
    history_box.insert(tk.END, f"🔥 {response}")

# ==== GUI ====
root = tk.Tk()
root.title("RoastBot")
root.geometry("500x400")
root.configure(bg="black")

# Title
tk.Label(root, text="RoastBot", font=("Arial", 20, "bold"), fg="pink", bg="black").pack(pady=10)

# Input Field
entry = tk.Entry(root, font=("Arial", 12), width=40)
entry.pack(pady=10, ipady=5)

# Output Field
output = tk.Text(root, font=("Arial", 12), height=6, width=50, wrap="word", bg="gray", fg="white")
output.pack(pady=10)
output.config(state="disabled")

# Roast History
tk.Label(root, text="Roast History", font=("Arial", 12), fg="white", bg="black").pack()
history_box = tk.Listbox(root, font=("Courier", 10), height=6, width=50, bg="darkgray", fg="white")
history_box.pack(pady=5)

# Roast Button
tk.Button(root, text="Roast Me", command=roast_user, font=("Arial", 12), bg="pink").pack(pady=10)

# Run the App
root.mainloop()
