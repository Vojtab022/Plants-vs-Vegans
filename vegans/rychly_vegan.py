from vegans.zakladni_vegan import ZakladniVegan

class RychlyVegan(ZakladniVegan):
    def __init__(self, waypoints):
        # Rychlý, málo HP, menší poloměr
        super().__init__(waypoints, hp=40, rychlost=4, barva=(255, 255, 0), polomer=12)