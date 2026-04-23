# --- NASTAVENÍ OBRAZOVKY A UI ---
VELIKOST_POLICKA = 60
FPS = 60
CURSOR_SKIN = "Zlatý kurzor" # Může být "Zlatý kurzor" nebo "Zelený kurzor"

# --- HLASITOST (0.0 až 1.0) ---
HLASITOST_HUDBY = 0.3
HLASITOST_EFEKTU = 0.5

# Mapa zůstává stejná
MAPA_LEVEL_1 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0],
    [1, 1, 1, 0, 0, 0, 0, 0, 0, 0,0,0],
    [0, 0, 1, 0, 0, 0, 1, 1, 1, 0,0,0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0,0,0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0,0,0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0,0,0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0,0,0],
    [0, 0, 1, 0, 0, 0, 1, 0, 1, 0,0,0],
    [0, 0, 1, 1, 1, 1, 1, 0, 1, 0,0,0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1,1,1]
]

MAPA_LEVEL_2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Automatický výpočet velikosti MAPY
SLOUPCU = len(MAPA_LEVEL_1[0])
RADKU = len(MAPA_LEVEL_1)
SIRKA_OKNA = SLOUPCU * VELIKOST_POLICKA
VYSKA_MAPY = RADKU * VELIKOST_POLICKA

# Definice UI baru
VYSKA_UI = 100
VYSKA_OKNA = VYSKA_MAPY + VYSKA_UI

# --- BARVY ---
BARVA_TRAVY = (34, 139, 34)
BARVA_CESTY = (139, 69, 19)
BARVA_MRIZKY = (0, 0, 0)
BARVA_UI_POZADI = (100, 100, 100)
BARVA_UI_VYBER = (255, 215, 0)

WAYPOINTY = [(30, 90), (150, 90), (150, 510), (390, 510), (390, 150), (510, 150), (510, 570), (690, 570)]
WAYPOINTY_LEVEL_2 = [(30, 90), (510, 90), (510, 210), (150, 210), (150, 330), (510, 330), (510, 450), (150, 450), (150, 570), (690, 570)]

AKTUALNI_MAPA = MAPA_LEVEL_1
AKTUALNI_WAYPOINTY = WAYPOINTY

# --- DEFINICE KYTEK ---
KYTKA_1_DATA = {
    "nazev": "Hrachostřel", "cena": 100, "barva": (0, 200, 0), "typ": "utocna", "dostřel": 250, "cooldown": 800
}
KYTKA_2_DATA = {
    "nazev": "Slunečnice", "cena": 50, "barva": (255, 255, 0), "typ": "ekonomicka", "cooldown": 3000, "vydelek": 25
}
SEZNAM_DOSTUPNYCH_KYTEK = [KYTKA_1_DATA, KYTKA_2_DATA]

# --- DEFINICE STŘEL ---
STRELA_HRY_DATA = {
    "rychlost": 6, "poskozeni": 15, "barva": (255, 215, 0), "velikost": 6
}