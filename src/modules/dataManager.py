import openpyxl
from PyQt6.QtWidgets import QMessageBox

from src.modules.netManager import NetManager

class DataManager:
    def __init__(self, net_manager: NetManager, min_matches: int, max_matches: int, file_name: str):
        self.net_manager = net_manager
        self.min_matches = min_matches
        self.max_matches = max_matches
        self.file_name = file_name

    def search(self) -> None:
        self.net_manager.fix_payload()
        self.fetch_and_display()

    def fetch_and_display(self) -> None:
        athletes: list[dict[str, str | int | dict[str, int]]] = []

        while True:
            athletes_divs = self.net_manager.get_athletes()

            if athletes_divs:
                for athlete_div in athletes_divs:
                    button = athlete_div.find('button', class_='btn btn-dark btn-sm record')
                    matricola = button["data-id"]
                    stats = self.net_manager.get_athlete_stats(matricola)

                    if not (self.min_matches <= stats["numero_match"] <= self.max_matches):
                        continue

                    name = athlete_div.find(class_='card-title').text
                    age = int(
                        athlete_div.find(class_='card-title')
                        .find_next_sibling(class_='card-title').text.split(':')[-1]
                    )
                    club = athlete_div.find('h6', string='Società').find_next('p').text

                    athletes.append({
                        "nome": name,
                        "età": age,
                        "società": club,
                        "statistiche": stats
                    })

                self.net_manager.next_page()
            else:
                wb = openpyxl.Workbook()
                sheet = wb.active
                keys = ["Nome e cognome", "Età", "Società", "Numero match", "Vittorie", "Sconfitte", "Pareggi"]
                if sheet is not None:
                    for col_num, key in enumerate(keys, start=1):
                        sheet.cell(row=1, column=col_num, value=key)
                    for row_num, atleta in enumerate(athletes, start=2):
                        sheet.cell(row=row_num, column=1, value=atleta.get("nome"))
                        sheet.cell(row=row_num, column=2, value=atleta.get("età"))
                        sheet.cell(row=row_num, column=3, value=atleta.get("società"))
                        sheet.cell(row=row_num, column=4, value=atleta["statistiche"].get("numero_match"))
                        sheet.cell(row=row_num, column=5, value=atleta["statistiche"].get("vittorie"))
                        sheet.cell(row=row_num, column=6, value=atleta["statistiche"].get("sconfitte"))
                        sheet.cell(row=row_num, column=7, value=atleta["statistiche"].get("pareggi"))

                try:
                    wb.save(f"{self.file_name}.xlsx")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Warning)  # Impostiamo l'icona come avviso (Warning)
                    msg.setWindowTitle("processo terminato")
                    msg.setText(f"File '{self.file_name}.xlsx' creato con successo!")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)  # Pulsante Ok

                    # Mostra il messaggio
                    msg.exec()
                except:
                    QMessageBox.critical(QMessageBox(), "Errore", "non è stato possibile salvare il file")
                break
