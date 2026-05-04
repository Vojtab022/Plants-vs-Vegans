import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, base_color, hover_color, text_color=(255, 255, 255), icon=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.icon = icon

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        # Pokud je myš nad tlačítkem, použije se barva pro hover
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.base_color
        
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2) # Přidáme pěkný bílý okraj
        
        # Podpora pro více řádků (rozdělení pomocí \n)
        lines = self.text.split('\n')
        line_height = self.font.get_height()
        total_height = line_height * len(lines)
        start_y = self.rect.centery - (total_height // 2)
        
        text_start_x = self.rect.centerx
        
        if self.icon:
            # Vykreslení ikonky na levé straně
            icon_rect = self.icon.get_rect(midleft=(self.rect.left + 5, self.rect.centery))
            screen.blit(self.icon, icon_rect)
            
            # Posunutí středu textu doprava
            zbyle_misto_x = self.rect.left + 5 + self.icon.get_width()
            zbyle_misto_sirka = self.rect.width - 5 - self.icon.get_width()
            text_start_x = zbyle_misto_x + (zbyle_misto_sirka // 2)

        for i, line in enumerate(lines):
            label = self.font.render(line, True, self.text_color)
            text_rect = label.get_rect(center=(text_start_x, start_y + i * line_height + (line_height // 2)))
            screen.blit(label, text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)