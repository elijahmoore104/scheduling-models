from Asset import Asset

class Schedule:
    def __init__(self, name: str, owner: str, crew_num: int) -> None:
        self.name = name
        self.owner = owner
        self.crew_num = crew_num