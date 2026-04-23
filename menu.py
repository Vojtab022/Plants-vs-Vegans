import pygame
import sys
import main
import config

class MenuSystem:
    def __init__(self):
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.init()
        
        self.width, self.height = 800, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Plants vs Vegans")
        
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
            
        self.play_btn = pygame.Rect(200, 200, 400, 60)
        self.settings_btn = pygame.Rect(200, 280, 400, 60)
        self.quit_btn = pygame.Rect(200, 360, 400, 60)
        
        self.fps_btn = pygame.Rect(200, 120, 400, 50)
        self.cursor_btn = pygame.Rect(200, 180, 400, 50)
        self.vol_music_down = pygame.Rect(200, 260, 50, 50)
        self.vol_music_up = pygame.Rect(550, 260, 50, 50)
        self.vol_sfx_down = pygame.Rect(200, 320, 50, 50)
        self.vol_sfx_up = pygame.Rect(550, 320, 50, 50)
        self.back_btn = pygame.Rect(200, 420, 400, 60)
        
        self.level1_btn = pygame.Rect(200, 200, 400, 60)
        self.level2_btn = pygame.Rect(200, 280, 400, 60)

        self.nastav_kurzor(config.CURSOR_SKIN)
        self.hraj_hudbu_menu()

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

    def draw_button(self, rect, text, mouse_pos):
        color = self.DARK_GREEN if rect.collidepoint(mouse_pos) else self.GREEN
        pygame.draw.rect(self.screen, color, rect)
        label = self.font.render(text, True, self.WHITE)
        text_rect = label.get_rect(center=rect.center)
        self.screen.blit(label, text_rect)

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
            
            self.draw_button(self.level1_btn, "Level 1", mouse_pos)
            self.draw_button(self.level2_btn, "Level 2", mouse_pos)
            self.draw_button(self.back_btn, "Back", mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.level1_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        config.AKTUALNI_MAPA = config.MAPA_LEVEL_1
                        config.AKTUALNI_WAYPOINTY = config.WAYPOINTY
                        return True
                    if self.level2_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        config.AKTUALNI_MAPA = config.MAPA_LEVEL_2
                        config.AKTUALNI_WAYPOINTY = config.WAYPOINTY_LEVEL_2
                        return True
                    if self.back_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        return False
            pygame.display.flip()

    def settings_menu(self):
        while True:
            self.screen.fill(self.GRAY)
            mouse_pos = pygame.mouse.get_pos()
            
            title = self.title_font.render("Settings", True, self.WHITE)
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 50))
            
            self.draw_button(self.fps_btn, f"FPS: {config.FPS}", mouse_pos)
            self.draw_button(self.cursor_btn, f"Cursor: {config.CURSOR_SKIN}", mouse_pos)
            
            self.draw_button(self.vol_music_down, "-", mouse_pos)
            music_txt = self.font.render(f"Music: {int(config.HLASITOST_HUDBY * 100)}%", True, self.WHITE)
            self.screen.blit(music_txt, (300, 270))
            self.draw_button(self.vol_music_up, "+", mouse_pos)
            
            self.draw_button(self.vol_sfx_down, "-", mouse_pos)
            sfx_txt = self.font.render(f"SFX: {int(config.HLASITOST_EFEKTU * 100)}%", True, self.WHITE)
            self.screen.blit(sfx_txt, (300, 330))
            self.draw_button(self.vol_sfx_up, "+", mouse_pos)
            
            self.draw_button(self.back_btn, "Back", mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.fps_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        config.FPS = 30 if config.FPS == 60 else 60
                    if self.cursor_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        config.CURSOR_SKIN = "Zelený kurzor" if config.CURSOR_SKIN == "Zlatý kurzor" else "Zlatý kurzor"
                        self.nastav_kurzor(config.CURSOR_SKIN)
                    if self.vol_music_down.collidepoint(mouse_pos):
                        config.HLASITOST_HUDBY = max(0.0, config.HLASITOST_HUDBY - 0.1)
                        pygame.mixer.music.set_volume(config.HLASITOST_HUDBY)
                        self.hraj_klik()
                    if self.vol_music_up.collidepoint(mouse_pos):
                        config.HLASITOST_HUDBY = min(1.0, config.HLASITOST_HUDBY + 0.1)
                        pygame.mixer.music.set_volume(config.HLASITOST_HUDBY)
                        self.hraj_klik()
                    if self.vol_sfx_down.collidepoint(mouse_pos):
                        config.HLASITOST_EFEKTU = max(0.0, config.HLASITOST_EFEKTU - 0.1)
                        self.hraj_klik()
                    if self.vol_sfx_up.collidepoint(mouse_pos):
                        config.HLASITOST_EFEKTU = min(1.0, config.HLASITOST_EFEKTU + 0.1)
                        self.hraj_klik()
                    if self.back_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        return
            pygame.display.flip()

    def main_menu(self):
        while True:
            self.screen.fill(self.GRAY)
            mouse_pos = pygame.mouse.get_pos()
            
            self.draw_button(self.play_btn, "Play", mouse_pos)
            self.draw_button(self.settings_btn, "Settings", mouse_pos)
            self.draw_button(self.quit_btn, "Quit", mouse_pos)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        if self.levels_menu():
                            pygame.mixer.music.stop()
                            main.start_game()
                            self.screen = pygame.display.set_mode((self.width, self.height))
                            self.hraj_hudbu_menu()
                    if self.settings_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        self.settings_menu()
                    if self.quit_btn.collidepoint(mouse_pos):
                        self.hraj_klik()
                        pygame.quit()
                        sys.exit()
            pygame.display.flip()

def main_menu():
    menu = MenuSystem()
    menu.main_menu()