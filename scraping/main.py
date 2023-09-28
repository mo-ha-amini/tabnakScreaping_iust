
import requests
import html5lib
from tqdm import tqdm
import convert_numbers
from bs4 import BeautifulSoup
from datetime import datetime
  
def getnewsLink():
    links = []
    # cart_id = [0,1,2,3,4,5,6,8,9,10,11,19,22,23,24,42,51,59,71,72,75,95,96,98,99,100,101,102,103,138,139,140,141,142,143,144,145,146,147,148,149,182,184,185,186,187,188,245]
    cart_id = [1]
    
    for id in tqdm(cart_id):
        for page in range(0,1):
            URL = "https://www.tabnak.ir/fa/archive?service_id=1&sec_id=-1&cat_id="+ str(id) +"&rpp=20&from_date=1384/01/01&to_date=1402/07/04&p=" + str(page)
            r = requests.get(URL)
            soup = BeautifulSoup(r.content, 'html5lib')

            linksElement = soup.find_all("div", {"class":"linear_news"})
            for element in linksElement:
                link = element.findChild('a')
                link = "https://www.tabnak.ir" + link['href']
                links.append(link)
    with open('links.txt', 'w',  encoding='utf-8') as writer:
        for link in links:        
            writer.write(str(link))
            writer.write('\n')            
    
    return links

def convertToDateTimeformat(persianDate, enDate):
    time = persianDate.split(" ")[4]
    hour = convert_numbers.persian_to_english(time.split(":")[0])
    minute = convert_numbers.persian_to_english(time.split(":")[1])
    time = hour + ':' + minute

    dateTime = enDate +" " +time
    dateTime = datetime.strptime(dateTime, "%d %B %Y %H:%M")
    return dateTime


def scarpeEachLink(links):
    data = []
    arrayOfText = []
    for link in tqdm(links):
        news = ()
        r = requests.get(link)
        soup = BeautifulSoup(r.content, 'html5lib')

        newsTitle = soup.find('h1', {"class":"Htag"})
        if newsTitle != None:
            newsTitle = newsTitle.text.strip()
            newsViews = soup.find('div', {"class":"news_nav news_hits visible-xs"}).findChildren('span')[1].text.strip()
            newsCode = convert_numbers.persian_to_english(soup.find('span', {"class":"news_id"}).text.strip())
            news += (int(newsCode),)
            news += (newsTitle,)
            news += (int(newsViews),)


            persianDate = soup.find('span', {"class":"fa_date"}).text.strip()
            enDate = soup.find('span', {"class":"en_date visible-lg visible-md"}).text.strip()
            newsDateTime = convertToDateTimeformat(persianDate, enDate)
            news += (newsDateTime,)
            
            newsBody = soup.find('div', {"id":"newsMainBody"})
            paraChilds = newsBody.findChildren("p")
            newsText = ''
            if len(paraChilds) !=0:
                for para in paraChilds:
                    newsText += para.text.strip()
            else:
                newsText += newsBody.text.strip()
            
            news+=(newsText,)
            
            arrayOfText.append(newsText)

            shortlink =soup.find('input', {"id":"foo"})
            shortlink = shortlink['value']
            news+= (shortlink,)

        data.append(news)

    with open('textArr.txt', 'w',  encoding='utf-8') as writer:
            # for row in data:
            #     writer.write(str(row))
            #     writer.write('\n')
        writer.write(str(arrayOfText))

def main():
    links = getnewsLink()
    scarpeEachLink(links)

main()
