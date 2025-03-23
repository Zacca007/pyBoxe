class Athlete:
    _name = str()
    _age = int()
    _club = str()

    def __init__(self, wins: int, losses: int, draws: int):
        self._wins = wins
        self._losses = losses
        self._draws = draws
        self._fix_total_matches()

    # Getters
    def get_name(self) -> str:
        return self._name

    def get_age(self) -> int:
        return self._age

    def get_club(self) -> str:
        return self._club

    def get_matches(self) -> int:
        return self._matches

    def get_wins(self) -> int:
        return self._wins

    def get_losses(self) -> int:
        return self._losses

    def get_draws(self) -> int:
        return self._draws

    # Setters
    def set_name(self, name: str):
        self._name = name

    def set_age(self, age: int):
        self._age = age

    def set_club(self, club: str):
        self._club = club

    #logic
    def _fix_total_matches(self):
        self._matches = self._wins + self._draws + self._losses