import pygame
import config
from plants.zakladni_kytka import ZakladniKytka

class Slunecnice(ZakladniKytka):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, config.KYTKA_2_DATA)

    def update(self, seznam_veganu, seznam_strel, aktualni_penize):
        nyni = pygame.time.get_ticks()
        
        # Generování peněz
        if nyni - self.posledni_akce_cas > self.data["cooldown"]:
            # Přidáme peníze do peněženky v main.py (musíme vrátit novou hodnotu)
            aktualni_penize += self.data["vydelek"]
            print(f"Slunečnice vyrobila peníze! Celkem: ${aktualni_penize}")
            
            self.posledni_akce_cas = nyni
            return aktualni_penize # Vracíme aktualizovaný stav peněz

        return aktualni_penize # Vracíme beze změny