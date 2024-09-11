class Bird:
    def __init__(self, species, favorite_rhythm):
        self.species = species
        self.favorite_rhythm = favorite_rhythm

    def is_attracted(self, rhythm):
        return rhythm == self.favorite_rhythm
