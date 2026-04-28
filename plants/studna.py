import pygame
import config
from plants.zakladni_kytka import ZakladniKytka

class Studna(ZakladniKytka):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, config.KYTKA_2_DATA)

        # Načtení obrázků studny
        try:
            self.img_idle = pygame.image.load("gfx/well.png").convert_alpha()
            self.img_active = pygame.image.load("gfx/well_active.png").convert_alpha()
            self.img_idle = pygame.transform.smoothscale(self.img_idle, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
            self.img_active = pygame.transform.smoothscale(self.img_active, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
        except (pygame.error, FileNotFoundError):
            self.img_idle = None
            self.img_active = None
            
        self.image = self.img_idle

    def update(self, seznam_veganu, seznam_strel, hrac):
        nyni = pygame.time.get_ticks()
        
        # Animace aktivní studny (ukáže kapku 500ms po výrobě peněz)
        if self.img_idle and self.img_active:
            self.image = self.img_active if nyni - self.cas_posledni_animace < 500 else self.img_idle

        # Generování peněz
        if nyni - self.posledni_akce_cas > self.data["cooldown"]:
            # Přidáme peníze do peněženky v objektu Hrac
            hrac.pridej_penize(self.data["vydelek"])
            print(f"Studna vyrobila peníze! Celkem: ${hrac.penize}")
            
            self.posledni_akce_cas = nyni
            self.cas_posledni_animace = nyni