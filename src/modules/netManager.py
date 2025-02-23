from http.client import responses
from typing import Final, Dict
import requests
from bs4 import BeautifulSoup, ResultSet


class NetManager:
    __session: requests.Session
    __payload: dict[str, int | str]
    __pesi_cache: Dict[str, Dict[str, str]]
    __qualifiche: dict[str, str]

    __URL: Final[dict[str, str]] = {
        "atleti": "https://www.fpi.it/atleti.html",
        "qualifiche": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_qualifiche",
        "peso": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_peso",
        "statistiche": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_totalizzatori"
    }

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

    def __init__(self):
        self.__payload = {
            "id_tipo_tessera": "5",  # Atleta dilettante IBA
            "sesso": "M"
        }

        self.__pesi_cache = {}

        self.__session = requests.Session()
        self.__session.verify = False
        self.__session.headers.update(self.__header)

        self.setQualifiche()

    def getSession(self) -> requests.Session:
        return self.__session

    def getComitati(self) -> dict[str, str]:
        return self.__comitati

    def setQualifiche(self) -> None:
        response = self.__session.get(self.__URL["qualifiche"], params=self.__payload)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        self.__qualifiche = {option.text: option["value"] for option in soup.find_all("option") if option['value']}

    def getQualifiche(self) -> dict[str, str]:
        return self.__qualifiche

    def setPesi(self, qualifica: str) -> None:
        if qualifica not in self.__pesi_cache:
            response = self.__session.get(self.__URL["peso"], params=self.__payload)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            self.__pesi_cache[qualifica] = {
                option.text: option["value"]
                for option in soup.find_all("option")
                if option['value']
            }

    def getPesi(self) -> dict[str, str]:
        current_qualifica = None
        for q_name, q_id in self.__qualifiche.items():
            if q_id == self.__payload.get("qualifica"):
                current_qualifica = q_name
                break

        return self.__pesi_cache.get(current_qualifica, {})

    def updateComitato(self, text: str) -> None:
        self.__payload["id_comitato_atleti"] = self.__comitati[text]
        print(self.__payload)

    def updateQualifica(self, text: str, on_search: bool = False) -> None:
        if on_search:
            self.__payload["id_qualifica"] = self.__payload.pop("qualifica")
        else:
            self.__payload["qualifica"] = self.__qualifiche[text]
            if "id_peso" in self.__payload:
                self.__payload.pop("id_peso")

            # Se non è Schoolboy, carica i pesi se non sono in cache
            if text != "Schoolboy":
                self.setPesi(text)
        print(self.__payload)

    def updatePesi(self, text: str) -> None:
        current_qualifica = next(
            (q_name for q_name, q_id in self.__qualifiche.items()
             if q_id == self.__payload["qualifica"]),
            None
        )
        if current_qualifica and text in self.__pesi_cache[current_qualifica]:
            self.__payload["id_peso"] = self.__pesi_cache[current_qualifica][text]
        print(self.__payload)

    def fixPayload(self) -> None:
        qualifica = self.__payload.pop("qualifica")
        if qualifica is not None:
            self.__payload["id_qualifica"] = qualifica
            peso = self.__payload["id_peso"]
            if peso is not None:
                if qualifica == 20 and peso == 114:
                    self.__payload["id_peso"] = 468
                elif qualifica == 97 and peso == 159:
                    self.__payload["id_peso"] = 429
        self.__payload["page"] = "1"

    def getAthletes(self) -> ResultSet:
        response = self.__session.post(self.__URL["atleti"], params=self.__payload)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all("div", class_="atleta")

    def getAthleteStats(self, matricola: str) -> dict[str, int]:
        response = self.__session.post(self.__URL["statistiche"], params={"matricola": matricola})
        response.raise_for_status()
        stats = BeautifulSoup(response.text, 'html.parser').find_all("td")
        statistiche = {
            "numero_match": int(stats[0].text),
            "vittorie": int(stats[1].text),
            "sconfitte": int(stats[2].text),
            "pareggi": int(stats[3].text),
        }
        return statistiche

    def nextPage(self) -> None:
        page = int(self.__payload["page"]) + 1
        self.__payload["page"] = str(page)