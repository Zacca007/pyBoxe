class FpiAthlete:
    """Rappresenta un atleta FPI con le sue informazioni e statistiche."""
    
    def __init__(self, name: str, club: str, age: int, id: int):
        """
        Inizializza un atleta FPI.
        
        Args:
            name: Nome dell'atleta
            club: Società di appartenenza
            age: Età dell'atleta
            id: ID univoco dell'atleta
        """
        self.name: str = name
        self.club: str = club
        self.age: int = age
        self.id: int = id

        self.wins: int = 0
        self.losses: int = 0
        self.draws: int = 0

    def total_matches(self) -> int:
        """
        Calcola il numero totale di match.
        
        Returns:
            Somma di vittorie, sconfitte e pareggi
        """
        return self.wins + self.losses + self.draws

    def set_stats(self, wins: int, losses: int, draws: int) -> None:
        """
        Imposta le statistiche dell'atleta.
        
        Args:
            wins: Numero di vittorie
            losses: Numero di sconfitte
            draws: Numero di pareggi
        """
        self.wins = wins
        self.losses = losses
        self.draws = draws

    def __repr__(self) -> str:
        """Rappresentazione stringa dell'atleta."""
        return f"FpiAthlete(name='{self.name}', age={self.age}, matches={self.total_matches()})"