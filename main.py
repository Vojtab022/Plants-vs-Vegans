import pygame
import sys
import os
import config

from vegans.zakladni_vegan import ZakladniVegan 
# !!! NOVÉ !!! Importujeme specifické kytky místo základní
from plants.hrachostrel import Hrachostrel
from plants.slunecnice import Slunecnice

def start_game():
    pygame.init()
    screen = pygame.display.set_mode((config.SIRKA_OKNA, config.VYSKA_OKNA))
    pygame.display.set_caption("Plants vs Vegans")
    clock = pygame.time.Clock()

    # --- 1. HERNÍ DATA ---
    seznam_veganu = []
    # --- NOVÉ: SYSTÉM PRO VLNY NEPŘÁTEL ---
    cas_posledniho_spawnu = pygame.time.get_ticks()
    SPAWN_INTERVAL = 2500 # Každých 2.5 vteřiny (2500 ms) přijde nový vegan
    celkem_vygenerovano = 0
    MAX_VEGANU_VE_VLNE = 10 # Vlna skončí po 10 veganech

    seznam_kytek = []
    seznam_strel = [] # !!! NOVÉ !!! Seznam střel
    seznam_obsazenych_policek = []

    vybrany_typ_kytky_data = None 
    penize = 200 

    font_ui = pygame.font.SysFont("Arial", 20, bold=True)

    # --- TLAČÍTKA PRO PAUSE MENU ---
    btn_w, btn_h = 200, 60
    stred_x = config.SIRKA_OKNA // 2 - btn_w // 2
    continue_btn = pygame.Rect(stred_x, 200, btn_w, btn_h)
    settings_btn = pygame.Rect(stred_x, 280, btn_w, btn_h)
    main_menu_btn = pygame.Rect(stred_x, 360, btn_w, btn_h)
    
    font_pause = pygame.font.SysFont("Arial", 60, bold=True)
    paused = False
    pause_start_cas = 0

    # --- HLAVNÍ HERNÍ SMYČKA ---
    running = True
    while running:
        # A) Zpracování událostí
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Pokud hráč klikne na křížek, vrací se do menu
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not paused:
                        paused = True
                        pause_start_cas = pygame.time.get_ticks()
                    else:
                        paused = False
                        # Po pauze posuneme časovače, aby hra nenagenerovala vše naráz
                        posun = pygame.time.get_ticks() - pause_start_cas
                        cas_posledniho_spawnu += posun
                        for kytka in seznam_kytek:
                            kytka.posledni_akce_cas += posun
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                if paused:
                    if continue_btn.collidepoint(mouse_x, mouse_y):
                        paused = False
                        posun = pygame.time.get_ticks() - pause_start_cas
                        cas_posledniho_spawnu += posun
                        for kytka in seznam_kytek:
                            kytka.posledni_akce_cas += posun
                    elif settings_btn.collidepoint(mouse_x, mouse_y):
                        import menu
                        menu.screen = screen # Předáme menu.py naše aktuální herní okno
                        menu.settings_menu()
                    elif main_menu_btn.collidepoint(mouse_x, mouse_y):
                        running = False # Ukončí herní smyčku, vrací se do menu
                else:
                    # --- Část 1: Sázení ---
                    if mouse_y < config.VYSKA_MAPY:
                        grid_x = mouse_x // config.VELIKOST_POLICKA
                        grid_y = mouse_y // config.VELIKOST_POLICKA
                        
                        if vybrany_typ_kytky_data is not None:
                            if config.AKTUALNI_MAPA[grid_y][grid_x] == 0 and (grid_x, grid_y) not in seznam_obsazenych_policek:
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
                    
                    # --- Část 2: Výběr UI (Dynamický systém ze seznamu) ---
                    else:
                        for i, data in enumerate(config.SEZNAM_DOSTUPNYCH_KYTEK):
                            btn_x = 10 + (i * 160)
                            btn_y = config.VYSKA_MAPY + 10
                            btn_width = 150
                            btn_height = 80
                            btn_rect = pygame.Rect(btn_x, btn_y, btn_width, btn_height)
                            
                            if btn_rect.collidepoint(mouse_x, mouse_y):
                                vybrany_typ_kytky_data = data

        # B) Aktualizace a Logika (!!! Zásadní změny !!!)
        if not paused:
            nyni = pygame.time.get_ticks()
            
            # --- NOVÉ: Spawnování veganů ---
            # Pokud uběhl dostatek času a ještě jsme nevyčerpali limit vlny
            if nyni - cas_posledniho_spawnu > SPAWN_INTERVAL and celkem_vygenerovano < MAX_VEGANU_VE_VLNE:
                novy_vegan = ZakladniVegan(config.AKTUALNI_WAYPOINTY)
                seznam_veganu.append(novy_vegan)
                
                cas_posledniho_spawnu = nyni
                celkem_vygenerovano += 1
                print(f"Pozor! Na mapu vstoupil vegan číslo {celkem_vygenerovano}!")
            
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
            # Používáme rychlé přepsání listu místo pop() pro vyšší výkon
            seznam_strel = [strela for strela in seznam_strel if strela.je_ziva]
                    
            zivi_vegani = []
            for vegan in seznam_veganu:
                if vegan.hp > 0:
                    zivi_vegani.append(vegan)
                else:
                    print("Vegan byl poražen!")
            seznam_veganu = zivi_vegani
                    
            # Aktualizace pohybu zbylých veganů
            for vegan in seznam_veganu: vegan.move()

        # C) Vykreslení
        # (Vykreslení mapy barevnými čtverci ponechte)
        for radek_index in range(config.RADKU):
            for sloupec_index in range(config.SLOUPCU):
                cislo_policka = config.AKTUALNI_MAPA[radek_index][sloupec_index]
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

        # --- VYKRESLENÍ PAUSE MENU OVERLAY ---
        if paused:
            # Poloprůhledné pozadí
            s = pygame.Surface((config.SIRKA_OKNA, config.VYSKA_OKNA), pygame.SRCALPHA)
            s.fill((0, 0, 0, 160)) # Černá se slušnou průhledností
            screen.blit(s, (0, 0))

            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Hover efekt pro tlačítka
            barva_cont = (0, 200, 0) if continue_btn.collidepoint(mouse_x, mouse_y) else (0, 150, 0)
            barva_set = (0, 200, 0) if settings_btn.collidepoint(mouse_x, mouse_y) else (0, 150, 0)
            barva_menu = (0, 200, 0) if main_menu_btn.collidepoint(mouse_x, mouse_y) else (0, 150, 0)

            pygame.draw.rect(screen, barva_cont, continue_btn)
            pygame.draw.rect(screen, barva_set, settings_btn)
            pygame.draw.rect(screen, barva_menu, main_menu_btn)

            pygame.draw.rect(screen, (255, 255, 255), continue_btn, 2)
            pygame.draw.rect(screen, (255, 255, 255), settings_btn, 2)
            pygame.draw.rect(screen, (255, 255, 255), main_menu_btn, 2)

            # Texty tlačítek (vycentrované)
            lbl_cont = font_ui.render("Continue", True, (255, 255, 255))
            lbl_set = font_ui.render("Settings", True, (255, 255, 255))
            lbl_menu = font_ui.render("Main Menu", True, (255, 255, 255))

            screen.blit(lbl_cont, (continue_btn.x + continue_btn.width//2 - lbl_cont.get_width()//2, continue_btn.y + continue_btn.height//2 - lbl_cont.get_height()//2))
            screen.blit(lbl_set, (settings_btn.x + settings_btn.width//2 - lbl_set.get_width()//2, settings_btn.y + settings_btn.height//2 - lbl_set.get_height()//2))
            screen.blit(lbl_menu, (main_menu_btn.x + main_menu_btn.width//2 - lbl_menu.get_width()//2, main_menu_btn.y + main_menu_btn.height//2 - lbl_menu.get_height()//2))

            # Nadpis
            lbl_pause = font_pause.render("PAUSED", True, (255, 255, 255))
            screen.blit(lbl_pause, (config.SIRKA_OKNA//2 - lbl_pause.get_width()//2, 80))

        pygame.display.flip()
        clock.tick(config.FPS)

# Záchranná brzda - kód se spustí jen tehdy, pokud je main.py spuštěn přímo (a nikoliv importován z menu.py)
if __name__ == "__main__":
    # Pokud hráč omylem spustí main.py, přesměrujeme ho do menu
    print("Přesměrování do hlavního menu...")
    import menu
    menu.main_menu()