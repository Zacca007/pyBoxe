import requests


class FpiClient:
    DOMAIN: str = "https://www.fpi.it"

    URLS: dict[str, str] = {
        "athletes": f"{DOMAIN}/atleti.html",
        "qualifications": f"{DOMAIN}/index.php?option=com_callrestapi&task=json_qualifiche",
        "weights": f"{DOMAIN}/index.php?option=com_callrestapi&task=json_peso",
        "statistics": f"{DOMAIN}/index.php?option=com_callrestapi&task=json_totalizzatori",
    }

    HEADERS: dict[str, str] = {
        "Host": "www.fpi.it",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:134.0) Gecko/20100101 Firefox/134.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    # Committees mapping
    COMMITTEES: dict[str, str] = {
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

    def __init__(self):
        self._payload: dict[str, str | int] = {
            "id_tipo_tessera": 5,
            "sesso": "M",
        }
        self._session = requests.Session()
        self._session.verify = False
        self._session.headers.update(self.HEADERS)

    # ========== PAYLOAD MANAGEMENT ==========
    @property
    def committees(self) -> list[str]:
        """Returns list of available committees."""
        return list(self.COMMITTEES.keys())

    def update_committee(self, committee_name: str) -> None:
        """Updates the committee in the payload."""
        if committee_name and committee_name in self.COMMITTEES:
            self._payload["id_comitato_atleti"] = self.COMMITTEES[committee_name]
        else:
            self._payload.pop("id_comitato_atleti", None)

    def update_qualification(self, qualification_id: str) -> None:
        """Updates the qualification in the payload."""
        # Remove weight when qualification changes
        self._payload.pop("id_peso", None)

        if qualification_id:
            self._payload["qualifica"] = qualification_id
        else:
            self._payload.pop("qualifica", None)

    def update_weight(self, weight_id: str) -> None:
        """Updates the weight category in the payload."""
        if weight_id:
            self._payload["id_peso"] = weight_id
        else:
            self._payload.pop("id_peso", None)

    def get_current_qualification(self) -> str| int:
        """Returns the current qualification ID."""
        return self._payload.get("qualifica", "")

    # ========== FETCH HTML ==========
    def qualifications_html(self) -> str:
        """Fetches HTML with qualification options."""
        r = self._session.get(self.URLS["qualifications"], params=self._payload)
        r.raise_for_status()
        return r.text

    def weights_html(self) -> str:
        """Fetches HTML with weight options for current qualification."""
        if "qualifica" not in self._payload:
            raise RuntimeError("Qualifica non impostata")
        r = self._session.get(self.URLS["weights"], params=self._payload)
        r.raise_for_status()
        return r.text

    def athletes_html(self) -> str:
        """Fetches HTML with athletes list."""
        r = self._session.post(self.URLS["athletes"], params=self._payload)
        r.raise_for_status()
        return r.text

    def statistics_html(self, athlete_id: int) -> str:
        """Fetches HTML with statistics for a specific athlete."""
        r = self._session.post(self.URLS["statistics"], params={"matricola": athlete_id})
        r.raise_for_status()
        return r.text

    # ========== PAGINATION ==========
    def setup_payload_on_search(self) -> None:
        """Prepares payload for search by converting qualifica to id_qualifica and adding page."""
        qualification = self._payload.pop("qualifica", None)
        if qualification is not None:
            self._payload["id_qualifica"] = qualification
        self._payload["page"] = "1"

    def reset_payload(self) -> None:
        """Resets payload after search by converting id_qualifica back to qualifica."""
        qualification = self._payload.pop("id_qualifica", None)
        if qualification is not None:
            self._payload["qualifica"] = qualification
        self._payload.pop("page", None)

    def next_page(self) -> None:
        """Increments the page number for pagination."""
        if "page" in self._payload:
            self._payload["page"] = str(int(self._payload["page"]) + 1)