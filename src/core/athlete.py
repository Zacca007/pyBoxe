class FpiAthlete:
    def __init__(self, name: str, club: str, age: int, id: int):
        self.name: str = name
        self.club: str = club
        self.age: int = age
        self.id: int = id

        self.wins: int = 0
        self.losses: int = 0
        self.draws: int = 0

    def total_matches(self) -> int:
        return self.wins + self.losses + self.draws

    def set_stats(self, stats: tuple[int, int, int]):
        self.wins = stats[0]
        self.losses = stats[1]
        self.draws = stats[2]