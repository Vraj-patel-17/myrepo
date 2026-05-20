from bs4 import BeautifulSoup
import requests
import json
final_list=[]
for i in range(1,10):
    url=f"https://quotes.toscrape.com/page/{i}/"
    req=requests.get(url)
    soup=BeautifulSoup(req.content,'html.parser')
    quotes=soup.find_all('span',class_='text')
    authors=soup.find_all('small',class_='author')
    for quote,author in zip(quotes,authors):
        data={"quote":quote.text
              ,"author":author.text}
        final_list.append(data)
with open("quote_generator/quotes.json","w") as file:
    json.dump(final_list,file,indent=4)

