import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, text_color=(255, 255, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        # Pokud je myš nad tlačítkem, použije se barva pro hover
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2) # Přidáme pěkný bílý okraj
        
        label = self.font.render(self.text, True, self.text_color)
        text_rect = label.get_rect(center=self.rect.center)
        screen.blit(label, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)