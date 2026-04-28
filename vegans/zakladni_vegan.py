import pygame
import config

class ZakladniVegan:
    def __init__(self, waypoints, hp=100, rychlost=2, barva=(255, 0, 0), polomer=15):
        self.waypoints = waypoints
        self.aktualni_cil_index = 1
        self.pozice = pygame.math.Vector2(waypoints[0])
        
        self.rychlost = rychlost
        self.hp = hp
        self.max_hp = hp # Uložíme si i maximum pro výpočet procent
        
        self.barva = barva
        self.polomer = polomer

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

    def vezmi_poskozeni(self, dmg):
        # Vegan si sám zpracuje odečtení životů
        self.hp -= dmg

    def draw(self, screen):
        # Vykreslíme vegana jako kruh (aby se lišil od hranatých políček)
        # int() používáme, protože pixely nemůžou být desetinná čísla
        pygame.draw.circle(screen, self.barva, (int(self.pozice.x), int(self.pozice.y)), self.polomer)
        
        # --- VYKRESLENÍ HP BARU ---
        sirka_baru = max(30, self.polomer * 2) # Udržíme minimální šířku 30, ale u velkého bosse se bar roztáhne
        vyska_baru = 5
        
        # Ochrana proti záporným hodnotám při úmrtí
        procento_hp = max(0, self.hp / self.max_hp)
        aktualni_sirka_baru = int(sirka_baru * procento_hp)
        
        bar_x = int(self.pozice.x) - (sirka_baru // 2)
        bar_y = int(self.pozice.y) - self.polomer - 10 # Umístíme bar těsně nad vegana
        
        # Červené pozadí (ztracené zdraví)
        pygame.draw.rect(screen, (200, 0, 0), (bar_x, bar_y, sirka_baru, vyska_baru))
        # Zelené popředí (aktuální zdraví)
        if aktualni_sirka_baru > 0:
            pygame.draw.rect(screen, (0, 200, 0), (bar_x, bar_y, aktualni_sirka_baru, vyska_baru))
        # Černý okraj
        pygame.draw.rect(screen, (0, 0, 0), (bar_x, bar_y, sirka_baru, vyska_baru), 1)