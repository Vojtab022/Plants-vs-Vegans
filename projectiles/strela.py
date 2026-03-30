import pygame
import config

class Strela:
    def __init__(self, start_x, start_y, cilový_vegan):
        self.pozice = pygame.math.Vector2(start_x, start_y)
        self.cil = cilový_vegan # Strela si pamatuje, na kterého vegana byla vystřelena
        self.data = config.STRELA_HRY_DATA
        
        self.je_ziva = True # Pro snadné mazání střel, které trefily
        
        # Vypočítáme konstantní směr k cíli v momentě výstřelu
        # (Aby střela "nezahejbala", když se vegan pohne)
        smer_k_cili = (self.cil.pozice - self.pozice).normalize()
        self.vektor_pohybu = smer_k_cili * self.data["rychlost"]

    def update(self):
        # Střela letí rovně podle vektoru pohybu
        self.pozice += self.vektor_pohybu
        
        # Kontrola, jestli střela nevyletěla z obrazovky
        if (self.pozice.x < 0 or self.pozice.x > config.SIRKA_OKNA or
            self.pozice.y < 0 or self.pozice.y > config.VYSKA_MAPY):
            self.je_ziva = False

    def draw(self, screen):
        # Kreslíme střelu jako kuličku
        pygame.draw.circle(screen, self.data["barva"], (int(self.pozice.x), int(self.pozice.y)), self.data["velikost"])