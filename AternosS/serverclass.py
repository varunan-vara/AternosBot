from hashlib import md5
import hashlib
import os
from blurple import ui #type: ignore
import requests #type:ignore
import configparser
import time
import cloudscraper #type:ignore
import random
from returntoken import convertToken
from bs4 import BeautifulSoup #type:ignore


class CustomSession:
    def __init__ (self):
        self.ses = requests.session()
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
        else:
            self.ses = newses
            isArrowFunction = True
            while isArrowFunction:
                try:
                    if isUpdateToken:
                        self.token = convertToken(r)
                        isArrowFunction = False
                except:
                    r = newses.get(link , params= parameters, headers= headers, cookies= inputcookies)
    def fancypost(self, customprint = print, link = "", data = {}, headers = {}, inputcookies = {}):
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        newses = cloudscraper.create_scraper()
        newses.cookies = self.ses.cookies
        try:
            data["TOKEN"] = self.token
        except:
            customprint("No Token provided")
            return
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
        else:
            self.ses = newses

class server:
    def __init__ (self):
        print("Initialized Server")

class User:
    def __init__ (self, printfunc = print):    
        # This bot currently only accepts one account
        # Add bot information in settings.ini
        printfunc("Initializing New Class User")
        self.s = requests.session()
        self.w = []
        self.printfunc = printfunc
        self.isActive = False
    def authenticate (self, username = "", password = ""):
        if username == "":
            authget = configparser.ConfigParser()
            cwd = os.getcwd()
            filePath = cwd + "\settings.ini"
            authget.read(filePath)
            if authget["ACCOUNT"]["user"] == "user":
                self.printfunc("Account info not found")
                return None
            username = authget["ACCOUNT"]["user"]
            password = password.encode("utf8")
            password = md5(password).hexdigest()    
        if type(username) != str or type(password) != str:
            self.printfunc("Invalid User and Password")
            return None

sesh = CustomSession()
sesh.fancyget(link = "https://aternos.org/go", isUpdateToken = True)
print(md5("spedtreequestion".encode("utf-8")).hexdigest().lower())
sesh.fancypost(
    link = 'https://aternos.org/panel/ajax/account/login.php?SEC=' + sesh.sec + '&TOKEN=' + sesh.token,
    data = {
        "user": "spedtreequestion",
        "password": hashlib.md5("spedtreequestion".encode("utf8")).hexdigest().lower()
    }
    )
print(sesh.ses.cookies)
r = sesh.ses.get('https://aternos.org/servers/')
html = r.text
goodSoup = BeautifulSoup(html, features="html.parser")
gooddivs = str(goodSoup.find_all("div", {"class": "server"}))
divlist = gooddivs.split("<div class=")
print(divlist)
