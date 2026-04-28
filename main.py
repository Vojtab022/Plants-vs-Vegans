import pygame
import sys
import random
import config
import menu
from player import Hrac
from wave_manager import WaveManager
from plants.hrachostrel import Hrachostrel
from plants.kaktus import Kaktus
from plants.studna import Studna
from ui import Button

class PlantsVsVegansGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_ui = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_pause = pygame.font.SysFont("Arial", 60, bold=True)
        
        # Herní stav 
        self.running = True
        self.paused = False
        self.game_over = False
        self.action_after_quit = "MENU"
        self.pause_start_cas = 0
        self.hrac = Hrac(200)
        self.wave_manager = WaveManager()
        self.vybrany_typ_kytky_data = None
        self.survived_time_ms = 0
        
        # Výběr a prodej existující kytky
        self.vybrana_polozena_kytka = None
        self.sell_btn = Button(0, 0, 120, 35, "Prodat", self.font_ui, (200, 0, 0), (255, 50, 50))

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
        self.start_wave_btn = Button(config.SIRKA_OKNA - 350, config.VYSKA_MAPY + 20, 180, 60, "Start Wave", self.font_ui, (200, 0, 0), (255, 50, 50))

        # Tlačítka pro výběr kytek v UI
        self.plant_buttons = []
        for i, data in enumerate(config.SEZNAM_DOSTUPNYCH_KYTEK):
            bx = 10 + (i * 160)
            by = config.VYSKA_MAPY + 10
            barva_zaklad = data["barva"]
            # Vypočítáme trochu světlejší barvu pro hover efekt
            barva_hover = (min(255, barva_zaklad[0]+40), min(255, barva_zaklad[1]+40), min(255, barva_zaklad[2]+40))
            btn = Button(bx, by, 150, 80, f"{data['nazev']} ${data['cena']}", self.font_ui, barva_zaklad, barva_hover, (0, 0, 0))
            self.plant_buttons.append({"btn": btn, "data": data})

        # Tlačítka pro Game Over
        self.restart_btn = Button(stred_x, 260, btn_w, btn_h, "Restart", self.font_ui, (200, 0, 0), (255, 50, 50))
        self.go_main_menu_btn = Button(stred_x, 340, btn_w, btn_h, "Main Menu", self.font_ui, (200, 0, 0), (255, 50, 50))

        # Načtení textur cesty a vygenerování fixní mapy textur
        self.path_images = []
        try:
            for i in range(1, 4):
                img = pygame.image.load(f"gfx/path{i}.png").convert_alpha()
                img = pygame.transform.smoothscale(img, (config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
                self.path_images.append(img)
        except (pygame.error, FileNotFoundError):
            self.path_images = None
            
        self.grid_textur = []
        for radek in config.AKTUALNI_MAPA:
            radek_textur = []
            for policko in radek:
                # Pokud je to cesta (1) a obrázky se úspěšně načetly, vybereme náhodný
                if policko == 1 and self.path_images:
                    radek_textur.append(random.choice(self.path_images))
                else:
                    radek_textur.append(None) # Tráva nebo fallback
            self.grid_textur.append(radek_textur)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.toggle_pause()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(pygame.mouse.get_pos())

    def toggle_pause(self):
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
                m = menu.Menu(in_game=True)
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

            # Kontrola kliknutí na plovoucí tlačítko Prodat
            if self.vybrana_polozena_kytka and self.sell_btn.is_clicked(pos):
                self.sell_plant()
                return

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
        if self.vybrana_polozena_kytka:
            cena = self.vybrana_polozena_kytka.data["cena"] // 2
            self.hrac.pridej_penize(cena)
            self.seznam_kytek.remove(self.vybrana_polozena_kytka)
            self.seznam_obsazenych_policek.remove((self.vybrana_polozena_kytka.grid_x, self.vybrana_polozena_kytka.grid_y))
            self.vybrana_polozena_kytka = None

    def select_ui_item(self, mx, my):
        for item in self.plant_buttons:
            if item["btn"].is_clicked((mx, my)):
                self.vybrany_typ_kytky_data = item["data"]
                self.vybrana_polozena_kytka = None # Zruší výběr postavené kytky

    def update(self):
        if self.paused or self.game_over:
            return
            
        # Přičteme čas (v milisekundách), který uběhl od posledního snímku
        self.survived_time_ms += self.clock.get_time()
            
        self.wave_manager.update(self.seznam_veganu, self.hrac)
        
        for kytka in self.seznam_kytek:
            if not self.wave_manager.wave_started:
                kytka.posledni_akce_cas = pygame.time.get_ticks()
                
            kytka.update(self.seznam_veganu, self.seznam_strel, self.hrac)

        for strela in self.seznam_strel:
            strela.update()
            for vegan in self.seznam_veganu:
                dist = strela.pozice.distance_to(vegan.pozice)
                # Hitbox záleží na velikosti (poloměru) konkrétního vegana
                if dist < vegan.polomer + 5: 
                    vegan.vezmi_poskozeni(strela.poskozeni)
                    strela.je_ziva = False

        self.seznam_strel = [strela for strela in self.seznam_strel if strela.je_ziva]
        self.seznam_veganu = [vegan for vegan in self.seznam_veganu if vegan.hp > 0]
        for vegan in self.seznam_veganu:
            vegan.move()
            # Pokud vegan došel na poslední waypoint, je konec hry
            if vegan.aktualni_cil_index >= len(vegan.waypoints):
                self.game_over = True

    def draw(self):
        for radek_index in range(config.RADKU):
            for sloupec_index in range(config.SLOUPCU):
                cislo_policka = config.AKTUALNI_MAPA[radek_index][sloupec_index]
                x = sloupec_index * config.VELIKOST_POLICKA
                y = radek_index * config.VELIKOST_POLICKA
                
                if cislo_policka == 1 and self.grid_textur[radek_index][sloupec_index]:
                    self.screen.blit(self.grid_textur[radek_index][sloupec_index], (x, y))
                else:
                    barva = config.BARVA_TRAVY if cislo_policka == 0 else config.BARVA_CESTY
                    pygame.draw.rect(self.screen, barva, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
                pygame.draw.rect(self.screen, config.BARVA_MRIZKY, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA), 1)

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
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)
        return self.action_after_quit

def start_game():
    while True:
        screen = pygame.display.set_mode((config.SIRKA_OKNA, config.VYSKA_OKNA), pygame.FULLSCREEN | pygame.SCALED)
        game = PlantsVsVegansGame(screen)
        action = game.run()
        if action != "RESTART":
            break

if __name__ == "__main__":
    # Hlavní smyčka aplikace (State Manager), která řídí přechody mezi menu a hrou
    while True:
        m = menu.Menu()
        akce = m.main_menu()
        
        if akce == "PLAY":
            # Zkontrolujeme, zda se zvukový modul úspěšně načetl, abychom předešli pádu hry
            if pygame.mixer.get_init() is not None:
                pygame.mixer.music.stop()
            start_game()