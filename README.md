# Plants vs Vegans

Zábavná Tower Defense hra naprogramovaná v Pythonu pomocí knihovny Pygame. Braňte svou zahradu před nájezdy hladových veganů pomocí strategicky rozmístěných rostlin!

## 🌟 Vlastnosti hry

* **Více druhů rostlin:**
  * **Hrachostřel:** Rychlá základní útočná jednotka.
  * **Kaktus:** Pomalý, ale silný sniper s obrovským dostřelem a velkým poškozením.
  * **Studna:** Ekonomická budova, která pravidelně generuje peníze.
* **Různí nepřátelé (Vegani):** Setkáte se se standardním veganem, rychlíkem, obrněným tankem i obřím Bossem.
* **Systém vln:** Hra postupně zvyšuje obtížnost. Nepřátelé chodí ve vlnách, za jejichž přežití získáváte bonusové finance.
* **Ekonomika:** Začínáte s počátečním obnosem, rostliny nakupujete a můžete je v případě potřeby za poloviční cenu zase prodat.
* **Více úrovní:** Hra obsahuje Level 1 a Level 2 se specifičtější trasou.
* **Nastavení:** Možnost úpravy hlasitosti hudby/efektů, změny kurzoru myši a přepínání FPS (30/60).

## 🎮 Ovládání

* **Levé tlačítko myši:** Veškerá interakce. Výběr v menu, nákup rostlin ve spodním panelu, pokládání rostlin na mapu i jejich prodej.
* **ESC:** Pozastavení hry (Pauza).

## 🚀 Instalace a spuštění

Hra je zabalena jako samostatný spustitelný program pro Windows, takže nepotřebujete instalovat Python ani žádné další knihovny.

1. Stáhněte a rozbalte složku s hrou.
2. Dvojitým kliknutím spusťte soubor `PlantsVsVegans.exe`.
3. Bavte se!

## 🏗 Architektura projektu

Projekt je napsán s velkým důrazem na **čisté Objektově Orientované Programování**. Herní entity a systémy jsou odděleny do specializovaných tříd a balíčků:

* `main.py` & `HerniAplikace`: Hlavní smyčka a State Manager.
* `mapa.py`: Modul starající se o automatické generování zatáček na cestě a vykreslování mapy.
* `wave_manager.py`: Řídí vlny a spawnování nepřátel.
* `plants/`: Balíček obsahující základní třídu `ZakladniKytka` a její potomky.
* `vegans/`: Balíček obsahující základní třídu `ZakladniVegan` a definice jednotlivých nepřátel.
* `projectiles/`: Balíček obsahující třídu pro automaticky naváděné střely (`Homing`).
* `ui.py`: Modul pro interaktivní tlačítka s podporou více řádků a ikon.