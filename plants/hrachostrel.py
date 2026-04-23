import pygame
import config
import math
from plants.zakladni_kytka import ZakladniKytka
from projectiles.strela import Strela

class Hrachostrel(ZakladniKytka): # Dědí ze ZakladniKytka
    def __init__(self, grid_x, grid_y):
        # Zavoláme konstruktor rodičovské třídy s daty Hrachostřelu
        super().__init__(grid_x, grid_y, config.KYTKA_1_DATA)

    def update(self, seznam_veganu, seznam_strel, aktualni_penize):
        nyni = pygame.time.get_ticks()
        
        # Kontrola, jestli už můžeme střílet (cooldown)
        if nyni - self.posledni_akce_cas > self.data["cooldown"]:
            
            # --- LOGIKA ZAMĚŘOVÁNÍ (První v řadě) ---
            prvni_vegan = None
            max_pokrok = -1000000 # Hledáme co největší pokrok
            
            # Najdeme vegana, který je v dostřelu a došel na mapě nejdál
            for vegan in seznam_veganu:
                vzdalenost_od_kytky = (pygame.math.Vector2(self.x, self.y)).distance_to(vegan.pozice)
                
                if vzdalenost_od_kytky < self.data["dostřel"]:
                    # Vypočítáme, jak daleko je vegan na mapě:
                    # 1. Čím vyšší index cílového bodu, tím dál vegan je (násobíme 10000, aby to mělo vždy největší váhu)
                    # 2. Odečteme vzdálenost ke konkrétnímu bodu (čím menší číslo, tím blíž je k cíli)
                    if vegan.aktualni_cil_index < len(vegan.waypoints):
                        cil_pozice = pygame.math.Vector2(vegan.waypoints[vegan.aktualni_cil_index])
                        vzdalenost_k_dalsimu_bodu = vegan.pozice.distance_to(cil_pozice)
                        pokrok = (vegan.aktualni_cil_index * 10000) - vzdalenost_k_dalsimu_bodu
                    else:
                        pokrok = float('inf') # Vegan už je v cíli (má absolutní prioritu)
                    
                    if pokrok > max_pokrok:
                        prvni_vegan = vegan
                        max_pokrok = pokrok
            
            # Pokud jsme našli cíl, vystřelíme!
            if prvni_vegan:
                # Vytvoříme novou střelu a přidáme ji do seznamu v main.py
                nova_strela = Strela(self.x, self.y, prvni_vegan)
                seznam_strel.append(nova_strela)
                
                # Resetujeme časovač
                self.posledni_akce_cas = nyni