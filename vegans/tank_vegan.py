from vegans.zakladni_vegan import ZakladniVegan

class TankVegan(ZakladniVegan):
    def __init__(self, waypoints):
        # Pomalý, hodně HP, obrovský
        super().__init__(waypoints, hp=350, rychlost=1, barva=(139, 0, 0), polomer=22)