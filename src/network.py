import requests
from bs4 import BeautifulSoup

class NetManager:
    __session: requests.Session

    """
    in order to search for athletes on the website, it's required to compile a (partially) dynamically generated form.
    every field has a list of options that changes based on the combinations of options selected previously.
    in order to do that, the website uses json data to memorize the options and to get new ones.
    the payload attribute mimics is used as json in order to mimic the website structure.
    """
    __payload: dict[str, int | str]

    """
    the website uses php src to manage dynamic form compilation.
    the URL attribute serves as a collection of queries that lead to every php script necessary to compile the form.
    """
    __URL: dict[str, str] = {
        "atleti": "https://www.fpi.it/atleti.html",
        "qualifiche": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_qualifiche",
        "peso": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_peso",
        "statistiche": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_totalizzatori"
    }

    """
    for some reason, the website has recently adopted cloudflare as security service,
    this causes the program to get error status codes when sends any request to the web server is sent.
    to bypass this problem, i just copied and pasted my own request HTTP header into the session headers,
    i don't know which key - value makes the web server think i'm a human, but i don't even car
    """
    __header: dict[str, str] = {
            "Host": "www.fpi.it",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Referer": "https://www.google.com/",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "cross-site",
            "Priority": "u=0, i"
        }

    def __init__(self):
        self.__payload = {
            "id_tipo_tessera": "5",  # Atleta dilettante IBA
            "sesso": "M"
        }

        """
        the websites checks for certificates that i know nothing about.
        i don't know why, but sometimes, a computer might not have the necessary certificates.
        in order to completely avoid this problem, the verify parameter of session is set to false.
        this leads to a less secure navigation that might cause really big problems if the website is under attack,
        but since the activity on the website is very short, and the website hasn't got nothing to get attacked,
        i feel like the risk is still near to none.
        """
        self.__session = requests.Session()
        self.__session.verify = False
        self.__session.headers.update(self.__header)