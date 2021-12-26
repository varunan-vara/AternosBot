from serverclass import CustomSession, Server
from hashlib import md5
from bs4 import BeautifulSoup #type:ignore

class User:
    def __init__ (self, user : str, password : str, customprint: function = print):
        self.updatecreds(user, password)
        self.customprint = customprint
    def updatecreds (self, user : str, password : str):
        self.user = user
        self.password = password
        self.session = CustomSession()
    def login(self):
        self.session.fancyget(link = "https://aternos.org/go", isUpdateToken = True, customprint=self.customprint)
        self.session.fancypost(
            link = 'https://aternos.org/panel/ajax/account/login.php?SEC=' + self.session.sec + '&TOKEN=' + self.session.token,
            customprint=self.customprint,
            data = {
                "user": "spedtreequestion",
                "password": md5("spedtreequestion".encode("utf8")).hexdigest().lower()
        }
        )
        r = self.session.ses.get('https://aternos.org/servers/')
        html = r.text
        goodSOUP = BeautifulSoup(html, features = "html.parser")
        gooddivs = str(goodSOUP.find_all("div", {"class": "server"}))
        