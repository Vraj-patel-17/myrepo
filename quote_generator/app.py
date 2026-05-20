import json
import tkinter as tk
from tkinter import ttk
import random

with open("quote_generator/quotes.json","r") as file:
    final_list=json.load(file)
def generate_quote():
    label.config(text=random.choice(final_list))

root=tk.Tk()
root.title("Quote Generator")
root.geometry("700x400")
root.configure(bg="#121212")
frame=tk.Frame(root,bg="#121212")
frame.pack(expand=True)
style = ttk.Style()
style.theme_use("clam")
title=tk.Label(frame,text="\U0001F4AD"+"Daily Quote",font=("Segoe UI", 20, "bold"),
    bg="#121212",
    fg="white")
title.pack(pady=(10,30))
label=tk.Label(frame,text="Click below to generate a quote",font=("Poppins",18,"italic"),bg="#1E1E1E",fg="#EAEAEA",wraplength=550,justify="center",padx=25,pady=25)
label.pack(pady=20)
label.pack()
button=tk.Button(root,text="Generate a Quote :)",command=generate_quote,font=("Segoe UI", 14, "bold"),bg="#3B82F6",fg="white",relief="flat",padx=20,pady=10,cursor="hand2")
button.pack(pady=20)
root.mainloop()