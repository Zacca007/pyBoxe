from typing import Final, Dict
import requests
from bs4 import BeautifulSoup, ResultSet


class NetManager:
    __session: requests.Session
    __payload: Dict[str, int | str]
    __pesi_cache: Dict[str, Dict[str, str]]
    __qualifiche: Dict[str, str]

    __URL: Final[Dict[str, str]] = {
        "atleti": "https://www.fpi.it/atleti.html",
        "qualifiche": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_qualifiche",
        "peso": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_peso",
        "statistiche": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_totalizzatori",
    }

    __HEADERS: Final[Dict[str, str]] = {
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
        "Priority": "u=0, i",
    }

    __COMITATI: Final[Dict[str, str]] = {
        "C.R. ABRUZZO-MOLISE F.P.I.": "1",
        "C.R. CALABRIA F.P.I.": "3",
        "C.R. CAMPANIA F.P.I.": "4",
        "C.R. EMILIA - ROMAGNA F.P.I.": "5",
        "C.R. FRIULI V.GIULIA F.P.I.": "18",
        "C.R. LAZIO  F.P.I.": "8",
        "C.R. LIGURIA  F.P.I.": "7",
        "C.R. LOMBARDIA  F.P.I.": "6",
        "C.R. MARCHE F.P.I.": "9",
        "C.R. PIEMONTE-VALLE D'AOSTA F.P.I.": "11",
        "C.R. PUGLIA-BASILICATA F.P.I.": "10",
        "C.R. SARDEGNA F.P.I.": "12",
        "C.R. SICILIA  F.P.I.": "13",
        "C.R. TOSCANA  F.P.I.": "15",
        "C.R. VENETO  F.P.I.": "17",
        "DEL. PROVINCIALE DI BOLZANO F.P.I.": "2",
        "DEL. PROVINCIALE DI TRENTO F.P.I.": "14",
        "DEL. REGIONALE UMBRIA F.P.I.": "16",
    }

    def __init__(self):
        self.__payload = {"id_tipo_tessera": "5", "sesso": "M"}
        self.__pesi_cache = {}
        self.__session = requests.Session()
        self.__session.verify = False
        self.__session.headers.update(self.__HEADERS)
        self.set_qualifiche()

    def get_session(self) -> requests.Session:
        return self.__session

    def get_comitati(self) -> Dict[str, str]:
        return self.__COMITATI

    def set_qualifiche(self) -> None:
        response = self.__session.get(self.__URL["qualifiche"], params=self.__payload)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        self.__qualifiche = {opt.text: opt["value"] for opt in soup.find_all("option") if opt["value"]}

    def get_qualifiche(self) -> Dict[str, str]:
        return self.__qualifiche

    def set_pesi(self, qualifica: str) -> None:
        if qualifica not in self.__pesi_cache:
            response = self.__session.get(self.__URL["peso"], params=self.__payload)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            self.__pesi_cache[qualifica] = {
                opt.text: opt["value"] for opt in soup.find_all("option") if opt["value"]
            }

    def get_pesi(self) -> Dict[str, str]:
        current_qualifica = next(
            (name for name, q_id in self.__qualifiche.items() if q_id == self.__payload.get("qualifica")), None
        )
        return self.__pesi_cache.get(current_qualifica, {})

    def update_comitato(self, text: str) -> None:
        self.__payload["id_comitato_atleti"] = self.__COMITATI[text]

    def update_qualifica(self, text: str, on_search: bool = False) -> None:
        if on_search:
            self.__payload["id_qualifica"] = self.__payload.pop("qualifica")
        else:
            self.__payload["qualifica"] = self.__qualifiche[text]
            self.__payload.pop("id_peso", None)
            if text != "Schoolboy":
                self.set_pesi(text)

    def update_pesi(self, text: str) -> None:
        current_qualifica = next(
            (name for name, q_id in self.__qualifiche.items() if q_id == self.__payload["qualifica"]), None
        )
        if current_qualifica and text in self.__pesi_cache.get(current_qualifica, {}):
            self.__payload["id_peso"] = self.__pesi_cache[current_qualifica][text]

    def fix_payload(self) -> None:
        qualifica = self.__payload.pop("qualifica", None)
        if qualifica is not None:
            self.__payload["id_qualifica"] = qualifica
            peso = self.__payload.get("id_peso")
            if peso is not None:
                if qualifica == "20" and peso == "114":
                    self.__payload["id_peso"] = "468"
                elif qualifica == "97" and peso == "159":
                    self.__payload["id_peso"] = "429"
        self.__payload["page"] = "1"

    def get_athletes(self) -> ResultSet:
        response = self.__session.post(self.__URL["atleti"], params=self.__payload)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser").find_all("div", class_="atleta")

    def get_athlete_stats(self, matricola: str) -> Dict[str, int]:
        response = self.__session.post(self.__URL["statistiche"], params={"matricola": matricola})
        response.raise_for_status()
        stats = BeautifulSoup(response.text, "html.parser").find_all("td")
        return {"numero_match": int(stats[0].text), "vittorie": int(stats[1].text), "sconfitte": int(stats[2].text), "pareggi": int(stats[3].text)}

    def next_page(self) -> None:
        self.__payload["page"] = str(int(self.__payload["page"]) + 1)
