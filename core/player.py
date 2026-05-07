class Hrac:
    def __init__(self, pocatecni_penize=200):
        self.penize = pocatecni_penize

    def pridej_penize(self, castka):
        self.penize += castka

    def uber_penize(self, castka):
        if self.ma_dostatek(castka):
            self.penize -= castka

    def ma_dostatek(self, castka):
        return self.penize >= castka