from vegans.zakladni_vegan import ZakladniVegan
import config

class TankVegan(ZakladniVegan):
    def __init__(self, waypoints):
        # Tady pro změnu využijeme variantu heavy_chew.png (poloměr 22 udělá obrázek 44x44)
        d = config.VEGAN_TANK_DATA
        super().__init__(waypoints, hp=d["hp"], rychlost=d["rychlost"], barva=d["barva"], polomer=d["polomer"], obrazek_cesta="gfx/heavy_chew.png")