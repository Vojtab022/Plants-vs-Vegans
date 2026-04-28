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
        self.cas_posledni_animace = -10000 # Časovač čistě pro animace (aby nehrály hned po položení)

        self.image = None # Bude obsahovat načtený obrázek

    # Tuhle metodu bude mít každá kytka jinou
    def update(self, seznam_veganu, seznam_strel, hrac):
        pass # Uděláme v podtřídách
        
    def draw(self, screen):
        if self.image:
            # Pokud má kytka obrázek, vykreslíme ho na střed
            rect = self.image.get_rect(center=(self.x, self.y))
            screen.blit(self.image, rect)
        else:
            # Základní čtverec jako záložní řešení
            velikost = 20
            pygame.draw.rect(screen, self.data["barva"], (self.x - velikost, self.y - velikost, velikost*2, velikost*2))