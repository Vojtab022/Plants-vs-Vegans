import pygame
import random
import config

class HerniMapa:
    def __init__(self):
        self.nacti_textury()
        self.vytvor_grid()
        self.vytvor_mrizku_a_ukazatele()

    def nacti_textury(self):
        self.path_textures = {}
        path_files = {
            "horizon": "gfx/Horizon.png", "straight": "gfx/Straight.png",
            "top_left": "gfx/top-left.png", "top_right": "gfx/top-right.png",
            "bot_left": "gfx/bot-left.png", "bot_right": "gfx/Bot-right.png"
        }
        for key, filepath in path_files.items():
            try:
                img = pygame.image.load(filepath).convert_alpha()
                self.path_textures[key] = pygame.transform.smoothscale(img, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
            except (pygame.error, FileNotFoundError):
                self.path_textures[key] = None
            
        self.grass_textures = []
        try:
            grass_base = pygame.image.load("gfx/grass.png").convert_alpha()
            grass_base = pygame.transform.smoothscale(grass_base, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
            self.grass_textures.extend([
                grass_base,
                pygame.transform.rotate(grass_base, 90),
                pygame.transform.rotate(grass_base, 180),
                pygame.transform.rotate(grass_base, 270)
            ])
        except (pygame.error, FileNotFoundError):
            pass

    def vytvor_grid(self):
        self.grid_textur = []
        for radek_index in range(config.RADKU):
            radek_textur = []
            for sloupec_index in range(config.SLOUPCU):
                policko = config.AKTUALNI_MAPA[radek_index][sloupec_index]
                if policko == 1:
                    up = radek_index > 0 and config.AKTUALNI_MAPA[radek_index-1][sloupec_index] == 1
                    down = radek_index < config.RADKU - 1 and config.AKTUALNI_MAPA[radek_index+1][sloupec_index] == 1
                    left = sloupec_index > 0 and config.AKTUALNI_MAPA[radek_index][sloupec_index-1] == 1
                    right = sloupec_index < config.SLOUPCU - 1 and config.AKTUALNI_MAPA[radek_index][sloupec_index+1] == 1

                    if up and not (down or left or right): down = True
                    elif down and not (up or left or right): up = True
                    elif left and not (right or up or down): right = True
                    elif right and not (left or up or down): left = True

                    img = None
                    if left and right and not up and not down: img = self.path_textures.get("horizon")
                    elif up and down and not left and not right: img = self.path_textures.get("straight")
                    elif right and down and not up and not left: img = self.path_textures.get("top_left")
                    elif left and down and not up and not right: img = self.path_textures.get("top_right")
                    elif right and up and not down and not left: img = self.path_textures.get("bot_left")
                    elif left and up and not down and not right: img = self.path_textures.get("bot_right")
                    else: img = self.path_textures.get("horizon") 
                    
                    radek_textur.append(img)
                else:
                    if self.grass_textures:
                        radek_textur.append(random.choice(self.grass_textures))
                    else:
                        radek_textur.append(None)
            self.grid_textur.append(radek_textur)

    def vytvor_mrizku_a_ukazatele(self):
        self.grid_surface = pygame.Surface((config.SIRKA_OKNA, config.VYSKA_MAPY), pygame.SRCALPHA)
        for radek_index in range(config.RADKU):
            for sloupec_index in range(config.SLOUPCU):
                x = sloupec_index * config.VELIKOST_POLICKA
                y = radek_index * config.VELIKOST_POLICKA
                pygame.draw.rect(self.grid_surface, config.BARVA_MRIZKY, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA), 1)
                
        if len(config.AKTUALNI_WAYPOINTY) >= 2:
            p1 = pygame.math.Vector2(config.AKTUALNI_WAYPOINTY[0])
            p2 = pygame.math.Vector2(config.AKTUALNI_WAYPOINTY[1])
            if p1.distance_to(p2) > 0:
                smer = (p2 - p1).normalize()
                stred = p1
                konec_tela = stred + smer * 5
                zadek_tela = stred - smer * 15
                hrot = stred + smer * 18
                kolmice = pygame.math.Vector2(-smer.y, smer.x)
                
                pygame.draw.line(self.grid_surface, (255, 50, 50, 180), zadek_tela, konec_tela, 6)
                pygame.draw.polygon(self.grid_surface, (255, 50, 50, 180), [
                    hrot, 
                    konec_tela + kolmice * 10, 
                    konec_tela - kolmice * 10
                ])

    def draw(self, screen, wave_started):
        for radek_index in range(config.RADKU):
            for sloupec_index in range(config.SLOUPCU):
                cislo_policka = config.AKTUALNI_MAPA[radek_index][sloupec_index]
                x = sloupec_index * config.VELIKOST_POLICKA
                y = radek_index * config.VELIKOST_POLICKA
                
                if self.grid_textur[radek_index][sloupec_index]:
                    screen.blit(self.grid_textur[radek_index][sloupec_index], (x, y))
                else:
                    barva = config.BARVA_TRAVY if cislo_policka == 0 else config.BARVA_CESTY
                    pygame.draw.rect(screen, barva, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
                
        if not wave_started:
            screen.blit(self.grid_surface, (0, 0))