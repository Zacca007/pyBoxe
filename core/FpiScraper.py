from .FpiClient import FpiClient
from .FpiAthlete import FpiAthlete
from bs4 import BeautifulSoup


def search(client: FpiClient, min_match: int, max_match: int) -> list[FpiAthlete]:
    """
    Cerca atleti che soddisfano i criteri specificati.
    
    Args:
        client: Istanza di FpiClient configurata con i parametri di ricerca
        min_match: Numero minimo di match
        max_match: Numero massimo di match
        
    Returns:
        Lista di atleti che soddisfano i criteri
    """
    athletes: list[FpiAthlete] = []
    client.setup_payload_on_search()

    try:
        while True:
            page_html = client.athletes_html()
            parsed_athletes = parse_athletes(page_html)

            if not parsed_athletes:
                break

            for athlete in parsed_athletes:
                try:
                    stats_html = client.statistics_html(athlete.id)
                    wins, losses, draws = parse_statistics(stats_html)
                    athlete.set_stats(wins, losses, draws)
                    
                    if min_match <= athlete.total_matches() <= max_match:
                        athletes.append(athlete)
                except Exception as e:
                    print(f"Errore nel recupero statistiche per atleta {athlete.name}: {e}")
                    continue

            client.next_page()
    finally:
        client.reset_payload()
    
    return athletes


def parse_athletes(html: str) -> list[FpiAthlete]:
    """
    Parsa lista atleti dal markup HTML.
    
    Args:
        html: HTML della pagina con la lista degli atleti
        
    Returns:
        Lista di oggetti FpiAthlete
    """
    soup = BeautifulSoup(html, "html.parser")
    athletes: list[FpiAthlete] = []
    
    for athlete_div in soup.find_all("div", class_="atleta"):
        try:
            title = athlete_div.find(class_="card-title")
            button = athlete_div.find("button", class_="btn btn-dark btn-sm record")
            
            if not title or not button:
                continue
            
            name: str = title.text.strip()
            
            # Trova la società
            club_label = athlete_div.find("h6", string="Società")
            club: str = club_label.find_next("p").text.strip() if club_label else "N/A"
            
            # Trova l'età
            age_element = title.find_next_sibling(class_="card-title")
            age_text = age_element.text.split(":")[-1].strip() if age_element else "0"
            age: int = int(age_text)
            
            # ID atleta
            athlete_id: int = int(button["data-id"])
            
            athletes.append(FpiAthlete(name=name, club=club, age=age, id=athlete_id))
        except (ValueError, KeyError, AttributeError) as e:
            print(f"Errore nel parsing di un atleta: {e}")
            continue
    
    return athletes


def parse_statistics(html: str) -> tuple[int, int, int]:
    """
    Parsa statistiche dall'HTML.
    
    Args:
        html: HTML della pagina con le statistiche
        
    Returns:
        Tupla (wins, losses, draws)
    """
    soup = BeautifulSoup(html, "html.parser")
    stats = soup.find_all("td")
    
    if len(stats) < 4:
        return (0, 0, 0)
    
    try:
        wins = int(stats[1].text.strip())
        losses = int(stats[2].text.strip())
        draws = int(stats[3].text.strip())
        return (wins, losses, draws)
    except (ValueError, IndexError):
        return (0, 0, 0)