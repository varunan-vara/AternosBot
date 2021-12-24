from hashlib import md5
import os
from blurple import ui #type: ignore
import requests #type:ignore
import configparser
import time
import cloudscraper #type:ignore
import random
import lxml.html #type:ignore
import re
from atjparse import exec


class CustomSession:
    def __init__ (self):
        self.ses = requests.session()
        self.sec = None
    def randval ():
        s = ""
        for i in range(16):
            s += str(random.randint(0,9))
        return s
    def get (self, customprint = print, link = "", parameters = {}, headers = {}, inputcookies = {}, isUpdateToken = False):
        if self.sec == None:
            val1 = self.randval()
            val2 = self.randval()
            self.sec = val1 + ":" + val2
            cookiekey = "ATERNOS_SEC_"
            newval2 = val2 + ";path=" + link
            self.ses.cookies.set((cookiekey + val1), newval2)
            customprint("Created randval")
        newses = requests.session()
        newses.cookies = self.ses.cookies
        r = newses.get(link, params= parameters, headers= headers, cookies= inputcookies)

        cloudfail = 0
        while 'const COOKIE_PREFIX = "ATERNOS";' not in r.text and cloudfail < 20:
            time.sleep(1)
            customprint("CloudFlare Error, Attempt Number: ", str(cloudfail + 1))
            cloudfail += 1
            r = newses.get(link, params= parameters, headers= headers, cookies= inputcookies)
        if 'const COOKIE_PREFIX = "ATERNOS";' not in r.text:
            customprint("Failed to load Aternos.org")
        else:
            webhead = lxml.html.fromString(r.content).head.textcontent()
            
            return r


    def post():
        pass

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
        

sess = cloudscraper.create_scraper()
r = sess.get("https://aternos.org/go").content
bruh = re.findall(r'\(\(\)(.*?)\)\(\);', lxml.html.fromstring(r).head.text_content())
print(len(bruh))
ctx = exec(bruh[0])
print(r)
print("\n\n")
print(bruh)
print(ctx)
print(ctx.window["AJAX_TOKEN"])



# test = User("bruh", "bruh")

