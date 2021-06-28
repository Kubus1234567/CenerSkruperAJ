from app import app
from app.utils import extractElement
from app.models.opinion import Opinion
import requests
import json
from bs4 import BeautifulSoup

class Shop:

    url_pre = 'https://www.opineo.pl/opinie'
    #url_post = '#tab=reviews'

    def __init__(self, shopName=None, opinions=[]):
        self.shopName = shopName
        self.opinions = opinions

    def opinionsPageUrl(self):
        return self.url_pre+'/'+self.shopName
    
    def extractShop(self):
        url = self.opinionsPageUrl()
        i = 1
        while url:
            headers = {
            'User-Agent': 'Mozilla/5.0'
            }
            respons = requests.get(url, headers=headers)
            if respons.ok:
                pageDOM = BeautifulSoup(respons.text, 'html.parser')
                opinions = pageDOM.select("div.revz_container")
                if len(opinions) == 1 and opinions[0].text == '\nBrak wpisów\n':
                    break
                for opinion in opinions:
                    self.opinions.append(Opinion().extractOpinion(opinion).transformOpinion())
            else:
                url = None
            #try:
            #    url = self.opinionsPageUrl()+'/'+i
            #except TypeError:
            #    url = None
            i+=1
            url = self.opinionsPageUrl()+'/'+str(i)


    def exportShop(self):
        with open("app/opinions/{}.json".format(self.shopName), "w", encoding="UTF-8") as jf:
            json.dump(self.todict(), jf, indent=4, ensure_ascii=False)

    def __str__(self):
        return '''shopName: {}<br>
        name: {}<br>'''.format(self.shopName, 'PLACEHOLDER')+"<br>".join(str(opinion) for opinion in self.opinions)

    def todict(self):
        return {
            "shopName": self.shopName,
            "opinions": [opinion.todict() for opinion in self.opinions]
        }

