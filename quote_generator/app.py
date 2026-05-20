import json
import tkinter as tk
import customtkinter as ctk
import random

with open("quote_generator/quotes.json","r") as file:
    final_list=json.load(file)
def generate_quote():
    random_quote=random.choice(final_list)
    quote=random_quote["quote"]
    author=random_quote["author"]
    label.configure(text=f'{quote}\n\n--{author}')
    root.after(10000,generate_quote)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
root=ctk.CTk()
root.title("Quote Generator")
root.geometry("600x300+850+50")
root.configure(bg_color="#121212")
frame=ctk.CTkFrame(root,bg_color="#121212")
frame.pack(expand=True,fill="both")
title=ctk.CTkLabel(frame,text="\U0001F4AD"+"Daily Quotes",font=("Segoe UI", 20, "bold"),
    text_color="white")
title.pack(pady=(10,30))
label=ctk.CTkLabel(frame,text="",font=("Poppins",18,"italic"),bg_color="#1E1E1E",text_color="#EAEAEA",wraplength=550,justify="center",padx=25,pady=25)
label.pack(pady=20)
label.pack()
generate_quote()
close_button=ctk.CTkButton(root,text='X',width=20,height=20,command=root.destroy)
close_button.place(x=560,y=10)
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