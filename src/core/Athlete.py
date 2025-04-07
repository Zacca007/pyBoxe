class Athlete:
    name = str()
    club = str()
    age = int()
    _wins = int()
    _losses = int()
    _draws = int()

    def __init__(self, wins: int, losses: int, draws: int):
        self._wins = wins
        self._losses = losses
        self._draws = draws

    @property
    def wins(self) -> int:
        return self._wins

    @property
    def losses(self) -> int:
        return self._losses

    @property
    def draws(self) -> int:
        return self._draws

    def total_matches(self) -> int:
        return self._wins + self._losses + self._draws