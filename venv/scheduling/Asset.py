class Asset:
    def __init__(self, name: str="", owner: str="", crew_num: int=0, cargo: int=0) -> None:
        self.name = name
        self.owner = owner
        self.crew_num = crew_num
        self.cargo = cargo
