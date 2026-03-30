import pygame
import config

class ZakladniVegan:
    def __init__(self, waypoints):
        self.waypoints = waypoints
        self.aktualni_cil_index = 1
        self.pozice = pygame.math.Vector2(waypoints[0])
        self.rychlost = 2
        
        self.hp = 100  # <--- TADY ZMĚŇ self.zdravi NA self.hp
        
        self.barva = (255, 0, 0)

    def move(self):
        # Zkontrolujeme, jestli už nejsme v cíli
        if self.aktualni_cil_index < len(self.waypoints):
            # Zjistíme, kam chceme jít
            cil = pygame.math.Vector2(self.waypoints[self.aktualni_cil_index])
            
            # Vypočítáme směr k cíli
            smer = cil - self.pozice
            vzdalenost = smer.length()
            
            # Pokud jsme už skoro u cílového bodu, přepneme na další bod
            if vzdalenost < self.rychlost:
                self.aktualni_cil_index += 1
            else:
                # Normalizujeme směr (aby nešel rychleji šikmo) a posuneme ho
                smer = smer.normalize()
                self.pozice += smer * self.rychlost

    def draw(self, screen):
        # Vykreslíme vegana jako kruh (aby se lišil od hranatých políček)
        # int() používáme, protože pixely nemůžou být desetinná čísla
        pygame.draw.circle(screen, self.barva, (int(self.pozice.x), int(self.pozice.y)), 15)