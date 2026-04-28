import pygame
import config
import math
from plants.zakladni_kytka import ZakladniKytka
from projectiles.strela import Strela

class Kaktus(ZakladniKytka):
    def __init__(self, grid_x, grid_y):
        super().__init__(grid_x, grid_y, config.KYTKA_3_DATA)

        try:
            self.img_idle = pygame.image.load("gfx/kaktus_IDLE.png").convert_alpha()
            self.img_shoot = pygame.image.load("gfx/kaktus_SHOOT.png").convert_alpha()
            self.img_idle = pygame.transform.smoothscale(self.img_idle, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
            self.img_shoot = pygame.transform.smoothscale(self.img_shoot, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
        except (pygame.error, FileNotFoundError):
            self.img_idle = None
            self.img_shoot = None
            
        self.image = self.img_idle
        self.uhel = 0

    def update(self, seznam_veganu, seznam_strel, hrac):
        nyni = pygame.time.get_ticks()
        
        prvni_vegan = None
        max_pokrok = -1000000
        
        for vegan in seznam_veganu:
            vzdalenost_od_kytky = (pygame.math.Vector2(self.x, self.y)).distance_to(vegan.pozice)
            
            if vzdalenost_od_kytky < self.data["dostřel"]:
                if vegan.aktualni_cil_index < len(vegan.waypoints):
                    cil_pozice = pygame.math.Vector2(vegan.waypoints[vegan.aktualni_cil_index])
                    vzdalenost_k_dalsimu_bodu = vegan.pozice.distance_to(cil_pozice)
                    pokrok = (vegan.aktualni_cil_index * 10000) - vzdalenost_k_dalsimu_bodu
                else:
                    pokrok = float('inf')
                
                if pokrok > max_pokrok:
                    prvni_vegan = vegan
                    max_pokrok = pokrok
        
        if prvni_vegan:
            dx = prvni_vegan.pozice.x - self.x
            dy = prvni_vegan.pozice.y - self.y
            self.uhel = math.degrees(math.atan2(-dy, dx)) - 90

        if nyni - self.posledni_akce_cas > self.data["cooldown"]:
            if prvni_vegan:
                # Kaktus střílí s vyšším poškozením (předáme ho střele)
                nova_strela = Strela(self.x, self.y, prvni_vegan, self.data.get("poskozeni", 50))
                seznam_strel.append(nova_strela)
                self.posledni_akce_cas = nyni
                self.cas_posledni_animace = nyni
                
        if self.img_idle and self.img_shoot:
            zakladni_obr = self.img_shoot if nyni - self.cas_posledni_animace < 200 else self.img_idle
            self.image = pygame.transform.rotate(zakladni_obr, self.uhel)