from vegans.zakladni_vegan import ZakladniVegan

class BossVegan(ZakladniVegan):
    def __init__(self, waypoints):
        # Extrémně pomalý, gigantické HP, fialová barva a největší poloměr
        super().__init__(waypoints, hp=2000, rychlost=0.8, barva=(128, 0, 128), polomer=35)