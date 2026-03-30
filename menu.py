import pygame
import sys

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

def draw_button(rect, text, mouse_pos):
    if rect.collidepoint(mouse_pos):
        color = DARK_GREEN
    else:
        color = GREEN

    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, WHITE)
    screen.blit(label, (rect.x + 40, rect.y + 10))

def main_menu():
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
                    print("Start game")  # tady spustíš hru

                if settings_btn.collidepoint(mouse_pos):
                    print("Settings menu")

                if quit_btn.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

main_menu()
