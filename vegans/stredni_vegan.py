from vegans.zakladni_vegan import ZakladniVegan

class StredniVegan(ZakladniVegan):
    def __init__(self, waypoints):
        # Průměrný (stejný jako dřív)
        super().__init__(waypoints, hp=80, rychlost=2, barva=(255, 128, 0), polomer=15)