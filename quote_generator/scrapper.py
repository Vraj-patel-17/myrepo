from bs4 import BeautifulSoup
import requests
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
with open("quote_generator/quotes.json","w") as file:
    json.dump(final_list,file,indent=4)

