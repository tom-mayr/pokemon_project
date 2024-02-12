from pokedex import pokedex # importing a dictionary of all info for every pokemon

class Pokemon:
    def __init__(self, name: str, max_hp: int = 100):
        self.name = name
        self.type = pokedex[name]['type']
        self.moveset = pokedex[name]['moveset']
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.status = None
        self.accuracy = 1
    
    def get_info(self):
        return (self.name, self.type, self.moveset, self.max_hp)

    def get_state(self):
        return (self.current_hp, self.status, self.accuracy)
    
    def set_attributes(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self, attr, value)