from typing import Final
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
    __URL: Final[dict[str, str]] = {
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
    __header: Final[dict[str, str]] = {
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

    __comitati: Final[dict[str, str]] = {
        'Comitato': '',
        'C.R. ABRUZZO-MOLISE F.P.I.': '1',
        'C.R. CALABRIA F.P.I.': '3',
        'C.R. CAMPANIA F.P.I.': '4',
        'C.R. EMILIA - ROMAGNA F.P.I.': '5',
        'C.R. FRIULI V.GIULIA F.P.I.': '18',
        'C.R. LAZIO  F.P.I.': '8',
        'C.R. LIGURIA  F.P.I.': '7',
        'C.R. LOMBARDIA  F.P.I.': '6',
        'C.R. MARCHE F.P.I.': '9',
        "C.R. PIEMONTE-VALLE D'AOSTA F.P.I.": '11',
        'C.R. PUGLIA-BASILICATA F.P.I.': '10',
        'C.R. SARDEGNA F.P.I.': '12',
        'C.R. SICILIA  F.P.I.': '13',
        'C.R. TOSCANA  F.P.I.': '15',
        'C.R. VENETO  F.P.I.': '17',
        'DEL. PROVINCIALE DI BOLZANO F.P.I.': '2',
        'DEL. PROVINCIALE DI TRENTO F.P.I.': '14',
        'DEL. REGIONALE UMBRIA F.P.I.': '16'
    }

    __qualifiche: dict[str, str] = {
        'Elite': '97',
        'Elite II': '168',
        'Junior': '139',
        'Schoolboy': '17',
        'Youth': '20'
    }
    __pesi: dict[str, str]

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

    """
    __comitati dict is hard coded for efficiency reasons.
    if any values changes, just run this method, copy and paste the new dict and hard code it again.
    
    def setComitati(self) -> None:
        response = self.__session.get(self.__URL["atleti"])
        response.raise_for_status()  # Solleva HTTPError se lo status non è 200

        soup = BeautifulSoup(response.text, "html.parser")
        select_element = soup.find("select", id="id_comitato_atleti")

        if not select_element:
            raise ValueError("Elemento <select> con id 'id_comitato_atleti' non trovato nella pagina.")

        self.__comitati = {option.text.strip(): option["value"] for option in select_element.find_all("option")}
    """

    def getComitati(self) -> dict[str, str]:
        return self.__comitati

    def getqUalifiche(self) -> dict[str, str]:
        return self.__qualifiche

    """
    the setPesi can become setQualifiche if the url is changed.
    since the 'id_tipo_tessera' key in the payload has got a hard coded value, the result from setQualifiche will always be the same.
    if the websites updates and any value changes, just run the method switching the url from pesi to qualifiche to get the new dict
    """
    def setPesi(self) -> None:
        response = self.__session.get(self.__URL["pesi"], params=self.__payload)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        self.__pesi = {option.text: option["value"] for option in soup.find_all("option") if option['value']}

    def getPesi(self) -> dict[str, str]:
        return self.__pesi

if __name__ == "__main__":
    nm = NetManager()
