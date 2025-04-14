from bs4 import BeautifulSoup
from .athlete import FpiAthlete


class FpiParser:
    @staticmethod
    def parse_filters(html: str) -> dict[str, str]:
        """Parsa <option> in un dizionario testo→valore."""
        soup = BeautifulSoup(html, "html.parser")
        return {opt.text: opt["value"] for opt in soup.find_all("option") if opt.get("value")}

    @staticmethod
    def parse_athletes(html: str) -> list[FpiAthlete]:
        """Parsa lista atleti dal markup HTML."""
        soup = BeautifulSoup(html, "html.parser")
        athletes: list[FpiAthlete] = []
        for athlete_div in soup.find_all("div", class_="atleta"):
            title = athlete_div.find(class_="card-title")
            button = athlete_div.find("button", class_="btn btn-dark btn-sm record")

            name: str = title.text.strip()
            club: str = athlete_div.find("h6", string="Società").find_next("p").text.strip()
            age: int = int(title.find_next_sibling(class_="card-title").text.split(":")[-1])
            athlete_id: int = button["data-id"]

            athletes.append(FpiAthlete(name=name, club=club, age=age, id=athlete_id))
        return athletes

    @staticmethod
    def parse_statistics(html: str, athlete: FpiAthlete) -> FpiAthlete:
        """Parsa statistiche e aggiorna un atleta esistente."""
        soup = BeautifulSoup(html, "html.parser")
        stats = soup.find_all("td")
        athlete.wins = int(stats[1].text)
        athlete.losses = int(stats[2].text)
        athlete.draws = int(stats[3].text)
        return athlete
