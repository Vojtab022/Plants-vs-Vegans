import pygame
import sys
import main
import config

# Snížíme velikost audio bufferu, aby zvuky (kliknutí) neměly zpoždění
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plants vs Vegans")

font = pygame.font.SysFont(None, 50)

# Načtení zvuku kliknutí
try:
    click_sound = pygame.mixer.Sound("Sound/click.wav")
except (pygame.error, FileNotFoundError):
    click_sound = None

def hraj_hudbu_menu():
    """Spustí tichou hudbu v pozadí menu, pokud soubor existuje."""
    try:
        pygame.mixer.music.load("Sound/Background_Music.mp3")
        pygame.mixer.music.set_volume(0.2) # Nastaví hlasitost na 20 %
        pygame.mixer.music.play(-1) # -1 znamená, že bude hrát v nekonečné smyčce
    except (pygame.error, FileNotFoundError):
        pass # Pokud soubor nenajde, hra poběží bez hudby

# Spustíme hudbu hned po startu menu
hraj_hudbu_menu()

# barvy
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# tlačítka (rectangles)
play_btn = pygame.Rect(200, 200, 400, 60)
settings_btn = pygame.Rect(200, 280, 400, 60)
quit_btn = pygame.Rect(200, 360, 400, 60)

# tlačítka pro nastavení
fps_btn = pygame.Rect(200, 200, 400, 60)
cursor_btn = pygame.Rect(200, 280, 400, 60)
back_btn = pygame.Rect(200, 360, 400, 60)

# tlačítka pro levely
level1_btn = pygame.Rect(200, 200, 400, 60)
level2_btn = pygame.Rect(200, 280, 400, 60)

def draw_button(rect, text, mouse_pos):
    if rect.collidepoint(mouse_pos):
        color = DARK_GREEN
    else:
        color = GREEN

    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, WHITE)
    # Automatické vycentrování textu doprostřed tlačítka
    text_rect = label.get_rect(center=rect.center)
    screen.blit(label, text_rect)

def nastav_kurzor(skin_name):
    try:
        if skin_name == "Zlatý kurzor":
            img = pygame.image.load("gfx/Cursor_1.png").convert_alpha()
            # Zmenší obrázek na velikost 32x32 pixelů
            img = pygame.transform.smoothscale(img, (32, 32))
            # Zlatý kurzor míří nahoru a špička je zhruba uprostřed (osa X)
            # První číslo je X (doprava), druhé je Y (dolů)
            pygame.mouse.set_cursor(pygame.Cursor((15, 2), img))
        elif skin_name == "Zelený kurzor":
            img = pygame.image.load("gfx/Cursor_2.png").convert_alpha()
            # Zmenší obrázek na velikost 32x32 pixelů
            img = pygame.transform.smoothscale(img, (32, 32))
            # Zelený kurzor míří doleva nahoru, špička je blízko levého horního rohu
            pygame.mouse.set_cursor(pygame.Cursor((8, 2), img))
    except (pygame.error, FileNotFoundError):
        # Záložní řešení, pokud hra obrázky nenajde
        if skin_name == "Zelený kurzor":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

# Nastavení výchozího kurzoru při startu menu
nastav_kurzor(config.CURSOR_SKIN)

def hraj_klik():
    """Přehraje zvuk kliknutí, pokud je načtený."""
    if click_sound:
        click_sound.play()

def settings_menu():
    global screen
    while True:
        screen.fill(GRAY)
        mouse_pos = pygame.mouse.get_pos()

        # Nadpis
        title = font.render("Settings", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        draw_button(fps_btn, f"FPS: {config.FPS}", mouse_pos)
        draw_button(cursor_btn, f"Cursor: {config.CURSOR_SKIN}", mouse_pos)
        draw_button(back_btn, "Back", mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if fps_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    # Přepínání FPS mezi 60 a 30
                    config.FPS = 30 if config.FPS == 60 else 60

                if cursor_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    # Přepínání vzhledu kurzoru
                    if config.CURSOR_SKIN == "Zlatý kurzor":
                        config.CURSOR_SKIN = "Zelený kurzor"
                    else:
                        config.CURSOR_SKIN = "Zlatý kurzor"
                    nastav_kurzor(config.CURSOR_SKIN)

                if back_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    return  # Přeruší tuto smyčku a vrátí nás do main_menu()

        pygame.display.flip()

def levels_menu():
    global screen
    while True:
        screen.fill(GRAY)
        mouse_pos = pygame.mouse.get_pos()

        # Nadpis
        title = font.render("Select Level", True, WHITE)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        draw_button(level1_btn, "Level 1", mouse_pos)
        draw_button(level2_btn, "Level 2", mouse_pos)
        draw_button(back_btn, "Back", mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if level1_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    config.AKTUALNI_MAPA = config.MAPA_LEVEL_1
                    config.AKTUALNI_WAYPOINTY = config.WAYPOINTY
                    return True  # Vracíme True jako signál pro spuštění hry
                if level2_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    config.AKTUALNI_MAPA = config.MAPA_LEVEL_2
                    config.AKTUALNI_WAYPOINTY = config.WAYPOINTY_LEVEL_2
                    return True
                if back_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    return False # Zpět do hlavního menu

        pygame.display.flip()

def main_menu():
    global screen
    while True:
        screen.fill(GRAY)
        mouse_pos = pygame.mouse.get_pos()

        draw_button(play_btn, "Play", mouse_pos)
        draw_button(settings_btn, "Settings", mouse_pos)
        draw_button(quit_btn, "Quit", mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    vyber = levels_menu()
                    if vyber == True: # Pokud hráč zvolil level a neklikl na "Back"
                        pygame.mixer.music.stop() # Před startem hry hudbu z menu vypneme
                        # Zavoláme hlavní herní smyčku ze souboru main.py
                        main.start_game()
                        # Až hráč herní okno zavře, hra se vrátí sem. My jen znovu nastavíme velikost okna pro menu.
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Plants vs Vegans")
                        hraj_hudbu_menu() # Po návratu do menu hudbu opět zapneme

                if settings_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    settings_menu()

                if quit_btn.collidepoint(mouse_pos):
                    hraj_klik()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
