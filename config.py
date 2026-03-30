# (Ponechte vše, co v configu už máte, jen upravte tyto řádky:)

# --- UPRAVENO: NASTAVENÍ OBRAZOVKY A UI ---
VELIKOST_POLICKA = 60
FPS = 60

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

# Automatický výpočet velikosti MAPY
SLOUPCU = len(MAPA_LEVEL_1[0])
RADKU = len(MAPA_LEVEL_1)
SIRKA_OKNA = SLOUPCU * VELIKOST_POLICKA
VYSKA_MAPY = RADKU * VELIKOST_POLICKA # Původní VYSKA_OKNA

# !!! NOVÉ: Definice UI baru !!!
VYSKA_UI = 100 # Jak vysoký bude bar na kytky dole
VYSKA_OKNA = VYSKA_MAPY + VYSKA_UI # Celková výška okna

# --- NOVÉ: DEFINICE KYTEK (Sázení a UI) ---
# [Jméno, Cena, Barva (placeholder)]
# Časem tu přidáme ID textury, dostřel, poškození, atd.
KYTKA_1 = {"nazev": "Hrachostřel", "cena": 100, "barva": (0, 200, 0)}
KYTKA_2 = {"nazev": "Slunečnice", "cena": 50, "barva": (255, 255, 0)}

SEZNAM_DOSTUPNYCH_KYTEK = [KYTKA_1, KYTKA_2]

# (Zbytek configu - barvy a waypoints - ponechte)
# --- BARVY ---
BARVA_TRAVY = (34, 139, 34)
BARVA_CESTY = (139, 69, 19)
BARVA_MRIZKY = (0, 0, 0)
# Přidáme barvy pro UI
BARVA_UI_POZADI = (100, 100, 100) # Šedá
BARVA_UI_VYBER = (255, 215, 0)   # Zlatá pro vybranou kytku

# (Waypointy ponechte tak, jak jsou)
WAYPOINTY = [
    (30, 90),   # Start (vlevo)
    (150, 90),  # První zatáčka (dolů)
    (150, 510), # Druhá zatáčka (doprava)
    (390, 510), # Třetí zatáčka (nahoru)
    (390, 150), # Čtvrtá zatáčka (doprava)
    (510, 150), # Pátá zatáčka (dolů)
    (510, 570), # Šestá zatáčka (doprava)
    (690, 570)  # Konec cesty (cíl - sklad tofu)
]
# (Vše, co v configu máte, ponechte, jen upravte tyto sekce:)

# --- UPRAVENO: DEFINICE KYTEK (Podrobnější data) ---
# Cooldown je v milisekundách (1000ms = 1 vteřina)
KYTKA_1_DATA = {
    "nazev": "Hrachostřel",
    "cena": 100,
    "barva": (0, 200, 0),
    "typ": "utocna",
    "dostřel": 250, # radius v pixelech
    "cooldown": 800  # jak často střílí (ms)
}

KYTKA_2_DATA = {
    "nazev": "Slunečnice",
    "cena": 50,
    "barva": (255, 255, 0),
    "typ": "ekonomicka",
    "cooldown": 3000, # dává peníze každé 3 vteřiny
    "vydelek": 25     # kolik peněz dá
}

SEZNAM_DOSTUPNYCH_KYTEK = [KYTKA_1_DATA, KYTKA_2_DATA]

# --- NOVÉ: DEFINICE STŘEL (Projectiles) ---
STRELA_HRY_DATA = {
    "rychlost": 6,
    "poskozeni": 15,
    "barva": (255, 215, 0), # Zlatá kulička
    "velikost": 6
}