import pygame
import random
import config
from vegans.rychly_vegan import RychlyVegan
from vegans.stredni_vegan import StredniVegan
from vegans.tank_vegan import TankVegan
from vegans.boss_vegan import BossVegan

class WaveManager:
    def __init__(self):
        self.cas_posledniho_spawnu = pygame.time.get_ticks()
        self.celkem_vygenerovano = 0
        self.spawn_interval = config.VLNA_SPAWN_INTERVAL
        self.max_veganu_ve_vlne = config.VLNA_START_VEGANU
        self.current_wave = 1
        self.wave_started = False

    def start_wave(self, nyni):
        if not self.wave_started:
            self.wave_started = True
            self.cas_posledniho_spawnu = nyni

    def posun_cas(self, posun):
        self.cas_posledniho_spawnu += posun

    def update(self, seznam_veganu, hrac, game_speed=1):
        # Kontrola dokončení vlny
        if self.wave_started and self.celkem_vygenerovano == self.max_veganu_ve_vlne and len(seznam_veganu) == 0:
            self.current_wave += 1
            self.max_veganu_ve_vlne += config.VLNA_PRIRUSTEK_VEGANU
            self.spawn_interval = max(config.VLNA_MIN_SPAWN_INTERVAL, self.spawn_interval - config.VLNA_ZRYCHLENI_SPAWNU)
            self.celkem_vygenerovano = 0
            self.wave_started = False
            hrac.pridej_penize(config.ODMENA_ZA_VLNU) # Odměna za přežití vlny
            return

        if not self.wave_started:
            return

        nyni = pygame.time.get_ticks()
        if nyni - self.cas_posledniho_spawnu > (self.spawn_interval / game_speed) and self.celkem_vygenerovano < self.max_veganu_ve_vlne:
            # Seznam dostupných nepřátel se postupně rozšiřuje podle aktuální vlny
            dostupni_vegani = [StredniVegan]
            
            if self.current_wave >= 2:
                dostupni_vegani.append(RychlyVegan)
            if self.current_wave >= 3:
                dostupni_vegani.append(TankVegan)
            if self.current_wave >= 10:
                # Boss se odemkne v 10. vlně, přidáme i středního pro naředění pravděpodobnosti, aby nebyl v každém spawnu
                dostupni_vegani.extend([StredniVegan, BossVegan]) 

            TypVegana = random.choice(dostupni_vegani)
            
            seznam_veganu.append(TypVegana(config.AKTUALNI_WAYPOINTY))
            self.cas_posledniho_spawnu = nyni
            self.celkem_vygenerovano += 1