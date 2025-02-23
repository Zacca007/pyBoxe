import openpyxl
from PyQt6.QtWidgets import QMessageBox
from src.modules.netManager import NetManager

class DataManager:
    def __init__(self, net_manager: "NetManager", min_matches: int, max_matches: int, file_name: str):
        self.net_manager = net_manager
        self.min_matches = min_matches
        self.max_matches = max_matches
        self.file_name = file_name

    def search(self) -> None:
        """
        Initiates the search by fixing the payload and then fetching and displaying athletes.
        """
        self.net_manager.fix_payload()
        self.fetch_and_display()

    def fetch_and_display(self) -> None:
        """
        Fetches athlete data page by page, filters them based on match count,
        and writes the results to an Excel file.
        """
        athletes: list[dict[str, str | int | dict[str, int]]] = list()

        while True:
            athlete_divs = self.net_manager.get_athletes()

            if athlete_divs:
                for athlete_div in athlete_divs:
                    button = athlete_div.find('button', class_='btn btn-dark btn-sm record')
                    athlete_id = button["data-id"]
                    stats = self.net_manager.get_athlete_stats(athlete_id)

                    # Filter athletes based on match count
                    if not (self.min_matches <= stats["matches"] <= self.max_matches):
                        continue

                    # Extract athlete details
                    name = athlete_div.find(class_='card-title').text
                    age_text = athlete_div.find(class_='card-title').find_next_sibling(class_='card-title').text
                    age = int(age_text.split(':')[-1])
                    club = athlete_div.find('h6', string='Società').find_next('p').text

                    athletes.append({
                        "name": name,
                        "age": age,
                        "club": club,
                        "stats": stats
                    })

                self.net_manager.next_page()
            else:
                workbook = openpyxl.Workbook()
                sheet = workbook.active
                headers = ["Name", "Age", "Club", "Matches", "Wins", "Losses", "Draws"]

                for col_num, header in enumerate(headers, start=1):
                    sheet.cell(row=1, column=col_num, value=header)
                for row_num, athlete in enumerate(athletes, start=2):
                    sheet.cell(row=row_num, column=1, value=athlete.get("name"))
                    sheet.cell(row=row_num, column=2, value=athlete.get("age"))
                    sheet.cell(row=row_num, column=3, value=athlete.get("club"))
                    sheet.cell(row=row_num, column=4, value=athlete["stats"].get("matches"))
                    sheet.cell(row=row_num, column=5, value=athlete["stats"].get("wins"))
                    sheet.cell(row=row_num, column=6, value=athlete["stats"].get("losses"))
                    sheet.cell(row=row_num, column=7, value=athlete["stats"].get("draws"))

                try:
                    workbook.save(f"{self.file_name}.xlsx")
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Icon.Warning)  # Using warning icon for the message
                    msg.setWindowTitle("Process Completed")
                    msg.setText(f"File '{self.file_name}.xlsx' created successfully!")
                    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
                    msg.exec()
                except Exception:
                    QMessageBox.critical(QMessageBox(), "Unable to save the file", f"{Exception}")
                break
