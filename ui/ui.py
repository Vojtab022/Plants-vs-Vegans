import pygame

class Button:
    def __init__(self, x, y, sirka, vyska, text, font, zakladni_barva, hover_barva, icon=None):
        self.rect = pygame.Rect(x, y, sirka, vyska)
        self.text = text
        self.font = font
        self.zakladni_barva = zakladni_barva
        self.hover_barva = hover_barva
        self.icon = icon

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Vytvoříme průhledný povrch pro tlačítko, aby mohl prosvítat background
        surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        
        # Zvolíme barvu podle toho, jestli na něm myš je nebo ne
        barva = self.hover_barva if is_hovered else self.zakladni_barva
        
        # Pokud je barva zadána jen jako RGB (3 hodnoty), přidáme alfa kanál (průhlednost 210)
        if len(barva) == 3:
            rgba_barva = (*barva, 210) 
        else:
            rgba_barva = barva
            
        # Vykreslíme zakulacené tlačítko (border_radius = 15)
        pygame.draw.rect(surface, rgba_barva, surface.get_rect(), border_radius=15)
        
        # Když najedeme myší, přidáme navíc zřetelný bílý rámeček
        if is_hovered:
            pygame.draw.rect(surface, (255, 255, 255, 255), surface.get_rect(), width=3, border_radius=15)

        # Vykreslíme výsledný povrch na skutečnou obrazovku
        screen.blit(surface, self.rect.topleft)

        # --- TEXT A IKONA ---
        # 1. Vykreslíme ikonu, pokud existuje
        text_start_x = self.rect.left + 15 # Výchozí odsazení textu
        if self.icon:
            icon_rect = self.icon.get_rect(centery=self.rect.centery, left=self.rect.left + 15)
            screen.blit(self.icon, icon_rect)
            text_start_x = icon_rect.right + 10 # Posuneme text za ikonu

        # 2. Vykreslíme text (s podporou více řádků)
        lines = self.text.split('\n')
        line_height = self.font.get_linesize()
        total_text_height = len(lines) * line_height
        start_y = self.rect.centery - total_text_height / 2

        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, (255, 255, 255))
            text_shadow_surf = self.font.render(line, True, (0, 0, 0))
            
            # Zarovnání textu: pokud je ikona, zarovnáme vlevo k ikoně, jinak plně na střed
            if self.icon:
                text_x = text_start_x
            else:
                text_x = self.rect.centerx - text_surf.get_width() / 2

            # Stín textu
            shadow_pos = (text_x + 2, start_y + i * line_height + 2)
            screen.blit(text_shadow_surf, shadow_pos)

            # Hlavní text
            text_pos = (text_x, start_y + i * line_height)
            screen.blit(text_surf, text_pos)

    def is_clicked(self, mouse_pos):
        # Kontrola, zda bylo na tlačítko kliknuto
        return self.rect.collidepoint(mouse_pos)
