import pygame
import config
import math
from plants.zakladni_kytka import ZakladniKytka
from projectiles.strela import Strela

class Hrachostrel(ZakladniKytka): # Dědí ze ZakladniKytka
    def __init__(self, grid_x, grid_y):
        # Zavoláme konstruktor rodičovské třídy s daty Hrachostřelu
        super().__init__(grid_x, grid_y, config.KYTKA_1_DATA)

        # Načtení a zmenšení obrázků
        try:
            self.img_idle = pygame.image.load("gfx/hrachstrel_IDLE.png").convert_alpha()
            self.img_shoot = pygame.image.load("gfx/hrachstrel_SHOOT.png").convert_alpha()
            self.img_idle = pygame.transform.smoothscale(self.img_idle, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
            self.img_shoot = pygame.transform.smoothscale(self.img_shoot, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
        except (pygame.error, FileNotFoundError):
            self.img_idle = None
            self.img_shoot = None
            
        self.image = self.img_idle
        self.uhel = 0 # Výchozí natočení (0 = nahoru)

    def update(self, seznam_veganu, seznam_strel, aktualni_penize):
        nyni = pygame.time.get_ticks()
        
        # --- LOGIKA ZAMĚŘOVÁNÍ (První v řadě) ---
        prvni_vegan = None
        max_pokrok = -1000000 # Hledáme co největší pokrok
        
        # Najdeme vegana, který je v dostřelu a došel na mapě nejdál
        for vegan in seznam_veganu:
            vzdalenost_od_kytky = (pygame.math.Vector2(self.x, self.y)).distance_to(vegan.pozice)
            
            if vzdalenost_od_kytky < self.data["dostřel"]:
                # Vypočítáme, jak daleko je vegan na mapě
                if vegan.aktualni_cil_index < len(vegan.waypoints):
                    cil_pozice = pygame.math.Vector2(vegan.waypoints[vegan.aktualni_cil_index])
                    vzdalenost_k_dalsimu_bodu = vegan.pozice.distance_to(cil_pozice)
                    pokrok = (vegan.aktualni_cil_index * 10000) - vzdalenost_k_dalsimu_bodu
                else:
                    pokrok = float('inf') # Vegan už je v cíli
                
                if pokrok > max_pokrok:
                    prvni_vegan = vegan
                    max_pokrok = pokrok
        
        # Pokud máme cíl, vypočítáme úhel, aby se kytka na něj natočila
        if prvni_vegan:
            dx = prvni_vegan.pozice.x - self.x
            dy = prvni_vegan.pozice.y - self.y
            # Pygame otáčí proti směru hodinových ručiček. Původní obrázek míří nahoru, proto -90.
            self.uhel = math.degrees(math.atan2(-dy, dx)) - 90

        # --- STŘELBA ---
        if nyni - self.posledni_akce_cas > self.data["cooldown"]:
            if prvni_vegan:
                # Vytvoříme novou střelu
                nova_strela = Strela(self.x, self.y, prvni_vegan)
                seznam_strel.append(nova_strela)
                self.posledni_akce_cas = nyni
                self.cas_posledni_animace = nyni
                
        # --- AKTUALIZACE GRAFIKY A ROTACE ---
        if self.img_idle and self.img_shoot:
            # Vybereme správný obrázek podle času od posledního výstřelu
            zakladni_obr = self.img_shoot if nyni - self.cas_posledni_animace < 200 else self.img_idle
            # Otočíme ho podle aktuálního úhlu a uložíme
            self.image = pygame.transform.rotate(zakladni_obr, self.uhel)