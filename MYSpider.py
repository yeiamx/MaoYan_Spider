from PCHelper import *
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time

class MYSpider:
    def __init__(self, Url):
        self.Url = Url
        self.pcHelper = PCHelper()
        self.soup = self.pcHelper.getSoup(Url)
        self.cinemaNameList = []
        self.cinemaDataList = []
        self.cinemaHrefList = []
        self.cinemaInfo = {}
        self.cinemaYearRecords = {}

    def processDataWithRange(self, urlStarter, limit=20, offset=0):
        date = time.strftime("%Y-%m-%d")
        url = urlStarter+"/filter?typeId=0&date="+date+"&offset="+str(offset)+"&limit="+str(limit)
        #print("using: "+url)
        cinemaInfoJsonStr = self.pcHelper.getJsonStr(url)
        #print(cinemaInfoJsonStr)
        cinemaInfoJsonStr = cinemaInfoJsonStr.replace("true", "True")
        cinemaInfoJsonStr = cinemaInfoJsonStr.replace("false", "False")
        cinemaInfoJsonStr = cinemaInfoJsonStr.replace("null", "0")
        cinemaInfoJsonObj = eval(cinemaInfoJsonStr)['data']

        currentTime = cinemaInfoJsonObj['updateInfo'].split(" ")[-1]
        #print(currentTime)
        self.currentTime = date+" "+currentTime

        cinemaInfoList = cinemaInfoJsonObj['list']
        for cinemaInfoObj in cinemaInfoList:
            self.cinemaNameList.append(cinemaInfoObj['cinemaName'])
            cinemaData = {}
            cinemaData['票房'] = cinemaInfoObj['boxInfo']
            cinemaData['人次'] = cinemaInfoObj['viewInfo']
            cinemaData['场均人次'] = cinemaInfoObj['avgShowView']
            cinemaData['平均票价'] = cinemaInfoObj['avgViewBox']
            self.cinemaDataList.append(cinemaData)
            self.cinemaHrefList.append(self.Url+"/"+str(cinemaInfoObj['cinemaId']))

       #Get All cinema data
        for i in range(len(self.cinemaDataList)):
            self.cinemaInfo[self.cinemaNameList[i]] = self.cinemaDataList[i]

        #Get cinema's year records from href list.
        for i in range(len(self.cinemaHrefList)):
            cinemaYearList = self.getCinemaYearRecord(self.cinemaHrefList[i])
            self.cinemaYearRecords[cinemaInfoList[i]['cinemaName']] = cinemaYearList


    def processData(self):
        date = self.soup.find("span", attrs={"class", "date"}).string
        week = self.soup.find("span", attrs={"class", "week"}).string
        time = self.soup.find("p", attrs={"class", "time-bar"}).string.split(" ")[1]
        self.currentTime = date+" ("+week+") "+time

        t_table = self.soup.find_all("div", {"class", "t-table"})[0]
        t_left = t_table.find_all("div", {"class", "t-left"})[0]
        cinemaTags = t_left.find_all("div", {"class", "t-cell"})
        for cinemaTag in cinemaTags:
            self.cinemaNameList.append(cinemaTag.string)

        #Get All cinema names
        t_right = t_table.find_all("div", {"class", "t-right"})[0]
        cinemaDataTags = t_right.find_all("div", {"class", "t-row"})
        for cinemaDataTag in cinemaDataTags:
            dataList = cinemaDataTag.find_all("p")
            cinemaData = {}
            cinemaData['票房'] = dataList[0].string
            cinemaData['人次'] = dataList[1].string
            cinemaData['场均人次'] = dataList[2].string
            cinemaData['平均票价'] = dataList[3].string
            self.cinemaDataList.append(cinemaData)

        #Get All cinema data
        for i in range(len(self.cinemaDataList)):
            self.cinemaInfo[self.cinemaNameList[i]] = self.cinemaDataList[i]

        #Get AppData from script
        appDataStr = self.soup.find_all("script")[1].string
        appDataStr = appDataStr[14:-1]
        #print(appDataStr.find("false"))
        appDataStr = appDataStr.replace("false", "False")
        appDataStr = appDataStr.replace("true", "True")
        appDataStr = appDataStr.replace("null", "0")
        #print(appDataStr)
        self.appData = eval(appDataStr)

        #Get hrefs from AppData
        pageData = self.appData['pageData']
        cinemaAppDataList = pageData['list']
        for cinemaAppData in cinemaAppDataList:
            self.cinemaHrefList.append(self.Url+"/"+str(cinemaAppData['cinemaId']))

        #Get cinema's year records from href list.
        for i in range(len(self.cinemaHrefList)):
            cinemaYearList = self.getCinemaYearRecord(self.cinemaHrefList[i])
            self.cinemaYearRecords[cinemaAppDataList[i]['cinemaName']] = cinemaYearList

    def getCinemaYearRecord(self, url):

        url = url+"/opdata?dateType=3"
        yearJsonStr = self.pcHelper.getJsonStr(url)
        yearJsonObject = eval(yearJsonStr)
        #print(yearJsonObject)
        chartData = eval(yearJsonObject['chartData'])
        #print(chartData)
        yearLabel = chartData['label']
        boxMoney = chartData['box']

        cinemaYearRecord = {}
        cinemaYearRecord['year'] = yearLabel
        cinemaYearRecord['box'] = boxMoney

        return cinemaYearRecord