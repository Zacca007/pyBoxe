import json

from src.modules.netManager import NetManager


class DataManager:
    netManager: NetManager
    min_matches: int
    max_matches: int

    def __init__(self, netManager: NetManager, min_matches: int, max_matches: int):
        self.netManager = netManager
        self.min_matches = min_matches
        self.max_matches = max_matches

    def search(self) -> None:
        self.netManager.fixPayload()
        self.fetch_and_display()

    def fetch_and_display(self) -> None:
        atheletes: list[dict[str, str | int | dict[str, int]]] = list()
        while True:
            atheles_divs = self.netManager.getAthletes()
            if len(atheles_divs) != 0:
                for athlete_div in atheles_divs:
                    nome = athlete_div.find(class_='card-title').text
                    eta = int(
                        athlete_div.find(class_='card-title').find_next_sibling(class_='card-title').text.split(':')[
                            -1])
                    societa = athlete_div.find('h6', string='Società').find_next('p').text
                    bottone = athlete_div.find('button', class_='btn btn-dark btn-sm record')
                    matricola = bottone["data-id"]
                    statistiche = self.netManager.getAthleteStats(matricola)
                    if self.min_matches <= statistiche["numero_match"] <= self.max_matches:
                        atheletes.append({
                            "nome": nome,
                            "età": eta,
                            "società": societa,
                            "statistiche": statistiche
                        })
                self.netManager.nextPage()
            else:
                print("finito")
                print(json.dumps(atheletes, indent=4))
                break
