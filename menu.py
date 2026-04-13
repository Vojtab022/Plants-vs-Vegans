import pygame
import sys
import main
import config

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Plants vs Vegans")

font = pygame.font.SysFont(None, 50)

# barvy
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)

# tlačítka (rectangles)
play_btn = pygame.Rect(300, 200, 200, 60)
settings_btn = pygame.Rect(300, 280, 200, 60)
quit_btn = pygame.Rect(300, 360, 200, 60)

# tlačítka pro nastavení
fps_btn = pygame.Rect(300, 200, 200, 60)
cursor_btn = pygame.Rect(300, 280, 200, 60)
back_btn = pygame.Rect(300, 360, 200, 60)

# tlačítka pro levely
level1_btn = pygame.Rect(300, 200, 200, 60)
level2_btn = pygame.Rect(300, 280, 200, 60)

def draw_button(rect, text, mouse_pos):
    if rect.collidepoint(mouse_pos):
        color = DARK_GREEN
    else:
        color = GREEN

    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, WHITE)
    screen.blit(label, (rect.x + 40, rect.y + 10))

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
                    # Přepínání FPS mezi 60 a 30
                    config.FPS = 30 if config.FPS == 60 else 60

                if cursor_btn.collidepoint(mouse_pos):
                    # Přepínání vzhledu kurzoru
                    if config.CURSOR_SKIN == "Arrow":
                        config.CURSOR_SKIN = "Crosshair"
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
                    else:
                        config.CURSOR_SKIN = "Arrow"
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                if back_btn.collidepoint(mouse_pos):
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
                    config.AKTUALNI_MAPA = config.MAPA_LEVEL_1
                    config.AKTUALNI_WAYPOINTY = config.WAYPOINTY
                    return True  # Vracíme True jako signál pro spuštění hry
                if level2_btn.collidepoint(mouse_pos):
                    config.AKTUALNI_MAPA = config.MAPA_LEVEL_2
                    config.AKTUALNI_WAYPOINTY = config.WAYPOINTY_LEVEL_2
                    return True
                if back_btn.collidepoint(mouse_pos):
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
                    vyber = levels_menu()
                    if vyber == True: # Pokud hráč zvolil level a neklikl na "Back"
                        # Zavoláme hlavní herní smyčku ze souboru main.py
                        main.start_game()
                        # Až hráč herní okno zavře, hra se vrátí sem. My jen znovu nastavíme velikost okna pro menu.
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        pygame.display.set_caption("Plants vs Vegans")

                if settings_btn.collidepoint(mouse_pos):
                    settings_menu()

                if quit_btn.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

if __name__ == "__main__":
    main_menu()
