#@KatsiarynaVol
#https://t.me/KatsiarynaVol

import telebot
import json
from setting import botToken
from bs4 import BeautifulSoup
import requests

bot = telebot.TeleBot (botToken)

with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8",
        "Accept-Language": "en"
    }
url = 'https://sneakerstore.by/'

#получили ссылку на 1 стр
def urls(url):
    resp = se.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    links = soup.findAll("a", class_="nav__link js-popup-call-hover")
    url_kross = []
    for x in links:
        x= x.get('href')
        url_kross.append(x)
    contact=soup.find("span",  itemprop="telephone")
    contact=contact.find("a").get("href")
    contact="+"+str(contact[4:])

    return url_kross[0]


#получили все ссылки
def all_url(urls):
    page=32
    all_link=[]
    for i in range(1,page+1):
        url = str(urls) + str('?page=')+str(i)
        resp = se.get(url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        all_url = soup.findAll("a", class_="products-list__img-item")
        for x in all_url:
            x= x.get('href')
            if x not in all_link:
                all_link.append(x)
    all_link=list((all_link))
    #print(len(all_link))

    return all_link

#получили все сведения
def dict_(all_urls):
    data_dict= []
    all_brend = []
    sizes=[]
    count=0
    try:

        for i in all_urls:
            resp = se.get(i)
            soup = BeautifulSoup(resp.text, 'html.parser')
            all_name = soup.findAll("h1", class_="catalogue__product-name")
            try:
                for z in all_name:
                    z=z.text.split()
                    link = i
                    model = z[2:]
                    model=' '.join(model)
                    brend=z[1]
                    if brend not in all_brend:
                        all_brend.append(brend)
                all_prise=soup.findAll("span", class_="catalogue__price catalogue__price--lg")
                #print(all_prise)
            except:
                pass
            for x in all_prise:
                price=x.find('span').text[:-6]
                #print(price)
                all_size=soup.findAll("div", class_="product-page__input-box")
                size=[]
                for n in all_size:
                    n = n.findAll("label")
                for t in n:
                    t=t.text.strip()
                    #print(t)
                    size.append(t)
                    if t not in sizes:
                        sizes.append(t)

            photo=soup.findAll("a",class_="js-fancy-img")
            photo_arr=[]
            for j in photo:
                j = j.get('href')
                #j=j.replace(' ', "").split(",")
                photo_arr.append(j)

            id_prodyct = soup.find("span", class_="product-page__vendor-code")
            id_prodyct=(id_prodyct).text[12:]
            size = " ".join(size)
            data = {  "brand":brend,
                         "link": link,
                      "id_prodyct":id_prodyct,
                          "model": model,
                          "price":price,
                          "size":size,
                          "photo":photo_arr}
            data_dict.append(data)
            #print(data_dict)
        # dict_card={}
        # for i in range(len(data_dict)-1):
        #     dict_card[str(i)]=data_dict[i]
        # print(dict_card)
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data_dict, f, ensure_ascii=False, indent=4)
            #print(data_dict)
        #print(data_dict)
    except:
        pass
    print(sizes)
    print(all_brend)
    return sizes, all_brend

# вызывает основную функцию
dict_(all_url(urls(url)))

sizes=['36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '42.5', '36.5', '44.5']
all_brand=['Saucony', 'Retropy', 'Nike',  'Niteball',  'Bad', 'Jordan',  'Slide', 'Balenciaga', 'superstar', 'Forum', 'Premiata', 'Dior', 'ZX', 'Rebasus', 'Adiprene', 'Adi2000', 'Ozelia',  'SB', 'nite', 'Converse',  'кеды', 'Fei', 'zx', 'Dr.Martens', 'Spezial', 'COLUMBIA', 'Ozweego', 'climacool', 'zx500', 'BLAZER', 'High', 'Brown', 'Dunk', 'Jazz', 'Black\\Orange', 'Air', 'Sonic', 'Yeezy', 'deerupt']





