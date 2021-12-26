import time
import cloudscraper #type:ignore
import random
from returntoken import convertToken

from hashlib import md5
from bs4 import BeautifulSoup #type:ignore
import json

import os
from blurple import ui #type: ignore
import requests #type:ignore
import configparser


class CustomSession:
    def __init__ (self):
        self.ses = cloudscraper.create_scraper()
        self.sec = None
        self.token = ""
    def randval (self):
        s = ""
        for i in range(16):
            s += str(random.randint(0,9))
        return s
    def fancyget (self, customprint = print, link = "", parameters = {}, headers = {}, inputcookies = {}, isUpdateToken = False):
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        if self.token == "":
            isUpdateToken = True
        else: 
            parameters["TOKEN"] = self.token
            # customprint("Token Found")
        if self.sec == None:
            val1 = self.randval()
            val2 = self.randval()
            self.sec = val1 + ":" + val2
            cookiekey = "ATERNOS_SEC_"
            newval2 = val2 + ";path=" + link
            self.ses.cookies.set((cookiekey + val1), newval2)
            customprint("Created randval")
            parameters["SEC"] = self.sec
        newses = cloudscraper.create_scraper()
        customprint("CloudScraper created")
        newses.cookies = self.ses.cookies
        r = newses.get(link , params= parameters, headers= headers, cookies= inputcookies)
        cloudfail = 0
        while '<title>Please Wait... | Cloudflare</title>' in r.text and cloudfail < 20:
            time.sleep(5)
            customprint("CloudFlare Error, Attempt Number: ", str(cloudfail + 1))
            cloudfail += 1
            r = newses.get(link, params= parameters, headers= headers, cookies= inputcookies)
        if '<title>Please Wait... | Cloudflare</title>' in r.text:
            customprint("Failed to load Aternos.org")
            return
        else:
            self.ses = newses
            isArrowFunction = True
            while isArrowFunction:
                try:
                    if isUpdateToken:
                        self.token = convertToken(r)
                        isArrowFunction = False
                except:
                    customprint("Error: Function does not support ArrowFunctions. \nRetrying convertToken() - This may take a few attempts")
                    r = newses.get(link , params= parameters, headers= headers, cookies= inputcookies)
        customprint("Get Request Completed")
    def fancypost(self, customprint = print, link = "", data = {}, headers = {}, inputcookies = {}):
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        newses = cloudscraper.create_scraper()
        newses.cookies = self.ses.cookies
        try:
            data["TOKEN"] = self.token
        except:
            customprint("No Token provided")
        if self.sec == None:
            customprint("No SEC, run CustomSessio().get()")
            return
        else: data["SEC"] = self.sec
        for item in self.ses.cookies.get_dict():
            if "_SEC_" in item:
                inputcookies[item] = self.ses.cookies.get(item)
        r = newses.post(link, data = data, headers= headers, cookies = inputcookies)
        cloudfail = 0
        while '<title>Please Wait... | Cloudflare</title>' in r.text and cloudfail < 20:
            time.sleep(5)
            customprint("CloudFlare Error, Attempt Number: ", str(cloudfail + 1))
            cloudfail += 1
            r = newses.post(link, data= data, headers= headers, cookies= inputcookies)
        if '<title>Please Wait... | Cloudflare</title>' in r.text:
            customprint("Failed to load Aternos.org")
            return
        else:
            self.ses = newses
        customprint("Post Request Completed")
    def refreshScraper (self, keepCookies = True):
        if keepCookies:
            try:
                cookies = self.ses.cookies
            except:
                cookies = None
        self.ses = cloudscraper.create_scraper()
        self.ses.cookies = cookies

class Server:
    def __init__ (self):
        print("Initialized Server")


sesh = CustomSession()
sesh.fancyget(link = "https://aternos.org/go", isUpdateToken = True)
print(md5("spedtreequestion".encode("utf-8")).hexdigest().lower())
sesh.fancypost(
    link = 'https://aternos.org/panel/ajax/account/login.php?SEC=' + sesh.sec + '&TOKEN=' + sesh.token,
    data = {
        "user": "spedtreequestion",
        "password": md5("spedtreequestion".encode("utf8")).hexdigest().lower()
    }
    )
print(sesh.ses.cookies)
r = sesh.ses.get('https://aternos.org/servers/')
html = r.text
goodSoup = BeautifulSoup(html, features="html.parser")
gooddivs = str(goodSoup.find_all("div", {"class": "server"}))
divlist = gooddivs.split("<div class=")
serverid = ""
for div in divlist:
    if "data-id" in div:
        ids = div.split('ata-id="')
        ids = ids[1].split('">\n')
        serverid = ids[0]
        break
print("Server ID: ", serverid)

parameters = {}
parameters["SEC"] = sesh.sec
parameters["TOKEN"] = sesh.token
headers1 = {}
headers1["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"

print(sesh.sec)

# sesh.refreshScraper()
# newr = sesh.fancyget(
#     link="https://aternos.org/panel/ajax/start.php",
#     parameters = parameters,
#     headers = headers1,
#     inputcookies = {
#         'ATERNOS-SERVER': serverid
#     }
# )
# sesh.refreshScraper()
# newnewr = sesh.ses.get('https://aternos.org/server/')
# print("newr json: ", newr.json)
# print("newnewr json: ",newnewr.json)