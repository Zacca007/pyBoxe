import requests
from bs4 import BeautifulSoup, ResultSet
from core.Athlete import Athlete


class Network:
    # URLs for various API endpoints
    _URL: dict[str, str] = {
        "athletes": "https://www.fpi.it/atleti.html",
        "qualifications": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_qualifiche",
        "weights": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_peso",
        "statistics": "https://www.fpi.it/index.php?option=com_callrestapi&task=json_totalizzatori",
    }

    # HTTP headers to bypass Cloudflare restrictions
    _HEADERS: dict[str, str] = {
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

    # Committees mapping
    _COMMITTEES: dict[str, str] = {
        "C.R. ABRUZZO-MOLISE F.P.I.": "1",
        "C.R. CALABRIA F.P.I.": "3",
        "C.R. CAMPANIA F.P.I.": "4",
        "C.R. EMILIA - ROMAGNA F.P.I.": "5",
        "C.R. FRIULI V.GIULIA F.P.I.": "18",
        "C.R. LAZIO F.P.I.": "8",
        "C.R. LIGURIA F.P.I.": "7",
        "C.R. LOMBARDIA F.P.I.": "6",
        "C.R. MARCHE F.P.I.": "9",
        "C.R. PIEMONTE-VALLE D'AOSTA F.P.I.": "11",
        "C.R. PUGLIA-BASILICATA F.P.I.": "10",
        "C.R. SARDEGNA F.P.I.": "12",
        "C.R. SICILIA F.P.I.": "13",
        "C.R. TOSCANA F.P.I.": "15",
        "C.R. VENETO F.P.I.": "17",
        "DEL. PROVINCIALE DI BOLZANO F.P.I.": "2",
        "DEL. PROVINCIALE DI TRENTO F.P.I.": "14",
        "DEL. REGIONALE UMBRIA F.P.I.": "16",
    }

    _qualifications: dict[str, str] = {}
    _weights_cache: dict[str, dict[str, str]] = {}

    _payload: dict[str, str | int] = {
        "id_tipo_tessera": 5,
        "sesso": "M",
    }

    def __init__(self):
        self._session = requests.Session()
        self._session.verify = False
        self._session.headers.update(self._HEADERS)
        self._set_qualifications()

    def get_session(self) -> requests.Session:
        return self._session

    def get_committees(self) -> dict[str, str]:
        return self._COMMITTEES

    def get_qualifications(self) -> dict[str, str]:
        return self._qualifications

    def get_weights(self) -> dict[str, str]:
        return self._weights_cache.get(self._current_qualification())

    def _set_qualifications(self) -> None:
        response = self._session.get(self._URL["qualifications"], params=self._payload)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        self._qualifications = {option.text: option["value"] for option in soup.find_all("option") if option["value"]}

    def set_weights(self, qualification: str) -> None:
        if qualification not in self._weights_cache:
            response = self._session.get(self._URL["weights"], params=self._payload)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            self._weights_cache[qualification] = {
                option.text: option["value"] for option in soup.find_all("option") if option["value"]
            }

    def update_committee(self, text: str) -> None:
        self._payload["id_comitato_atleti"] = self._COMMITTEES[text]

    def update_qualification(self, text: str) -> None:
        self._payload["qualifica"] = self._qualifications[text]
        self._payload.pop("id_peso", None)
        self.set_weights(text)

    def update_weights(self, text: str) -> None:
        current_qualification = self._current_qualification()
        if current_qualification and text in self._weights_cache.get(current_qualification):
            self._payload["id_peso"] = self._weights_cache[current_qualification][text]

    def _current_qualification(self) -> str:
        for qualification, value in self._qualifications.items():
            if value == self._payload.get("qualifica"):
                return qualification

    def fix_payload(self) -> None:
        qualification = self._payload.pop("qualifica", None)
        if qualification is not None:
            self._payload["id_qualifica"] = qualification
        self._payload["page"] = "1"

    def reset_payload(self) -> None:
        qualification = self._payload.pop("id_qualifica", None)
        if qualification is not None:
            self._payload["qualifica"] = qualification
        self._payload.pop("page", None)

    def next_page(self) -> None:
        self._payload["page"] = str(int(self._payload["page"]) + 1)

    def scrap_athletes_raw_data(self) -> ResultSet:
        response = self._session.post(self._URL["athletes"], params=self._payload)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser").find_all("div", class_="atleta")

    def div_to_athlete(self, athlete_div) -> Athlete:
        button = athlete_div.find('button', class_='btn btn-dark btn-sm record')
        athlete_id = button["data-id"]
        response = self._session.post(self._URL["statistics"], params={"matricola": athlete_id})
        response.raise_for_status()
        stats = BeautifulSoup(response.text, "html.parser").find_all("td")
        return Athlete(wins=int(stats[1].text), losses=int(stats[2].text), draws=int(stats[3].text))