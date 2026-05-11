import pygame
import sys
import os
import random
import config
# --- OPRAVA PRO PYINSTALLER (.exe) ---
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)
from ui.menu import Menu
from core.mapa import HerniMapa
from core.player import Hrac
from core.wave_manager import WaveManager
from plants.hrachostrel import Hrachostrel
from plants.kaktus import Kaktus
from plants.studna import Studna
from ui.ui import Button

class PlantsVsVegansGame:
    """
    Tato třída představuje samotnou hru (jeden level). 
    Uchovává si všechny informace o rozehrané hře (peníze, postavené kytky, nepřátele) a řídí její chod.
    """
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_ui = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_plants = pygame.font.SysFont("Arial", 16, bold=True) # Menší font pro delší názvy
        self.font_pause = pygame.font.SysFont("Arial", 60, bold=True)
        
        # Herní stav 
        self.running = True
        self.paused = False
        self.game_over = False
        self.action_after_quit = "MENU"
        self.pause_start_cas = 0
        self.game_speed = 1
        self.hrac = Hrac(config.POCATECNI_PENIZE)
        self.wave_manager = WaveManager()
        self.vybrany_typ_kytky_data = None
        self.survived_time_ms = 0
        
        # Výběr a prodej existující kytky
        self.vybrana_polozena_kytka = None
        self.sell_btn = Button(0, 0, 140, 35, "Prodat", self.font_ui, (200, 0, 0), (255, 50, 50))

        # Seznamy objektů 
        self.seznam_veganu = []
        self.seznam_kytek = []
        self.seznam_strel = []
        self.seznam_obsazenych_policek = []
        
        # UI Tlačítka pro pauzu
        btn_w, btn_h = 200, 60
        stred_x = config.SIRKA_OKNA // 2 - btn_w // 2
        barva_zaklad = (0, 150, 0)
        barva_hover = (0, 200, 0)
        self.continue_btn = Button(stred_x, 200, btn_w, btn_h, "Continue", self.font_ui, barva_zaklad, barva_hover)
        self.settings_btn = Button(stred_x, 280, btn_w, btn_h, "Settings", self.font_ui, barva_zaklad, barva_hover)
        self.main_menu_btn = Button(stred_x, 360, btn_w, btn_h, "Main Menu", self.font_ui, barva_zaklad, barva_hover)

        # Přípravná fáze
        self.start_wave_btn = Button(config.SIRKA_OKNA - 320, config.VYSKA_MAPY + 20, 160, 60, "Start Wave", self.font_ui, (200, 0, 0), (255, 50, 50))
        self.speed_btn = Button(config.SIRKA_OKNA - 320, config.VYSKA_MAPY + 20, 160, 60, "Rychlost: 1x", self.font_ui, (0, 0, 200), (50, 50, 255))

        # Tlačítka pro výběr kytek v UI
        self.plant_buttons = []
        for i, data in enumerate(config.SEZNAM_DOSTUPNYCH_KYTEK):
            bx = 10 + (i * 185) # Větší rozestup, aby se vešla širší tlačítka
            by = config.VYSKA_MAPY + 10
            barva_zaklad = data["barva"]
            # Vypočítáme trochu světlejší barvu pro hover efekt
            barva_hover = (min(255, barva_zaklad[0]+40), min(255, barva_zaklad[1]+40), min(255, barva_zaklad[2]+40))
            
            ikona = None
            if "ikona" in data:
                try:
                    ikona_img = pygame.image.load(data["ikona"]).convert_alpha()
                    ikona = pygame.transform.smoothscale(ikona_img, (40, 40))
                except (pygame.error, FileNotFoundError):
                    ikona = None
                    
            btn = Button(bx, by, 175, 80, f"{data['nazev']}\n${data['cena']}", self.font_plants, barva_zaklad, barva_hover, icon=ikona)
            self.plant_buttons.append({"btn": btn, "data": data})

        # Tlačítka pro Game Over
        self.restart_btn = Button(stred_x, 260, btn_w, btn_h, "Restart", self.font_ui, (200, 0, 0), (255, 50, 50))
        self.go_main_menu_btn = Button(stred_x, 340, btn_w, btn_h, "Main Menu", self.font_ui, (200, 0, 0), (255, 50, 50))

        # OOP: Logika mapy je nyní kompletně oddělena v samostatné třídě
        self.mapa = HerniMapa()

    def handle_events(self):
        """Zpracovává veškeré vstupy od uživatele v každém snímku (framu)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(pygame.mouse.get_pos())

    def toggle_pause(self):
        """Zastaví nebo znovu spustí hru. Při spuštění dopočítá ztracený čas, aby se kytky nezbláznily."""
        if not self.paused:
            self.paused = True
            self.pause_start_cas = pygame.time.get_ticks()
        else:
            self.paused = False
            posun = pygame.time.get_ticks() - self.pause_start_cas
            self.wave_manager.posun_cas(posun)
            for kytka in self.seznam_kytek:
                kytka.posledni_akce_cas += posun

    def handle_click(self, pos):
        """Základní 'mozek' interakce. Řeší, na co přesně hráč kliknul (podle toho, zda je Game Over, Pauza nebo se hraje)."""
        mouse_x, mouse_y = pos
        if self.game_over:
            if self.restart_btn.is_clicked(pos):
                self.action_after_quit = "RESTART"
                self.running = False
            elif self.go_main_menu_btn.is_clicked(pos):
                self.action_after_quit = "MENU"
                self.running = False
        elif self.paused:
            if self.continue_btn.is_clicked(pos):
                self.toggle_pause()
            elif self.main_menu_btn.is_clicked(pos):
                self.running = False
            elif self.settings_btn.is_clicked(pos):
                m = Menu(in_game=True)
                m.settings_menu()
        else:
            # Kontrola kliknutí na tlačítko Start Wave (pokud vlna ještě nezačala)
            nyni = pygame.time.get_ticks()
            if not self.wave_manager.wave_started and self.start_wave_btn.is_clicked(pos):
                self.wave_manager.start_wave(nyni)
                
                # Resetujeme časovače u již položených kytek, aby nezačaly střílet/vydělávat s předstihem
                for kytka in self.seznam_kytek:
                    kytka.posledni_akce_cas = nyni
                return
            
            # Kontrola kliknutí na tlačítko pro zrychlení hry (pouze během vlny)
            if self.wave_manager.wave_started and self.speed_btn.is_clicked(pos):
                self.game_speed = 2 if self.game_speed == 1 else 1
                self.speed_btn.text = f"Rychlost: {self.game_speed}x"
                return

            # Kontrola kliknutí na plovoucí tlačítko Prodat
            if self.vybrana_polozena_kytka and self.sell_btn.is_clicked(pos):
                self.sell_plant()
                return

            # Pokud hráč klikl do horní části okna (herní plocha, nikoliv UI dole)
            if mouse_y < config.VYSKA_MAPY:
                grid_x = mouse_x // config.VELIKOST_POLICKA
                grid_y = mouse_y // config.VELIKOST_POLICKA
                
                # Zkusíme najít kytku na políčku, na které jsme klikli
                clicked_kytka = next((k for k in self.seznam_kytek if k.grid_x == grid_x and k.grid_y == grid_y), None)
                
                if clicked_kytka:
                    self.vybrana_polozena_kytka = clicked_kytka
                    self.vybrany_typ_kytky_data = None # Zrušíme případný výběr kytky z UI
                    
                    # Nastavení pozice tlačítka Prodat těsně nad kytkou
                    self.sell_btn.rect.x = clicked_kytka.x - self.sell_btn.rect.width // 2
                    self.sell_btn.rect.y = clicked_kytka.y - config.VELIKOST_POLICKA - 15
                    if self.sell_btn.rect.y < 0: # Pojistka, aby tlačítko nevyjelo mimo obrazovku
                        self.sell_btn.rect.y = clicked_kytka.y + config.VELIKOST_POLICKA // 2 + 10
                        
                    cena = clicked_kytka.data["cena"] // 2
                    self.sell_btn.text = f"Prodat ${cena}"
                else:
                    # Klikli jsme na prázdné políčko
                    if self.vybrany_typ_kytky_data:
                        self.place_plant(grid_x, grid_y)
                    else:
                        self.vybrana_polozena_kytka = None # Zruší výběr, pokud klikneme do prázdna
            else:
                self.select_ui_item(mouse_x, mouse_y)

    def place_plant(self, gx, gy):
        """
        Položí novou kytku na souřadnice (gx, gy) v mřížce.
        Předtím zkontroluje, jestli má hráč peníze, jestli je políčko volné a jestli je to políčko na trávě.
        """
        if self.vybrany_typ_kytky_data and config.AKTUALNI_MAPA[gy][gx] == 0:
            if (gx, gy) not in self.seznam_obsazenych_policek:
                if self.hrac.ma_dostatek(self.vybrany_typ_kytky_data["cena"]):
                    self.hrac.uber_penize(self.vybrany_typ_kytky_data["cena"])
                    if self.vybrany_typ_kytky_data["nazev"] == "Hrachostřel":
                        self.seznam_kytek.append(Hrachostrel(gx, gy))
                    elif self.vybrany_typ_kytky_data["nazev"] == "Kaktus":
                        self.seznam_kytek.append(Kaktus(gx, gy))
                    elif self.vybrany_typ_kytky_data["typ"] == "ekonomicka":
                        self.seznam_kytek.append(Studna(gx, gy))
                    self.seznam_obsazenych_policek.append((gx, gy))
                    self.vybrany_typ_kytky_data = None

    def sell_plant(self):
        """Smaže vybranou kytku z mapy a vrátí hráči polovinu její pořizovací ceny."""
        if self.vybrana_polozena_kytka:
            cena = self.vybrana_polozena_kytka.data["cena"] // 2
            self.hrac.pridej_penize(cena)
            self.seznam_kytek.remove(self.vybrana_polozena_kytka)
            self.seznam_obsazenych_policek.remove((self.vybrana_polozena_kytka.grid_x, self.vybrana_polozena_kytka.grid_y))
            self.vybrana_polozena_kytka = None

    def select_ui_item(self, mx, my):
        """Zjistí, na kterou kytku hráč kliknul v dolním panelu (UI)."""
        for item in self.plant_buttons:
            if item["btn"].is_clicked((mx, my)):
                self.vybrany_typ_kytky_data = item["data"]
                self.vybrana_polozena_kytka = None # Zruší výběr postavené kytky

    def update(self):
        """
        Logika hry, která běží 60x za vteřinu.
        Tady se řeší matematika, pohyb střel a nepřátel, hlídají se zásahy (kolize) a umírání.
        """
        if self.paused or self.game_over:
            return
            
        # Přičteme čas (v milisekundách), který uběhl od posledního snímku
        self.survived_time_ms += self.clock.get_time()
            
        self.wave_manager.update(self.seznam_veganu, self.hrac, self.game_speed)
        
        for kytka in self.seznam_kytek:
            if not self.wave_manager.wave_started:
                kytka.posledni_akce_cas = pygame.time.get_ticks()
                
            kytka.update(self.seznam_veganu, self.seznam_strel, self.hrac, self.game_speed)

        # Kontrola, zda některá ze střel nezasáhla nějakého Vegana
        for strela in self.seznam_strel:
            strela.update(self.game_speed)
            for vegan in self.seznam_veganu:
                dist = strela.pozice.distance_to(vegan.pozice)
                # Hitbox (kruh zásahu) záleží na velikosti (poloměru) konkrétního vegana
                if dist < vegan.polomer + 5:
                    vegan.vezmi_poskozeni(strela.poskozeni)
                    strela.je_ziva = False

        # Pročistíme seznamy (smažeme ty střely a vegany, kteří v tomto framu umřeli / narazili)
        self.seznam_strel = [strela for strela in self.seznam_strel if strela.je_ziva]
        self.seznam_veganu = [vegan for vegan in self.seznam_veganu if vegan.hp > 0]
        
        for vegan in self.seznam_veganu:
            vegan.move(self.game_speed)
            # Pokud vegan došel na poslední waypoint, je konec hry
            if vegan.aktualni_cil_index >= len(vegan.waypoints):
                self.game_over = True

    def draw(self):
        """
        Vykreslí vše na obrazovku v přesném pořadí (odspodu nahoru). 
        Co se vykreslí dřív, to je vespod (jako malování na plátno).
        """
        # OOP: Vykreslování mapy a mřížky delegujeme na instanci mapy
        self.mapa.draw(self.screen, self.wave_manager.wave_started)

        for kytka in self.seznam_kytek: kytka.draw(self.screen)
        for strela in self.seznam_strel: strela.draw(self.screen)
        for vegan in self.seznam_veganu: vegan.draw(self.screen)
            
        # Vykreslení dosahu a tlačítka u aktuálně vybrané kytky na mapě
        if self.vybrana_polozena_kytka:
            kytka = self.vybrana_polozena_kytka
            if "dostřel" in kytka.data:
                s = pygame.Surface((config.SIRKA_OKNA, config.VYSKA_OKNA), pygame.SRCALPHA)
                pygame.draw.circle(s, (255, 255, 255, 50), (kytka.x, kytka.y), kytka.data["dostřel"])
                pygame.draw.circle(s, (255, 255, 255, 150), (kytka.x, kytka.y), kytka.data["dostřel"], 2)
                self.screen.blit(s, (0, 0))
            self.sell_btn.draw(self.screen)

        self.draw_ui()

        if self.game_over:
            self.draw_game_over()
        elif self.paused:
            self.draw_pause_menu()

        pygame.display.flip()

    def draw_ui(self):
        pygame.draw.rect(self.screen, config.BARVA_UI_POZADI, (0, config.VYSKA_MAPY, config.SIRKA_OKNA, config.VYSKA_UI))
        penize_text = self.font_ui.render(f"Peníze: ${self.hrac.penize}", True, (255, 255, 255))
        vlna_text = self.font_ui.render(f"Vlna: {self.wave_manager.current_wave}", True, (255, 255, 255))
        self.screen.blit(penize_text, (config.SIRKA_OKNA - 150, config.VYSKA_MAPY + 10))
        self.screen.blit(vlna_text, (config.SIRKA_OKNA - 150, config.VYSKA_MAPY + 40))
        
        for item in self.plant_buttons:
            btn = item["btn"]
            data = item["data"]
            
            # Zlatý okraj pro zvýraznění aktuálně vybrané kytky
            if self.vybrany_typ_kytky_data is not None and self.vybrany_typ_kytky_data["nazev"] == data["nazev"]:
                pygame.draw.rect(self.screen, config.BARVA_UI_VYBER, (btn.rect.x - 3, btn.rect.y - 3, btn.rect.width + 6, btn.rect.height + 6), 3)
            
            btn.draw(self.screen)

        if not self.wave_manager.wave_started:
            self.start_wave_btn.draw(self.screen)
        else:
            self.speed_btn.draw(self.screen)

    def draw_pause_menu(self):
        s = pygame.Surface((config.SIRKA_OKNA, config.VYSKA_OKNA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        self.screen.blit(s, (0, 0))

        self.continue_btn.draw(self.screen)
        self.settings_btn.draw(self.screen)
        self.main_menu_btn.draw(self.screen)

        lbl_pause = self.font_pause.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(lbl_pause, (config.SIRKA_OKNA//2 - lbl_pause.get_width()//2, 80))

    def draw_game_over(self):
        """Ztmaví obrazovku červenou barvou, vypíše skóre a nabídne restartování nebo návrat do menu."""
        s = pygame.Surface((config.SIRKA_OKNA, config.VYSKA_OKNA), pygame.SRCALPHA)
        s.fill((50, 0, 0, 180)) # Červený poloprůhledný nádech
        self.screen.blit(s, (0, 0))

        lbl_over = self.font_pause.render("GAME OVER", True, (255, 50, 50))
        self.screen.blit(lbl_over, (config.SIRKA_OKNA//2 - lbl_over.get_width()//2, 80))

        # --- Vypsání statistik přežití ---
        total_seconds = self.survived_time_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        lbl_wave = self.font_ui.render(f"Dosažená vlna: {self.wave_manager.current_wave}", True, (255, 255, 255))
        lbl_time = self.font_ui.render(f"Doba přežití: {minutes:02d}:{seconds:02d}", True, (255, 255, 255))
        self.screen.blit(lbl_wave, (config.SIRKA_OKNA//2 - lbl_wave.get_width()//2, 160))
        self.screen.blit(lbl_time, (config.SIRKA_OKNA//2 - lbl_time.get_width()//2, 190))

        self.restart_btn.draw(self.screen)
        self.go_main_menu_btn.draw(self.screen)

    def run(self):
        """
        Samotná 'smyčka', která volá vstupy, update a kreslení furt dokola podle přednastaveného FPS.
        Vrátí informaci o tom, co má hra udělat, až se z ní hráč vrátí (MENU nebo RESTART).
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)
        return self.action_after_quit

class HerniAplikace:
    """
    Úplně nejvyšší třída celého programu, která funguje jako State Manager (přepínač stavů).
    Stará se o plynulé překlikávání mezi hlavním menu a hrou, aniž by se program vypnul.
    """
    def spust_hru(self):
        while True:
            screen = pygame.display.set_mode((config.SIRKA_OKNA, config.VYSKA_OKNA), pygame.FULLSCREEN | pygame.SCALED)
            game = PlantsVsVegansGame(screen)
            action = game.run()
            if action != "RESTART":
                break
                
    def run(self):
        while True:
            m = Menu()
            akce = m.main_menu()
            
            if akce == "PLAY":
                if pygame.mixer.get_init() is not None:
                    pygame.mixer.music.stop()
                self.spust_hru()
            else:
                break

if __name__ == "__main__":
    app = HerniAplikace()
    app.run()