import requests
from bs4 import BeautifulSoup

class PCHelper:
    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}

    def getSoup(self, url):
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        #print(res.text)

        return BeautifulSoup(res.text,'html.parser')

    def getJsonStr(self, url):
        #print("accept url "+url)
        res = requests.get(url, headers=self.headers)
        res.encoding = 'utf-8'
        #print("get: "+res.content.decode())
        return res.content.decode()