from bs4 import BeautifulSoup
import requests
import random
import tkinter as tk
from tkinter import ttk
import json
author_list=[]
quote_list=[]
final_list=[]
for i in range(1,10):
    url=f"https://quotes.toscrape.com/page/{i}/"
    req=requests.get(url)
    soup=BeautifulSoup(req.content,'html.parser')
    content=soup.find_all('span',class_='text')
    authors=soup.find_all('small',class_='author')
    for quote in content:
        quote_list.append(quote.text)
    for author in authors:
        author_list.append(":- " +author.text)

    for a,b in zip(quote_list,author_list):
        final_list.append(a+" "+b)
with open("quotes.json","w") as file:
    json.dump(final_list,file,indent=4)
with open("quotes.json","r") as file:
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