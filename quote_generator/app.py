import json
import tkinter as tk
import customtkinter as ctk
import random
import os
import sys
def resource_path(relative_path):
    try:
        base_path=sys._MEIPASS
    except Exception:
        base_path=os.path.abspath(".")
    return os.path.join(base_path,relative_path)
json_path=resource_path("quote_generator/quotes.json")
with open(json_path,"r") as file:
    final_list=json.load(file)
def generate_quote():
    random_quote=random.choice(final_list)
    quote=random_quote["quote"]
    author=random_quote["author"]
    label.configure(text=f'{quote}\n\n--{author}')
    root.update_idletasks()
    width=min(label.winfo_reqwidth()+120,520)
    height=label.winfo_reqheight()+90
    root.geometry(f"{width}x{height}")
    root.after(10000,generate_quote)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root=ctk.CTk()
root.title("Quote Generator")
root.configure(bg_color="#121212")
frame=ctk.CTkFrame(root,bg_color="#121212")
frame.pack(expand=True,fill="both",pady=3,padx=3)
title=ctk.CTkLabel(frame,text="\U0001F4AD"+"Daily Quotes",font=("Segoe UI", 20, "bold"),
    text_color="white")
title.pack(pady=(5,15))
label=ctk.CTkLabel(frame,text="",font=("Poppins",14,"italic"),bg_color="#1E1E1E",text_color="#EAEAEA",wraplength=320,justify="center",padx=10,pady=6)
label.pack(pady=5,padx=10)
label.pack()
generate_quote()
close_button=ctk.CTkButton(root,text='X',width=20,height=20,command=root.destroy)
close_button.place(x=450,y=8)
root.overrideredirect(True)
root.attributes("-topmost",True)
def start_move(event):
    root.x=event.x
    root.y=event.y
def do_move(event):
    x=event.x_root -root.x
    y=event.y_root - root.y
    root.geometry(f"+{x}+{y}")
root.bind("<Button-1>",start_move)
root.bind("<B1-Motion>",do_move)
root.bind("<Escape>", lambda e:root.destroy())
root.mainloop()