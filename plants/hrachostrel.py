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
            
            # --- LOGIKA ZAMĚŘOVÁNÍ ---
            nejblizsi_vegan = None
            min_vzdalenost = 1000000 # Nesmyslně velké číslo na začátek
            
            # Najdeme nejbližšího vegana v dostřelu
            for vegan in seznam_veganu:
                vzdalenost = (pygame.math.Vector2(self.x, self.y)).distance_to(vegan.pozice)
                
                if vzdalenost < self.data["dostřel"] and vzdalenost < min_vzdalenost:
                    nejblizsi_vegan = vegan
                    min_vzdalenost = vzdalenost
            
            # Pokud jsme našli cíl, vystřelíme!
            if nejblizsi_vegan:
                # Vytvoříme novou střelu a přidáme ji do seznamu v main.py
                nova_strela = Strela(self.x, self.y, nejblizsi_vegan)
                seznam_strel.append(nova_strela)
                
                # Resetujeme časovač
                self.posledni_akce_cas = nyni