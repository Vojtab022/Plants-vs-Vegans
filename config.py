import pygame

# Zjištění rozlišení monitoru pro odstranění černých pruhů (Widescreen podpora)
pygame.init()
info = pygame.display.Info()
monitor_w, monitor_h = info.current_w, info.current_h
aspect_ratio = monitor_w / monitor_h if monitor_h > 0 else 16/9

# --- NASTAVENÍ OBRAZOVKY A UI ---
VELIKOST_POLICKA = 60
FPS = 60
CURSOR_SKIN = "Zlatý kurzor" # Může být "Zlatý kurzor" nebo "Zelený kurzor"

# --- HLASITOST (0.0 až 1.0) ---
HLASITOST_HUDBY = 0.3
HLASITOST_EFEKTU = 0.5

# --- NASTAVENÍ HRÁČE A VLN ---
POCATECNI_PENIZE = 200
ODMENA_ZA_VLNU = 100

VLNA_SPAWN_INTERVAL = 2500     # Výchozí čas mezi spawny veganů v ms (2.5 sekundy)
VLNA_MIN_SPAWN_INTERVAL = 500  # Minimální čas mezi spawny (aby nechodili v sobě)
VLNA_ZRYCHLENI_SPAWNU = 200    # O kolik ms se zkrátí spawn interval s každou další vlnou
VLNA_START_VEGANU = 10         # Kolik veganů je v první vlně
VLNA_PRIRUSTEK_VEGANU = 5      # O kolik veganů víc má každá další vlna

# Mapa zůstává stejná
MAPA_LEVEL_1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
]

MAPA_LEVEL_2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 2],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

RADKU = len(MAPA_LEVEL_1)
VYSKA_MAPY = RADKU * VELIKOST_POLICKA

# Definice UI baru
VYSKA_UI = 100
VYSKA_OKNA = VYSKA_MAPY + VYSKA_UI

# Automatický výpočet sloupců pro zaplnění širokoúhlého monitoru
cilova_sirka = int(VYSKA_OKNA * aspect_ratio)
SLOUPCU = cilova_sirka // VELIKOST_POLICKA
if cilova_sirka % VELIKOST_POLICKA != 0:
    SLOUPCU += 1  # Zarovnání nahoru, ať nevzniknou pruhy

if SLOUPCU < len(MAPA_LEVEL_1[0]):
    SLOUPCU = len(MAPA_LEVEL_1[0]) # Pro jistotu, aby mapa nebyla menší než originál

SIRKA_OKNA = SLOUPCU * VELIKOST_POLICKA

# Doplnění map prázdným prostorem (trávou) na pravé straně
for radek in MAPA_LEVEL_1:
    while len(radek) < SLOUPCU:
        radek.append(0)
        
for radek in MAPA_LEVEL_2:
    while len(radek) < SLOUPCU:
        radek.append(0)

# --- BARVY ---
BARVA_TRAVY = (34, 139, 34)
BARVA_CESTY = (139, 69, 19)
BARVA_MRIZKY = (150, 150, 150, 80)
BARVA_UI_POZADI = (100, 100, 100)
BARVA_UI_VYBER = (255, 215, 0)

WAYPOINTY = [
    (30, 90), (150, 90), (150, 510), (390, 510), (390, 150), (510, 150),
    (510, 570), (690, 570), (690, 450), (990, 450), (990, 270), (750, 270),
    (750, 90), (1170, 90)
]
WAYPOINTY_LEVEL_2 = [
    (30, 90), (510, 90), (510, 210), (150, 210), (150, 510), (750, 510),
    (750, 210), (930, 210), (930, 450), (1170, 450)
]

AKTUALNI_MAPA = MAPA_LEVEL_1
AKTUALNI_WAYPOINTY = WAYPOINTY

# --- DEFINICE KYTEK ---
KYTKA_1_DATA = {
    "nazev": "Hrachostřel", "cena": 100, "barva": (0, 200, 0), "typ": "utocna", "dostřel": 150, "cooldown": 800, "poskozeni": 20, "ikona": "gfx/hrachstrel_IDLE.png"
}
KYTKA_2_DATA = {
    "nazev": "Studna", "cena": 50, "barva": (0, 150, 255), "typ": "ekonomicka", "cooldown": 8000, "vydelek": 5, "ikona": "gfx/well.png"
}
KYTKA_3_DATA = {
    "nazev": "Kaktus", "cena": 150, "barva": (0, 100, 0), "typ": "utocna", "dostřel": 400, "cooldown": 2500, "poskozeni": 60, "ikona": "gfx/Kaktus_IDLE.png"
}
SEZNAM_DOSTUPNYCH_KYTEK = [KYTKA_1_DATA, KYTKA_2_DATA, KYTKA_3_DATA]

# --- DEFINICE VEGANŮ ---
VEGAN_STREDNI_DATA = {
    "hp": 80, "rychlost": 2, "polomer": 18, "barva": (255, 128, 0)
}
VEGAN_RYCHLY_DATA = {
    "hp": 40, "rychlost": 4, "polomer": 22, "barva": (255, 255, 0)
}
VEGAN_TANK_DATA = {
    "hp": 250, "rychlost": 1, "polomer": 22, "barva": (139, 0, 0)
}
VEGAN_BOSS_DATA = {
    "hp": 2000, "rychlost": 0.8, "polomer": 35, "barva": (128, 0, 128)
}

# --- DEFINICE STŘEL ---
STRELA_HRY_DATA = {
    "rychlost": 6, "poskozeni": 15, "barva": (255, 215, 0), "velikost": 6
}