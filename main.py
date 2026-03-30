import pygame
import sys
import os
import config

from vegans.zakladni_vegan import ZakladniVegan 
# !!! NOVÉ !!! Importujeme specifické kytky místo základní
from plants.hrachostrel import Hrachostrel
from plants.slunecnice import Slunecnice

pygame.init()
screen = pygame.display.set_mode((config.SIRKA_OKNA, config.VYSKA_OKNA))
pygame.display.set_caption("Plants vs. Vegans - Střílení a Ekonomika")
clock = pygame.time.Clock()

# --- 1. HERNÍ DATA ---
seznam_veganu = []
prvni_vegan = ZakladniVegan(config.WAYPOINTY)
seznam_veganu.append(prvni_vegan)

seznam_kytek = []
seznam_strel = [] # !!! NOVÉ !!! Seznam střel
seznam_obsazenych_policek = []

vybrany_typ_kytky_data = None 
penize = 200 

font_ui = pygame.font.SysFont("Arial", 20, bold=True)


# --- HLAVNÍ HERNÍ SMYČKA ---
running = True
while running:
    # A) Zpracování událostí
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # --- Část 1: Sázení ---
            if mouse_y < config.VYSKA_MAPY:
                grid_x = mouse_x // config.VELIKOST_POLICKA
                grid_y = mouse_y // config.VELIKOST_POLICKA
                
                if vybrany_typ_kytky_data is not None:
                    if config.MAPA_LEVEL_1[grid_y][grid_x] == 0 and (grid_x, grid_y) not in seznam_obsazenych_policek:
                        if penize >= vybrany_typ_kytky_data["cena"]:
                            penize -= vybrany_typ_kytky_data["cena"]
                            
                            # !!! NOVÉ: Vytváříme objekt podle typu kytky !!!
                            if vybrany_typ_kytky_data["typ"] == "utocna":
                                nova_kytka = Hrachostrel(grid_x, grid_y)
                            elif vybrany_typ_kytky_data["typ"] == "ekonomicka":
                                nova_kytka = Slunecnice(grid_x, grid_y)
                                
                            seznam_kytek.append(nova_kytka)
                            seznam_obsazenych_policek.append((grid_x, grid_y))
                            vybrany_typ_kytky_data = None 
            
            # --- Část 2: Výběr UI (Používáme KYTKA_x_DATA z configu) ---
            else:
                ui_y = mouse_y - config.VYSKA_MAPY
                if 10 < mouse_x < 160 and 10 < ui_y < 90:
                    vybrany_typ_kytky_data = config.KYTKA_1_DATA # !!! UPRAVENO !!!
                if 170 < mouse_x < 320 and 10 < ui_y < 90:
                    vybrany_typ_kytky_data = config.KYTKA_2_DATA # !!! UPRAVENO !!!


    # B) Aktualizace a Logika (!!! Zásadní změny !!!)
    
    # 1. Aktualizace kytky (střílení a generování peněz)
    for kytka in seznam_kytek:
        # Peníze se aktualizují jen pokud je kytka Slunečnice a generuje
        nove_penize = kytka.update(seznam_veganu, seznam_strel, penize)
        if nove_penize is not None: penize = nove_penize

    # 2. Aktualizace střel a kolize
    for strela in seznam_strel:
        strela.update()
        
        # --- KOLIZE: Střela vs Vegani ---
        for vegan in seznam_veganu:
            # Vypočítáme vzdálenost kuličky od středu vegana
            dist = strela.pozice.distance_to(vegan.pozice)
            # Pokud je menší než poloměr vegana (15px), trefili jsme ho!
            if dist < 15:
                # Ubereme zdraví veganovi
                vegan.hp -= config.STRELA_HRY_DATA["poskozeni"]
                strela.je_ziva = False # Střela zmizí
                print(f"Hit! HP vegana: {vegan.hp}")
                
    # 3. Odstranění "mrtvých" objektů
    # Odstraníme střely, které narazily nebo vyletěly
    for i in range(len(seznam_strel) - 1, -1, -1):
        if not seznam_strel[i].je_ziva:
            seznam_strel.pop(i)
            
    # Odstraníme vegany, kteří nemají zdraví
    for i in range(len(seznam_veganu) - 1, -1, -1):
        if seznam_veganu[i].hp <= 0:
            seznam_veganu.pop(i)
            print("Vegan byl poražen!")
            
    # Aktualizace pohybu zbylých veganů
    for vegan in seznam_veganu: vegan.move()


    # C) Vykreslení
    # (Vykreslení mapy barevnými čtverci ponechte)
    for radek_index in range(config.RADKU):
        for sloupec_index in range(config.SLOUPCU):
            cislo_policka = config.MAPA_LEVEL_1[radek_index][sloupec_index]
            x = sloupec_index * config.VELIKOST_POLICKA
            y = radek_index * config.VELIKOST_POLICKA
            if cislo_policka == 0: barva = config.BARVA_TRAVY
            elif cislo_policka == 1: barva = config.BARVA_CESTY
            pygame.draw.rect(screen, barva, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA))
            pygame.draw.rect(screen, config.BARVA_MRIZKY, (x, y, config.VELIKOST_POLICKA, config.VELIKOST_POLICKA), 1)

    # Vykreslení objektů
    for kytka in seznam_kytek: kytka.draw(screen)
    for strela in seznam_strel: strela.draw(screen) # !!! NOVÉ !!!
    for vegan in seznam_veganu: vegan.draw(screen)
        
    # Vykreslení UI
    ui_pozadi_rect = (0, config.VYSKA_MAPY, config.SIRKA_OKNA, config.VYSKA_UI)
    pygame.draw.rect(screen, config.BARVA_UI_POZADI, ui_pozadi_rect)
    penize_text = font_ui.render(f"Peníze: ${penize}", True, (255, 255, 255))
    screen.blit(penize_text, (config.SIRKA_OKNA - 150, config.VYSKA_MAPY + 10))
    for i, data in enumerate(config.SEZNAM_DOSTUPNYCH_KYTEK):
        btn_x = 10 + (i * 160)
        btn_y = config.VYSKA_MAPY + 10
        btn_width = 150
        btn_height = 80
        btn_rect = (btn_x, btn_y, btn_width, btn_height)
        if vybrany_typ_kytky_data is not None and vybrany_typ_kytky_data["nazev"] == data["nazev"]:
            pygame.draw.rect(screen, config.BARVA_UI_VYBER, (btn_x - 3, btn_y - 3, btn_width + 6, btn_height + 6), 3)
        pygame.draw.rect(screen, data["barva"], btn_rect)
        pygame.draw.rect(screen, (0,0,0), btn_rect, 2)
        text_name = font_ui.render(data["nazev"], True, (0, 0, 0))
        text_price = font_ui.render(f"${data['cena']}", True, (0, 0, 0))
        screen.blit(text_name, (btn_x + 10, btn_y + 10))
        screen.blit(text_price, (btn_x + 10, btn_y + 40))

    pygame.display.flip()
    clock.tick(config.FPS)

pygame.quit()
sys.exit()