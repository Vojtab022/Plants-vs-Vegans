import pygame
import config

# --- ZÁKLADNÍ TŘÍDA (Abstraktní - nelze z ní přímo vytvořit objekt) ---
class ZakladniKytka:
    def __init__(self, grid_x, grid_y, plant_data):
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.data = plant_data
        
        # Střed políčka v pixelech
        self.x = (grid_x * config.VELIKOST_POLICKA) + (config.VELIKOST_POLICKA // 2)
        self.y = (grid_y * config.VELIKOST_POLICKA) + (config.VELIKOST_POLICKA // 2)
        
        # Časovač (použijeme pygame.time.get_ticks())
        self.posledni_akce_cas = pygame.time.get_ticks()

    # Tuhle metodu bude mít každá kytka jinou
    def update(self, seznam_veganu, seznam_strel, aktualni_penize):
        pass # Uděláme v podtřídách
        
    def draw(self, screen):
        # Základní čtverec placeholder
        velikost = 20
        pygame.draw.rect(screen, self.data["barva"], (self.x - velikost, self.y - velikost, velikost*2, velikost*2))