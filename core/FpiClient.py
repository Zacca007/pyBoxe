import requests

DOMAIN: str = "https://www.fpi.it"

URLS: dict[str, str] = {
    "atleti": f"{DOMAIN}/atleti.html",
    "qualifiche": f"{DOMAIN}/index.php?option=com_callrestapi&task=json_qualifiche",
    "pesi": f"{DOMAIN}/index.php?option=com_callrestapi&task=json_peso",
    "statistiche": f"{DOMAIN}/index.php?option=com_callrestapi&task=json_totalizzatori",
}

HEADERS: dict[str, str] = {
    "Host": "www.fpi.it",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:145.0) Gecko/20100101 Firefox/145.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Priority": "u=0, i",
}


class FpiClient:
    """Client per interagire con l'API FPI."""
    
    def __init__(self):
        self._payload: dict[str, str | int] = {
            "id_tipo_tessera": 5,
            "sesso": "M",
        }
        self._session = requests.Session()
        self._session.headers.update(HEADERS)

    def athletes_html(self) -> str:
        """
        Recupera l'HTML con la lista degli atleti.
        
        Returns:
            HTML della pagina con gli atleti
        """
        r = self._session.post(URLS["atleti"], params=self._payload)
        r.raise_for_status()
        return r.text

    def statistics_html(self, athlete_id: int) -> str:
        """
        Recupera l'HTML con le statistiche di un atleta specifico.
        
        Args:
            athlete_id: ID dell'atleta
            
        Returns:
            HTML con le statistiche
        """
        r = self._session.post(URLS["statistiche"], params={"matricola": athlete_id})
        r.raise_for_status()
        return r.text

    def qualifiche_html(self) -> str:
        """
        Recupera l'HTML con le opzioni di qualifica.
        
        Returns:
            HTML con le opzioni <option> per il select delle qualifiche
        """
        r = self._session.get(URLS["qualifiche"], params=self._payload)
        r.raise_for_status()
        return r.text

    def pesi_html(self) -> str:
        """
        Recupera l'HTML con le opzioni di peso per la qualifica corrente.
        
        Returns:
            HTML con le opzioni <option> per il select dei pesi
            
        Raises:
            RuntimeError: Se la qualifica non è impostata
        """
        if "qualifica" not in self._payload:
            raise RuntimeError("Qualifica non impostata")
        r = self._session.get(URLS["pesi"], params=self._payload)
        r.raise_for_status()
        return r.text

    def update_comitato(self, id: str | None) -> None:
        """
        Aggiorna il comitato nel payload.
        
        Args:
            id: ID del comitato (None per rimuovere)
        """
        if id:
            self._payload["id_comitato_atleti"] = id
        else:
            self._payload.pop("id_comitato_atleti", None)

    def update_qualifiche(self, id: str | None) -> None:
        """
        Aggiorna la qualifica nel payload.
        Rimuove automaticamente il peso quando la qualifica cambia.
        
        Args:
            id: ID della qualifica (None per rimuovere)
        """
        # Rimuovi il peso quando la qualifica cambia
        self._payload.pop("id_peso", None)

        if id:
            self._payload["qualifica"] = id
        else:
            self._payload.pop("qualifica", None)

    def update_pesi(self, id: str | None) -> None:
        """
        Aggiorna la categoria di peso nel payload.
        
        Args:
            id: ID del peso (None per rimuovere)
        """
        if id:
            self._payload["id_peso"] = id
        else:
            self._payload.pop("id_peso", None)

    def setup_payload_on_search(self) -> None:
        """
        Prepara il payload per la ricerca convertendo 'qualifica' in 'id_qualifica'
        e aggiungendo la paginazione.
        """
        qualifica = self._payload.pop("qualifica", None)
        if qualifica is not None:
            self._payload["id_qualifica"] = qualifica
        self._payload["page"] = "1"

    def reset_payload(self) -> None:
        """
        Resetta il payload dopo la ricerca, riconvertendo 'id_qualifica' in 'qualifica'
        e rimuovendo la paginazione.
        """
        qualifica = self._payload.pop("id_qualifica", None)
        if qualifica is not None:
            self._payload["qualifica"] = qualifica
        self._payload.pop("page", None)

    def next_page(self) -> None:
        """Incrementa il numero di pagina per la paginazione."""
        if "page" in self._payload:
            self._payload["page"] = str(int(self._payload["page"]) + 1)