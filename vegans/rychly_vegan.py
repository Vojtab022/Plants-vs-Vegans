from vegans.zakladni_vegan import ZakladniVegan
import config

class RychlyVegan(ZakladniVegan):
    def __init__(self, waypoints):
        d = config.VEGAN_RYCHLY_DATA
        super().__init__(waypoints, hp=d["hp"], rychlost=d["rychlost"], barva=d["barva"], polomer=d["polomer"], obrazek_cesta="gfx/light.png")