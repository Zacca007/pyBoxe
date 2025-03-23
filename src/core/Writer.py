import openpyxl
import threading
from concurrent.futures import ThreadPoolExecutor
from core import Network, Athlete

class Writer:
    def __init__(self, network: Network, min_matches: int, max_matches: int, file_name: str):
        self.network = network
        self.min_matches = min_matches
        self.max_matches = max_matches
        self.file_name = file_name
        self._athletes: list[Athlete] = []
        self._lock = threading.Lock()  # Lock per la sincronizzazione

    def search(self) -> None:
        self.network.fix_payload()
        self.parse_athletes()
        self.write_athletes()

    def parse_athletes(self) -> None:
        with ThreadPoolExecutor(max_workers=5) as executor:  # 5 thread per le richieste
            futures = []
            while True:
                athlete_divs = self.network.scrap_athletes_raw_data()
                if not athlete_divs:
                    break
                
                for athlete_div in athlete_divs:
                    futures.append(executor.submit(self.process_athlete, athlete_div))
                
                self.network.next_page()
            
            for future in futures:
                future.result()  # Assicura che tutte le richieste siano completate
        
        self.network.reset_payload()

    def process_athlete(self, athlete_div) -> None:
        athlete = self.network.div_to_athlete(athlete_div)
        if athlete.get_matches() < self.min_matches or athlete.get_matches() > self.max_matches:
            return

        name_elem = athlete_div.find(class_='card-title')
        athlete.set_name(name_elem.text.strip())
        athlete.set_age(int(name_elem.find_next_sibling(class_='card-title').text.split(':')[-1]))
        athlete.set_club(athlete_div.find('h6', string='Società').find_next('p').text.strip())
        
        with self._lock:
            self._athletes.append(athlete)

    def write_athletes(self) -> None:
        workbook = openpyxl.Workbook()
        sheet = workbook.active
        headers = ["Name", "Age", "Club", "Matches", "Wins", "Losses", "Draws"]

        for col_num, header in enumerate(headers, start=1):
            sheet.cell(row=1, column=col_num, value=header)

        row_num = 2
        for athlete in self._athletes:
            sheet.cell(row=row_num, column=1, value=athlete.get_name())
            sheet.cell(row=row_num, column=2, value=athlete.get_age())
            sheet.cell(row=row_num, column=3, value=athlete.get_club())
            sheet.cell(row=row_num, column=4, value=athlete.get_matches())
            sheet.cell(row=row_num, column=5, value=athlete.get_wins())
            sheet.cell(row=row_num, column=6, value=athlete.get_losses())
            sheet.cell(row=row_num, column=7, value=athlete.get_draws())
            row_num += 1

        workbook.save(f"{self.file_name}.xlsx")