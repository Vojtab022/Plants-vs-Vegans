import pygame
import sys
import config
from vegans.zakladni_vegan import ZakladniVegan 
from plants.hrachostrel import Hrachostrel
from plants.slunecnice import Slunecnice

class PlantsVsVegansGame:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font_ui = pygame.font.SysFont("Arial", 20, bold=True)
        self.font_pause = pygame.font.SysFont("Arial", 60, bold=True)
        
        # Herní stav 
        self.running = True
        self.paused = False
        self.pause_start_cas = 0
        self.penize = 200
        self.vybrany_typ_kytky_data = None
        
        # Seznamy objektů 
        self.seznam_veganu = []
        self.seznam_kytek = []
        self.seznam_strel = []
        self.seznam_obsazenych_policek = []
        
        # Časovače
        self.cas_posledniho_spawnu = pygame.time.get_ticks()
        self.celkem_vygenerovano = 0
        self.spawn_interval = 2500
        self.max_veganu_ve_vlne = 10

        # UI Tlačítka pro pauzu
        btn_w, btn_h = 200, 60
        stred_x = config.SIRKA_OKNA // 2 - btn_w // 2
        self.continue_btn = pygame.Rect(stred_x, 200, btn_w, btn_h)
        self.settings_btn = pygame.Rect(stred_x, 280, btn_w, btn_h)
        self.main_menu_btn = pygame.Rect(stred_x, 360, btn_w, btn_h)

    def spawn_vegans(self):
        nyni = pygame.time.get_ticks()
        if nyni - self.cas_posledniho_spawnu > self.spawn_interval and self.celkem_vygenerovano < self.max_veganu_ve_vlne:
            novy_vegan = ZakladniVegan(config.AKTUALNI_WAYPOINTY)
            self.seznam_veganu.append(novy_vegan)
            self.cas_posledniho_spawnu = nyni
            self.celkem_vygenerovano += 1
            print(f"Pozor! Na mapu vstoupil vegan číslo {self.celkem_vygenerovano}!")

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
            self.cas_posledniho_spawnu += posun
            for kytka in self.seznam_kytek:
                kytka.posledni_akce_cas += posun

    def handle_click(self, pos):
        mouse_x, mouse_y = pos
        if self.paused:
            if self.continue_btn.collidepoint(pos):
                self.toggle_pause()
            elif self.main_menu_btn.collidepoint(pos):
                self.running = False
            elif self.settings_btn.collidepoint(pos):
                import menu
                m = menu.Menu()
                m.settings_menu()
        else:
            if mouse_y < config.VYSKA_MAPY:
                grid_x = mouse_x // config.VELIKOST_POLICKA
                grid_y = mouse_y // config.VELIKOST_POLICKA
                self.place_plant(grid_x, grid_y)
            else:
                self.select_ui_item(mouse_x, mouse_y)

    def place_plant(self, gx, gy):
        if self.vybrany_typ_kytky_data and config.AKTUALNI_MAPA[gy][gx] == 0:
            if (gx, gy) not in self.seznam_obsazenych_policek:
                if self.penize >= self.vybrany_typ_kytky_data["cena"]:
                    self.penize -= self.vybrany_typ_kytky_data["cena"]
                    if self.vybrany_typ_kytky_data["typ"] == "utocna":
                        self.seznam_kytek.append(Hrachostrel(gx, gy))
                    elif self.vybrany_typ_kytky_data["typ"] == "ekonomicka":
                        self.seznam_kytek.append(Slunecnice(gx, gy))
                    self.seznam_obsazenych_policek.append((gx, gy))
                    self.vybrany_typ_kytky_data = None

    def select_ui_item(self, mx, my):
        for i, data in enumerate(config.SEZNAM_DOSTUPNYCH_KYTEK):
            btn_rect = pygame.Rect(10 + (i * 160), config.VYSKA_MAPY + 10, 150, 80)
            if btn_rect.collidepoint(mx, my):
                self.vybrany_typ_kytky_data = data

    def update(self):
        if self.paused:
            return
        
        self.spawn_vegans()
        
        for kytka in self.seznam_kytek:
            nove_penize = kytka.update(self.seznam_veganu, self.seznam_strel, self.penize)
            if nove_penize is not None:
                self.penize = nove_penize

        for strela in self.seznam_strel:
            strela.update()
            for vegan in self.seznam_veganu:
                dist = strela.pozice.distance_to(vegan.pozice)
                if dist < 15:
                    vegan.hp -= config.STRELA_HRY_DATA["poskozeni"]
                    strela.je_ziva = False

        self.seznam_strel = [strela for strela in self.seznam_strel if strela.je_ziva]
        self.seznam_veganu = [vegan for vegan in self.seznam_veganu if vegan.hp > 0]
        for vegan in self.seznam_veganu:
            vegan.move()

    def draw(self):
        for radek_index in range(config.RADKU):
            for sloupec_index in range(config.SLOUPCU):
                cislo_policka = config.AKTUALNI_MAPA[radek_index][sloupec_index]
                x = sloupec_index * config.VELIKOST_POLICKA
                y = radek_index * config.VELIKOST_POLICKA
                barva = config.BARVA_TRAVY if cislo_policka == 0 else config.BARVA_CESTY
                pygame.draw.rect(self.screen, barva, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
                pygame.draw.rect(self.screen, config.BARVA_MRIZKY, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA), 1)

        for kytka in self.seznam_kytek: kytka.draw(self.screen)
        for strela in self.seznam_strel: strela.draw(self.screen)
        for vegan in self.seznam_veganu: vegan.draw(self.screen)
            
        self.draw_ui()

        if self.paused:
            self.draw_pause_menu()

        pygame.display.flip()

    def draw_ui(self):
        pygame.draw.rect(self.screen, config.BARVA_UI_POZADI, (0, config.VYSKA_MAPY, config.SIRKA_OKNA, config.VYSKA_UI))
        penize_text = self.font_ui.render(f"Peníze: ${self.penize}", True, (255, 255, 255))
        self.screen.blit(penize_text, (config.SIRKA_OKNA - 150, config.VYSKA_MAPY + 10))
        
        for i, data in enumerate(config.SEZNAM_DOSTUPNYCH_KYTEK):
            btn_x = 10 + (i * 160)
            btn_y = config.VYSKA_MAPY + 10
            btn_width, btn_height = 150, 80
            btn_rect = (btn_x, btn_y, btn_width, btn_height)
            
            if self.vybrany_typ_kytky_data is not None and self.vybrany_typ_kytky_data["nazev"] == data["nazev"]:
                pygame.draw.rect(self.screen, config.BARVA_UI_VYBER, (btn_x - 3, btn_y - 3, btn_width + 6, btn_height + 6), 3)
            
            pygame.draw.rect(self.screen, data["barva"], btn_rect)
            pygame.draw.rect(self.screen, (0,0,0), btn_rect, 2)
            
            text_name = self.font_ui.render(data["nazev"], True, (0, 0, 0))
            text_price = self.font_ui.render(f"${data['cena']}", True, (0, 0, 0))
            self.screen.blit(text_name, (btn_x + 10, btn_y + 10))
            self.screen.blit(text_price, (btn_x + 10, btn_y + 40))

    def draw_pause_menu(self):
        s = pygame.Surface((config.SIRKA_OKNA, config.VYSKA_OKNA), pygame.SRCALPHA)
        s.fill((0, 0, 0, 160))
        self.screen.blit(s, (0, 0))

        mouse_x, mouse_y = pygame.mouse.get_pos()

        barva_cont = (0, 200, 0) if self.continue_btn.collidepoint(mouse_x, mouse_y) else (0, 150, 0)
        barva_set = (0, 200, 0) if self.settings_btn.collidepoint(mouse_x, mouse_y) else (0, 150, 0)
        barva_menu = (0, 200, 0) if self.main_menu_btn.collidepoint(mouse_x, mouse_y) else (0, 150, 0)

        for btn, color in [(self.continue_btn, barva_cont), (self.settings_btn, barva_set), (self.main_menu_btn, barva_menu)]:
            pygame.draw.rect(self.screen, color, btn)
            pygame.draw.rect(self.screen, (255, 255, 255), btn, 2)

        lbl_cont = self.font_ui.render("Continue", True, (255, 255, 255))
        lbl_set = self.font_ui.render("Settings", True, (255, 255, 255))
        lbl_menu = self.font_ui.render("Main Menu", True, (255, 255, 255))

        self.screen.blit(lbl_cont, (self.continue_btn.x + self.continue_btn.width//2 - lbl_cont.get_width()//2, self.continue_btn.y + self.continue_btn.height//2 - lbl_cont.get_height()//2))
        self.screen.blit(lbl_set, (self.settings_btn.x + self.settings_btn.width//2 - lbl_set.get_width()//2, self.settings_btn.y + self.settings_btn.height//2 - lbl_set.get_height()//2))
        self.screen.blit(lbl_menu, (self.main_menu_btn.x + self.main_menu_btn.width//2 - lbl_menu.get_width()//2, self.main_menu_btn.y + self.main_menu_btn.height//2 - lbl_menu.get_height()//2))

        lbl_pause = self.font_pause.render("PAUSED", True, (255, 255, 255))
        self.screen.blit(lbl_pause, (config.SIRKA_OKNA//2 - lbl_pause.get_width()//2, 80))

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(config.FPS)

def start_game():
    screen = pygame.display.set_mode((config.SIRKA_OKNA, config.VYSKA_OKNA))
    game = PlantsVsVegansGame(screen)
    game.run()

if __name__ == "__main__":
    print("Přesměrování do hlavního menu...")
    import menu
    menu.main_menu()