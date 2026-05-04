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

ZakladniKytka
Dědí z: Ničeho (je to "praotec" kytek).
Používá se v: Nikdy ji nestavíš do hry přímo, jen z ní tvoříš další kytky.
Co dělá a proč tu je: Říká: "Každá kytka má souřadnice (x, y), nějaký obrázek a umí se nakreslit." Je tu proto, abys nemusel u každé nové kytky psát znovu kód pro kreslení na obrazovku.

Hrachostrel / Kaktus / Studna
Dědí ze: ZakladniKytka (berou si od ní kreslení a souřadnice).
Používá se v: main.py (když si je hráč koupí a položí na mapu).
Co dělají a proč tu jsou: Přidávají konkrétní chování. Hrachostřel střílí často, Kaktus na dálku a silně, Studna místo střílení dává peníze.

ZakladniVegan
Dědí z: Ničeho ("praotec" nepřátel).
Používá se v: Jen z něj tvoříš další nepřátele.
Co dělá a proč tu je: Říká: "Každý nepřítel umí chodit po cestě, má nějaké životy (HP) a kreslí se nad ním červeno-zelený pruh zdraví." Je tu proto, aby uměl sám chodit a umírat a tys to nemusel programovat u každého nepřítele zvlášť.

StredniVegan / RychlyVegan / TankVegan / BossVegan
Dědí ze: ZakladniVegan.
Používá se v: wave_manager.py (když se do hry posílá nová vlna).
Co dělají a proč tu jsou: Jen si mění čísla. Rychlý běží jak blázen, Boss je hrozně pomalý a nejde ho skoro zabít. Jsou tu pro zábavnost a rozdílnou obtížnost.

HerniAplikace
Dědí z: Ničeho.
Používá se v: Úplně na konci main.py jako spouštěč celého programu.
Co dělá a proč tu je: Přepíná mezi Menu a samotnou Hrou. Je tu proto, aby hra po kliknutí na "Play" nespadla, ale plynule se přepnula do hraní.

PlantsVsVegansGame
Dědí z: Ničeho.
Používá se v: Volá ji HerniAplikace.
Co dělá a proč tu je: To je hlavní smyčka (srdce hry). Běží 60x za vteřinu, hlídá klikání myší, říká kytkám ať střílí a střelám ať letí.

HerniMapa
Dědí z: Ničeho.
Používá se v: main.py (pro vykreslení pozadí).
Co dělá a proč tu je: Skládá cestičky, rohy, trávu a mřížku pro stavění. Je oddělená proto, abys v hlavním kódu neměl bordel ze stovek řádků o tom, jak se otáčí obrázek trávy.

WaveManager
Dědí z: Ničeho.
Používá se v: main.py (v hlavní smyčce).
Co dělá a proč tu je: Režisér hry. Hlídá si stopky a říká: "Uběhly dvě vteřiny, pošli tam Rychlého Vegana."

Hrac
Dědí z: Ničeho.
Používá se v: V hlavní smyčce (při nákupu) a ve studně (při výdělku).
Co dělá a proč tu je: Peněženka. Hlídá, jestli máš dost peněz na nákup. Je super ho mít zvlášť, aby peníze nebyly chaoticky rozházené po celé hře.

Strela
Dědí z: Ničeho.
Používá se v: V kytkách (ty ji vytvoří) a v main.py (tam letí a zabíjí).
Co dělá a proč tu je: Je to fyzický letící náboj, který jako "střela s plochou dráhou letu" pronásleduje svůj cíl, dokud ho nezasáhne.

Button
Dědí z: Ničeho.
Používá se v: Naprosto všude, kde se na něco kliká (Menu, UI hry, Game Over).
Co dělá a proč tu je: Klikací tlačítko, které změní barvu, když na něj najedeš myší. Je tu proto, abys tohle nemusel kódovat pro každé tlačítko znova.