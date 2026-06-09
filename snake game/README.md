# SINU-MODE Ussimäng 🐍

**Autor:** Mikk-Gregor  
**Kursus:** Programmeerimise alused  
**Teek:** Python + PyGame

---

## Projekti kirjeldus

SINU-MODE on kohandatud ussimäng, mis on loodud kolme erineva avaliku ussimängu koodist.  
Lähtepunktiks valiti `minu_tehtud_mang/sinu_mode.py` (OOP struktuur test_1 põhjal), millesse integreeriti ideid ja koodiosi test_2 ja test_3 failidest.

---

## Testitud lähtemängud

| # | Fail | Allikas | Kirjeldus |
|---|------|---------|-----------|
| 1 | `test 1.py` | [TechWithTim / GitHub](https://github.com/techwithtim/Snake-Game) | OOP `cube`/`snake` klassid, silmade joonistamine, ruudustik |
| 2 | `test 2.py` | [rajatdiptabiswas / GitHub](https://github.com/rajatdiptabiswas/snake-pygame) | Difficulty süsteem, nooleklahvid + WASD, game-over stiil |
| 3 | `test 3.py` | [MA-Abahmane / GitHub](https://github.com/MA-Abahmane/Python-Python) | Tkinter/Pygame hybrid, toiduemoji stiil, heli ideed |

**Valiku põhjendus:** `sinu_mode.py` (test_1 baas) on valitud lähtepunktiks, kuna:
- OOP struktuur on hästi laiendatav
- Ruudustiku loogika toimib täpsemalt kui test_2 pixel-põhine lähenemine
- Lihtsam lisada uusi funktsioone (elud, toidutüübid) ilma kogu struktuuri muutmata

---

## Parendused (5 tk)

### Parendus 1 — Kolm toidutüüpi
**Kirjeldus:** Lisati kolm erinevat toidutüüpi erineva käitumisega.
- 🔴 **Tavaline** (+1 punkt) — punane ruut, püsib ekraanil
- 🟡 **Boonus** (+3 punkti) — kuldne, vilgub sinuslainena, kaob 120 kaadri pärast
- 🟣 **Mürk** (−1 elu) — lilla X-märgiga, kaob samuti aja pärast

**Tõenäosused:** 70% tavaline / 20% boonus / 10% mürk  
**Tehniline lahendus:** `Toit._vali_tyyp()`, `Toit.joonista()` animatsioon `pygame.SRCALPHA` abil

**Probleem:** Alpha-kihi rakendamine nõudis eraldi `Surface` objekti loomist, kuna `pygame.draw.rect` ei toeta otse RGBA värve.  
**Lahendus:** `pygame.Surface(..., pygame.SRCALPHA)` + `surf.blit()`

---

### Parendus 2 — 3 elu süsteem
**Kirjeldus:** Mängijal on 3 elu. Elu kaotus (sein, iseendaga, mürk) lähtestab ussi, mitte kogu mängu. Elud on kujutatud punaste ringidena ekraani paremas ülanurgas.

**Tehniline lahendus:** `elud` muutuja, `Uss.reset()` kutsumine elu kaotuse korral.  
**Mõju mängitavusele:** Mäng on vähem frustreeriv — üks viga ei lõpeta kõike.

**Probleem:** Reset pidi säilitama skoori ja kiiruse, aga uss pidi alustama alguspositsioonilt.  
**Lahendus:** Ainult `uss.reset()` kutsutakse, skoor/kiirus jäävad muutmata.

---

### Parendus 3 — Suundtundlikud silmad
**Kirjeldus:** Ussi pea joonistab silmad liikumissuuna poole — 4 suunda (üles, alla, vasak, parem).

**Tehniline lahendus:** `Kuup.joonista()` kontrollib `self.suund_x` ja `self.suund_y` ning valib silmade koordinaadid vastavalt.  
**Allikas:** Inspireeritud test_1 `cube.draw(eyes=True)` loogikast.

**Probleem:** Algul olid silmad alati paremal pool olenemata suunast.  
**Lahendus:** `if self.suund_x == 1 / -1 / elif self.suund_y == -1 / else` haru.

---

### Parendus 4 — Difficulty valik + live muutmine
**Kirjeldus:** Start-ekraanil saab nooleklahvidega valida 4 raskusastet. Mängu ajal saab klahvidega 1-4 kiirust reaalajas muuta.

| Klahv | Nimi | FPS |
|-------|------|-----|
| 1 | Lihtne | 6 |
| 2 | Keskmine | 10 |
| 3 | Raske | 15 |
| 4 | Hull | 22 |

**Allikas:** test_2 `difficulty` konstant, laiendatud dünaamiliseks muutmiseks.  
**Tehniline lahendus:** `kell.tick(kiirus)` — muudetav `kiirus` muutuja.

---

### Parendus 5 — Animatsioonid, paus ja seansi rekord
**Kirjeldus:**
- **Start-ekraan:** "SINU-MODE" tiitel hõljub üles-alla sinuslainena
- **Game-over:** tekst pulseerib punasena
- **Paus (P-klahv):** poolläbipaistev overlay, mäng jääb seisma
- **Rekord:** `parim_skoor` säilib terve seansi vältel mängude vahel

**Tehniline lahendus:** `math.sin(tick * konstant)` annab sujuva animatsiooni; `pygame.SRCALPHA` pausioverlay jaoks.

**Probleem:** Rekord lähtestus iga mängu algul.  
**Lahendus:** `parim_skoor` on globaalne muutuja, mida uuendatakse ainult kui `skoor > parim_skoor`.

---

## Käivitamine

### Eeltingimused
```bash
pip install pygame
```

### Käivitamine
```bash
python sinu_mode.py
```

### Klahvid
| Klahv | Tegevus |
|-------|---------|
| ↑↓←→ / WASD | Ussi suunamine |
| 1 / 2 / 3 / 4 | Kiiruse muutmine |
| P | Paus sisse/välja |
| ESC / Q | Välju mängust |
| C (game-over) | Mängi uuesti |

---

## Projekti struktuur

```
sinu_mode_projekt/
├── sinu_mode.py      # Põhimäng (täielikult eestikeelsete kommentaaridega)
├── README.md         # Dokumentatsioon (see fail)
snakegame/
├── minu_esimene_test/
│   ├── test 1.py     # TechWithTim — OOP lähtevers
│   └── README.txt
├── minu_teine_test/
│   ├── test 2.py     # rajatdiptabiswas — difficulty süsteem
│   └── README.txt
├── minu_kolmas_test/
│   ├── test 3.py     # MA-Abahmane — Tkinter hybrid
│   └── README.txt
└── minu_tehtud_mang/
    └── sinu_mode.py  # Eelmine versioon (lähtepunkt)
```

---

## Teostatud tööd kokkuvõtlikult

1. Uuritud ja testitud 3 erinevat ussimängu (test_1, test_2, test_3)
2. Valitud parim lähtepunkt (OOP struktuur test_1/sinu_mode baasil)
3. Integreeritud difficulty süsteem test_2-st
4. Lisatud 5 originaalparendust (toidutüübid, elud, silmad, animatsioonid, rekord)
5. Kõik koodiread kommenteeritud eesti keeles
6. Dokumenteeritud probleemid ja lahendused README-s

---

## GitHub

Kogu projekt on kättesaadav GitHubis (lae üles oma repositooriumi):  
`git init && git add . && git commit -m "SINU-MODE ussimang - loplik versioon" && git push`

---

*SINU-MODE Ussimäng — Mikk-Gregor Edition*
