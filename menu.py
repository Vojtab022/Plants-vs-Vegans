import pygame
import sys
import config
from ui import Button

class Menu:
    def __init__(self, in_game=False):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        
        if not in_game:
            self.width, self.height = 800, 600
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN | pygame.SCALED)
            pygame.display.set_caption("Plants vs Vegans")
            
            try:
                ikona = pygame.image.load("gfx/hrachstrel_IDLE.png").convert_alpha()
                pygame.display.set_icon(ikona)
            except (pygame.error, FileNotFoundError):
                pass
                
            self.hraj_hudbu_menu()
        else:
            self.screen = pygame.display.get_surface()
            self.width, self.height = self.screen.get_size()
        
        self.font = pygame.font.SysFont(None, 40)
        self.title_font = pygame.font.SysFont(None, 60)
        
        self.WHITE = (255, 255, 255)
        self.GRAY = (100, 100, 100)
        self.GREEN = (0, 200, 0)
        self.DARK_GREEN = (0, 150, 0)
        
        try:
            self.click_sound = pygame.mixer.Sound("Sound/click.wav")
        except (pygame.error, FileNotFoundError):
            self.click_sound = None
            
        self.play_btn = Button(200, 200, 400, 60, "Play", self.font, self.DARK_GREEN, self.GREEN)
        self.settings_btn = Button(200, 280, 400, 60, "Settings", self.font, self.DARK_GREEN, self.GREEN)
        self.quit_btn = Button(200, 360, 400, 60, "Quit", self.font, self.DARK_GREEN, self.GREEN)
        
        self.fps_btn = Button(200, 120, 400, 50, f"FPS: {config.FPS}", self.font, self.DARK_GREEN, self.GREEN)
        self.cursor_btn = Button(200, 180, 400, 50, f"Cursor: {config.CURSOR_SKIN}", self.font, self.DARK_GREEN, self.GREEN)
        self.vol_music_down = Button(200, 260, 50, 50, "-", self.font, self.DARK_GREEN, self.GREEN)
        self.vol_music_up = Button(550, 260, 50, 50, "+", self.font, self.DARK_GREEN, self.GREEN)
        self.vol_sfx_down = Button(200, 320, 50, 50, "-", self.font, self.DARK_GREEN, self.GREEN)
        self.vol_sfx_up = Button(550, 320, 50, 50, "+", self.font, self.DARK_GREEN, self.GREEN)
        self.back_btn = Button(200, 420, 400, 60, "Back", self.font, self.DARK_GREEN, self.GREEN)
        
        self.level1_btn = Button(200, 200, 400, 60, "Level 1", self.font, self.DARK_GREEN, self.GREEN)
        self.level2_btn = Button(200, 280, 400, 60, "Level 2", self.font, self.DARK_GREEN, self.GREEN)

        self.nastav_kurzor(config.CURSOR_SKIN)

    def hraj_hudbu_menu(self):
        try:
            pygame.mixer.music.load("Sound/Background_Music.mp3")
            pygame.mixer.music.set_volume(config.HLASITOST_HUDBY)
            pygame.mixer.music.play(-1)
        except (pygame.error, FileNotFoundError):
            pass

    def hraj_klik(self):
        if self.click_sound:
            self.click_sound.set_volume(config.HLASITOST_EFEKTU)
            self.click_sound.play()

    def nastav_kurzor(self, skin_name):
        try:
            if skin_name == "Zlatý kurzor":
                img = pygame.image.load("gfx/Cursor_1.png").convert_alpha()
                img = pygame.transform.smoothscale(img, (32, 32))
                pygame.mouse.set_cursor(pygame.Cursor((15, 2), img))
            else:
                img = pygame.image.load("gfx/Cursor_2.png").convert_alpha()
                img = pygame.transform.smoothscale(img, (32, 32))
                pygame.mouse.set_cursor(pygame.Cursor((8, 2), img))
        except (pygame.error, FileNotFoundError):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def levels_menu(self):
        while True:
            self.screen.fill(self.GRAY)
            mouse_pos = pygame.mouse.get_pos()
            
            title = self.title_font.render("Select Level", True, self.WHITE)
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 100))
            
            self.level1_btn.draw(self.screen)
            self.level2_btn.draw(self.screen)
            self.back_btn.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level1_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        config.AKTUALNI_MAPA = config.MAPA_LEVEL_1
                        config.AKTUALNI_WAYPOINTY = config.WAYPOINTY
                        return True
                    if self.level2_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        config.AKTUALNI_MAPA = config.MAPA_LEVEL_2
                        config.AKTUALNI_WAYPOINTY = config.WAYPOINTY_LEVEL_2
                        return True
                    if self.back_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        return False
            pygame.display.flip()

    def settings_menu(self):
        while True:
            self.screen.fill(self.GRAY)
            mouse_pos = pygame.mouse.get_pos()
            
            title = self.title_font.render("Settings", True, self.WHITE)
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
            
            self.fps_btn.text = f"FPS: {config.FPS}"
            self.fps_btn.draw(self.screen)
            self.cursor_btn.text = f"Cursor: {config.CURSOR_SKIN}"
            self.cursor_btn.draw(self.screen)
            
            self.vol_music_down.draw(self.screen)
            music_txt = self.font.render(f"Music: {int(config.HLASITOST_HUDBY * 100)}%", True, self.WHITE)
            self.screen.blit(music_txt, (300, 270))
            self.vol_music_up.draw(self.screen)
            
            self.vol_sfx_down.draw(self.screen)
            sfx_txt = self.font.render(f"SFX: {int(config.HLASITOST_EFEKTU * 100)}%", True, self.WHITE)
            self.screen.blit(sfx_txt, (300, 330))
            self.vol_sfx_up.draw(self.screen)
            
            self.back_btn.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.fps_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        config.FPS = 30 if config.FPS == 60 else 60
                    if self.cursor_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        config.CURSOR_SKIN = "Zelený kurzor" if config.CURSOR_SKIN == "Zlatý kurzor" else "Zlatý kurzor"
                        self.nastav_kurzor(config.CURSOR_SKIN)
                    if self.vol_music_down.is_clicked(mouse_pos):
                        config.HLASITOST_HUDBY = max(0.0, config.HLASITOST_HUDBY - 0.1)
                        pygame.mixer.music.set_volume(config.HLASITOST_HUDBY)
                        self.hraj_klik()
                    if self.vol_music_up.is_clicked(mouse_pos):
                        config.HLASITOST_HUDBY = min(1.0, config.HLASITOST_HUDBY + 0.1)
                        pygame.mixer.music.set_volume(config.HLASITOST_HUDBY)
                        self.hraj_klik()
                    if self.vol_sfx_down.is_clicked(mouse_pos):
                        config.HLASITOST_EFEKTU = max(0.0, config.HLASITOST_EFEKTU - 0.1)
                        self.hraj_klik()
                    if self.vol_sfx_up.is_clicked(mouse_pos):
                        config.HLASITOST_EFEKTU = min(1.0, config.HLASITOST_EFEKTU + 0.1)
                        self.hraj_klik()
                    if self.back_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        return
            pygame.display.flip()

    def main_menu(self):
        while True:
            self.screen.fill(self.GRAY)
            mouse_pos = pygame.mouse.get_pos()
            
            self.play_btn.draw(self.screen)
            self.settings_btn.draw(self.screen)
            self.quit_btn.draw(self.screen)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        if self.levels_menu():
                            return "PLAY"
                    if self.settings_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        self.settings_menu()
                    if self.quit_btn.is_clicked(mouse_pos):
                        self.hraj_klik()
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()

def main_menu():
    menu = Menu()
    menu.main_menu()