import pygame
import config

class Strela:
    def __init__(self, start_x, start_y, cilový_vegan, poskozeni=15):
        # Pozice střely
        self.pozice = pygame.math.Vector2(start_x, start_y)
        
        # !!! DŮLEŽITÉ: Uložíme si REFERENCI na konkrétního vegana
        # Střela ho bude sledovat celou dobu
        self.cil = cilový_vegan
        
        self.data = config.STRELA_HRY_DATA
        self.rychlost = self.data["rychlost"] # Načteme rychlost z configu
        self.poskozeni = poskozeni
        
        self.je_ziva = True # Pro mazání

        try:
            self.image = pygame.image.load("gfx/hracho_bullet.png").convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (160, 160)) # Velikost náboje
        except (pygame.error, FileNotFoundError):
            self.image = None

    def update(self):
        # --- NOVÉ: ŘÍZENÝ POHYB (HOMING) ---
        
        # 1. Zkontrolujeme, zda cíl stále existuje a je naživu (HP > 0)
        # (Používáme self.cil.hp, protože jsme ve veganovi přejmenovali zdravi na hp)
        if self.cil and self.cil.hp > 0:
            
            # 2. Vypočítáme vektor k *aktuální* pozici cíle (každý frame!)
            smer_k_cili = (self.cil.pozice - self.pozice)
            vzdalenost = smer_k_cili.length()
            
            # 3. Pokud jsme už skoro u cíle, prostě se na něj "teleportujeme",
            # aby kolizní systém v main.py garantovaně detekoval zásah.
            if vzdalenost < self.rychlost:
                self.pozice = self.cil.pozice
            else:
                # 4. Jinak normalizujeme směr a posuneme se (bezpečnostní pojistka)
                if vzdalenost > 0:
                    smer_normalizovany = smer_k_cili.normalize()
                    self.pozice += smer_normalizovany * self.rychlost
                
        else:
            # Co když cíl umřel dřív, než střela doletěla?
            # V Tower Defense je běžné, že střela prostě letí dál rovně
            # nebo zmizí. Pro jednoduchost ji necháme zmizet.
            self.je_ziva = False

        # --- KONTROLA HRANIC (ponecháme původní) ---
        if (self.pozice.x < 0 or self.pozice.x > config.SIRKA_OKNA or
            self.pozice.y < 0 or self.pozice.y > config.VYSKA_MAPY):
            self.je_ziva = False

    def draw(self, screen):
        if self.image:
            # Vykreslení textury náboje
            rect = self.image.get_rect(center=(int(self.pozice.x), int(self.pozice.y)))
            screen.blit(self.image, rect)
        else:
            pygame.draw.circle(screen, self.data["barva"], (int(self.pozice.x), int(self.pozice.y)), self.data["velikost"])