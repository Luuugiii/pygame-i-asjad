"""
SINU-MODE Ussimäng
=====================================
Autor:    Mikk-Gregor
Kursus:   Tarkvaraarenduse projekt
Fail:     sinu_mode.py

Lähtepunkt: minu_tehtud_mang/sinu_mode.py (OOP klass-struktuur test_1 põhjal)
Integreeritud koodist:
  • test 1.py (TechWithTim)  — cube/snake OOP klassid, silmade joonistamine
  • test 2.py (rajatdiptabiswas) — difficulty süsteem, nooleklahvid + WASD, mängutsükkel
  • test 3.py (MA-Abahmane)  — Tkinter/Pygame hybrid ideed, toiduemoji stiil

PARENDUSED (5 tk):
  1. Kolm toidutüüpi: tavaline (+1), boonus (+3, vilgub), mürk (−1 elu)
  2. 3-elu süsteem — uss lähtestub, mäng ei lõpe kohe
  3. Pea joonistamine suundtundlike silmadega (test_1 stiil)
  4. Difficulty valik start-ekraanil + live muutmine klahvidega 1-4 (test_2 stiil)
  5. Animeeritud start-/game-over-ekraan + paus (P) + seansi rekord
"""

# ── teegid ────────────────────────────────────────────────────────────────────
import pygame   # graafikateek mängu joonistamiseks
import random   # juhuslike koordinaatide ja toidutüüpide genereerimiseks
import sys      # programmist väljumiseks sys.exit() kaudu
import math     # siinus-laine arvutamiseks animatsioonides

# ── pygame käivitus ───────────────────────────────────────────────────────────
pygame.init()   # lähtestab kõik pygame'i moodulid (graafika, klahvid jne)

# ── akna seaded ───────────────────────────────────────────────────────────────
LAIUS  = 800    # mänguakna laius pikslites
KORGUS = 600    # mänguakna kõrgus pikslites
PLOKI  = 20     # ühe ruudustikuploki suurus (uss liigub sammuga PLOKI pikselit)

# loo mänguaken ja määra pealkiri
ekraan = pygame.display.set_mode((LAIUS, KORGUS))
pygame.display.set_caption("SINU-MODE Ussimäng")

# kellaobjekti framerate piiramiseks
kell = pygame.time.Clock()

# ── värvikonstantid (R, G, B) ─────────────────────────────────────────────────
TAUST       = (10,  30,  10)   # tume roheline taust — metsatunne
GRID        = (15,  45,  15)   # ruudustikujoonte värv, veidi heledam taustast
USS_PEA     = (0,  255,  80)   # neonroheline — ussi pea
USS_KEHA    = (0,  200,  60)   # tumeroheline — ussi keha
USS_JOON    = (0,  100,  30)   # tume kontuurjoon ümber ussi lülide
VALGE       = (255, 255, 255)  # puhas valge tekstide ja silmade jaoks
KOLLANE     = (255, 220,   0)  # kuldkollane — boonustoit ja rekord
PUNANE      = (220,  40,  40)  # oht/elu — punane
LILLA       = (160,   0, 220)  # mürgiroheline asendus — lilla
HALL        = (120, 120, 120)  # neutraalne hall abiinfo jaoks
TUMESINI    = (20,   20,  60)  # tume sini — overlay'de
ORANZHH     = (255, 140,   0)  # oranž — hoiatusteated

# ── toidutüüpide andmed ───────────────────────────────────────────────────────
# Iga tüüp: (värvitõmme, kontuurvärv, punktiväärtus)
# Parendus 1: kolm erinevat toidutüüpi erineva efektiga
TOIT_TYYP = {
    "tavaline": (PUNANE,   (140,   0,   0),   1),   # tavaline toit +1 p
    "boonus":   (KOLLANE,  (180, 130,   0),   3),   # boonustoit +3 p, vilgub
    "myrk":     (LILLA,    ( 80,   0, 120),  -1),   # mürk võtab elu
}

# ── fondid ────────────────────────────────────────────────────────────────────
fond_suur  = pygame.font.SysFont("arial", 56, bold=True)  # tiitlid
fond_kesk  = pygame.font.SysFont("arial", 32, bold=True)  # alapealkirjad
fond_norm  = pygame.font.SysFont("arial", 24)             # tavalist infot
fond_vike  = pygame.font.SysFont("arial", 18)             # väike abiinfo

# ── globaalne rekord (püsib seansi jooksul) ───────────────────────────────────
# Parendus 5: seansi rekord, mis ei lähtesta mängude vahel
parim_skoor = 0


# ══════════════════════════════════════════════════════════════════════════════
# OOP KLASSID
# Allikas: test 1.py (TechWithTim) cube + snake klassid, kohandatud
# ══════════════════════════════════════════════════════════════════════════════

class Kuup:
    """
    Üks ussi lüli ruudustikul.
    Sisaldab positsiooni [col, row], liikumissuunda ja joonistamise loogikat.
    Vastab test_1 'cube' klassile, aga täiendatud suundtundlike silmadega.
    """

    def __init__(self, pos, suund_x=1, suund_y=0):
        """
        Loo uus lüli.
        pos     — [veerg, rida] ruudustiku koordinaadid
        suund_x — horisontaalne liikumissuund (-1 vasak, +1 parem, 0 seisab)
        suund_y — vertikaalne liikumissuund (-1 üles, +1 alla, 0 seisab)
        """
        self.pos     = list(pos)   # koopia, et muudatused ei mõjutaks originaali
        self.suund_x = suund_x     # jooksev horisontaalne suund
        self.suund_y = suund_y     # jooksev vertikaalne suund

    def liigu(self, dx, dy):
        """
        Nihutatakse lüli ühe sammu võrra antud suunas.
        dx, dy — liikumissuunad (-1, 0 või 1)
        """
        self.suund_x  = dx          # uuenda salvestatud suunda
        self.suund_y  = dy
        self.pos[0]  += dx          # liigu veerus
        self.pos[1]  += dy          # liigu reas

    def joonista(self, surf, on_pea=False):
        """
        Joonista see lüli ekraanile.
        surf   — pygame.Surface, kuhu joonistada
        on_pea — True kui see on ussi pea (joonistab silmad)

        Parendus 3: suundtundlikud silmad peal
        Allikas: test_1.py draw() meetod, täiendatud suunakontrolliga
        """
        # arvuta pikseli koordinaadid ruudustiku positsioonist
        x = self.pos[0] * PLOKI
        y = self.pos[1] * PLOKI

        # ristkülik lüli jaoks, 1 piksel vaba ääre jaoks
        r = pygame.Rect(x + 1, y + 1, PLOKI - 2, PLOKI - 2)

        # pea on heledam kui keha
        varv = USS_PEA if on_pea else USS_KEHA
        pygame.draw.rect(surf, varv,     r, border_radius=4)  # täidisega ruut
        pygame.draw.rect(surf, USS_JOON, r, 1, border_radius=4)  # kontuurjoon

        if on_pea:
            # Parendus 3: silmad joonistame suunast sõltuvalt
            rad = 3   # silmaraadius pikslites

            # vali silmade asukohad liikumissuuna järgi
            if self.suund_x == 1:       # liigub paremale
                s1 = (x + PLOKI - 5, y + 5)
                s2 = (x + PLOKI - 5, y + PLOKI - 7)
            elif self.suund_x == -1:    # liigub vasakule
                s1 = (x + 4, y + 5)
                s2 = (x + 4, y + PLOKI - 7)
            elif self.suund_y == -1:    # liigub üles
                s1 = (x + 5,          y + 4)
                s2 = (x + PLOKI - 7,  y + 4)
            else:                       # liigub alla (ka algseis)
                s1 = (x + 5,          y + PLOKI - 5)
                s2 = (x + PLOKI - 7,  y + PLOKI - 5)

            # joonista must silm + valge läige
            for silm in (s1, s2):
                pygame.draw.circle(surf, (0, 0, 0), silm, rad)       # must ring
                pygame.draw.circle(surf, VALGE,     silm, rad - 1)   # valge läige


class Uss:
    """
    Uss kui järjestatud nimekiri Kuup-lülidest.
    Pea on indeks 0, saba viimane element.
    Vastab test_1 'snake' klassile — reset, addCube, draw loogika.
    """

    def __init__(self, start_pos):
        """
        Loo uus uss alguspositsioonil.
        start_pos — [veerg, rida] ruudustiku koordinaadid
        """
        self.reset(start_pos)   # kasuta reset-meetodit initsialiseerimiseks

    def reset(self, start_pos):
        """
        Lähtesta uss: 1 lüli, liigub paremale.
        Kutsutakse nii __init__ kui ka elu kaotuse korral.
        """
        self.keha    = [Kuup(start_pos, 1, 0)]   # ainult pea alguses
        self.suund_x = 1    # algne liikumissuund: parem
        self.suund_y = 0
        self.kasva   = False   # kasvulipp: True kui järgmisel sammul kasvab

    @property
    def pea_pos(self):
        """Tagasta pea ruudustiku koordinaat listina [x, y]."""
        return self.keha[0].pos[:]   # koopia, et väline kood ei muudaks originaali

    def suu_suund(self, dx, dy):
        """
        Muuda liikumissuunda — ei luba 180° tagasipööret.
        Allikas: test_2 suundloogika (change_to != vastupidine)
        """
        # kontrolli et pole vastupidine suund
        if dx == -self.suund_x and dy == -self.suund_y:
            return   # ignoreeri keelatud suund
        self.suund_x = dx
        self.suund_y = dy

    def liigu(self):
        """
        Liiguta uss ühe sammu võrra.
        Lisa uus pea ette, eemalda saba (kui ei kasva).
        """
        # arvuta uue pea positsioon
        uus_pos = [
            self.keha[0].pos[0] + self.suund_x,
            self.keha[0].pos[1] + self.suund_y,
        ]
        uus_lyly = Kuup(uus_pos, self.suund_x, self.suund_y)
        self.keha.insert(0, uus_lyly)   # lisa pea esikohale

        if self.kasva:
            self.kasva = False   # järgmisel sammul ei kasva enam
        else:
            self.keha.pop()   # eemalda saba, sest ei kasva

    def soo(self):
        """Märgi et uss kasvab järgmisel sammul (söödud toit)."""
        self.kasva = True

    def kontrolli_kokkupoerget(self):
        """
        Kontrolli kas pea puudutab keha mõnda muud lüli.
        Tagastab True kui kokkupõrge toimunud.
        """
        p = self.keha[0].pos   # pea positsioon
        # võrdle pead iga kehaelemendiga (välja arvatud pea ise)
        return p in [l.pos for l in self.keha[1:]]

    def joonista(self, surf):
        """Joonista kõik lülid ekraanile; pea saab silmad."""
        for i, lyly in enumerate(self.keha):
            lyly.joonista(surf, on_pea=(i == 0))   # i==0 on pea


# ══════════════════════════════════════════════════════════════════════════════
# TOIDUD
# Parendus 1: kolm toidutüüpi erineva käitumisega
# ══════════════════════════════════════════════════════════════════════════════

class Toit:
    """
    Toit ruudustikul.
    Parendus 1: toidutüübid — tavaline, boonus (vilgub, ajutine), mürk (võtab elu).
    """

    def __init__(self, uss_keha, tyyp=None):
        """
        Loo uus toit.
        uss_keha — Kuup-objektide nimekiri (et mitte spawn'ida ussi peale)
        tyyp     — sunnitud toidutüüp str-ina; None = juhuslik
        """
        self.tyyp = tyyp or self._vali_tyyp()   # kasuta etteantud või vali juhuslikult
        self.pos  = self._loo_pos(uss_keha)      # leiad tühja koha ruudustikul

        varv_data      = TOIT_TYYP[self.tyyp]   # hangi värvi- ja punktiandmed
        self.varv      = varv_data[0]    # põhivärv
        self.joon_varv = varv_data[1]    # kontuurvärv
        self.punktid   = varv_data[2]    # punktiväärtus (võib olla negatiivne mürgi korral)

        # boonus- ja mürgitoit kaob teatud aja pärast (mitte tavaliine)
        self.eluiga = 120 if self.tyyp != "tavaline" else 99999

    def _vali_tyyp(self):
        """
        Vali juhuslik toidutüüp tõenäosusega:
        70% tavaline, 20% boonus, 10% mürk.
        """
        r = random.random()    # juhuslik arv 0.0 – 1.0 vahel
        if r < 0.70:
            return "tavaline"
        elif r < 0.90:
            return "boonus"
        else:
            return "myrk"

    def _loo_pos(self, uss_keha):
        """
        Leia juhuslik tühi ruudustiku positsioon (mitte ussi kehal).
        Kordab kuni leiab sobiva koha.
        """
        uss_pos = [l.pos for l in uss_keha]   # ussi kõigi lülide positsioonid
        while True:
            x = random.randrange(0, LAIUS  // PLOKI)   # juhusl. veerg
            y = random.randrange(0, KORGUS // PLOKI)   # juhusl. rida
            if [x, y] not in uss_pos:
                return [x, y]   # leitud sobiv koht

    def joonista(self, surf, tick):
        """
        Joonista toit ekraanile.
        tick — mängutsükli loendur, kasutatakse vilkumisanimatsiooniks.
        Parendus 1: boonus vilgub sinuslaine abil, mürk näitab X-märki.
        """
        x = self.pos[0] * PLOKI   # pikseli x-koordinaat
        y = self.pos[1] * PLOKI   # pikseli y-koordinaat
        r = pygame.Rect(x + 1, y + 1, PLOKI - 2, PLOKI - 2)

        if self.tyyp == "boonus":
            # vilkuv efekt: alfa muutub siinuslainena
            alfa = int(180 + 70 * math.sin(tick * 0.15))
            s = pygame.Surface((PLOKI - 2, PLOKI - 2), pygame.SRCALPHA)
            s.fill((*self.varv, alfa))   # RGBA värv muutuva läbipaistvusega
            surf.blit(s, (x + 1, y + 1))
        else:
            # tavaline ja mürk — täisjoonistus
            pygame.draw.rect(surf, self.varv, r, border_radius=3)

        pygame.draw.rect(surf, self.joon_varv, r, 1, border_radius=3)  # kontuurjoon

        if self.tyyp == "myrk":
            # mürgi peal joonista X-märk hoiatuseks
            pygame.draw.line(surf, VALGE, (x+3,       y+3),       (x+PLOKI-4, y+PLOKI-4), 2)
            pygame.draw.line(surf, VALGE, (x+PLOKI-4, y+3),       (x+3,       y+PLOKI-4), 2)


# ══════════════════════════════════════════════════════════════════════════════
# ABIFUNKTSIOONID
# ══════════════════════════════════════════════════════════════════════════════

def joonista_grid():
    """
    Joonista ruudustikujooned kogu ekraanil.
    Annab mängijale visuaalse abijoone liikumise planeerimiseks.
    """
    for x in range(0, LAIUS, PLOKI):    # vertikaalsed jooned
        pygame.draw.line(ekraan, GRID, (x, 0), (x, KORGUS))
    for y in range(0, KORGUS, PLOKI):   # horisontaalsed jooned
        pygame.draw.line(ekraan, GRID, (0, y), (LAIUS, y))


def joonista_hud(skoor, elud, kiirus):
    """
    Joonista ekraani ülaosas infopaneel (HUD = heads-up display).
    Näitab: skoor, rekord, kiirus, elude süda-ikoonid.
    Parendus 2 + 5: elud südametena, rekord püsib läbi mängude.
    """
    # taustariba HUD-i taga
    pygame.draw.rect(ekraan, (0, 50, 0), (0, 0, LAIUS, 36))

    # skoori tekst vasakul
    sk = fond_norm.render(f"Skoor: {skoor}", True, VALGE)
    ekraan.blit(sk, (10, 6))

    # rekord keskel-vasakul
    rek = fond_norm.render(f"Rekord: {parim_skoor}", True, KOLLANE)
    ekraan.blit(rek, (180, 6))

    # kiirus paremal pool
    kii = fond_norm.render(f"Kiirus: {kiirus}  [1-4 muuta]", True, USS_PEA)
    ekraan.blit(kii, (350, 6))

    # elude ikoonid (südamed) ekraani paremas servas
    for i in range(elud):
        pygame.draw.circle(ekraan, PUNANE, (LAIUS - 30 - i * 28, 18), 10)


def tekst_keskele(tekst, fond, varv, y_nihe=0):
    """
    Joonista tekst horisontaalselt ja vertikaalselt keskel + y_nihe.
    Kasutatakse start- ja game-over-ekraanidel.
    """
    pilt = fond.render(tekst, True, varv)
    rect = pilt.get_rect(center=(LAIUS // 2, KORGUS // 2 + y_nihe))
    ekraan.blit(pilt, rect)


def tekst_koht(tekst, fond, varv, x, y):
    """Joonista tekst fikseeritud koordinaadil (x, y)."""
    pilt = fond.render(tekst, True, varv)
    ekraan.blit(pilt, (x, y))


# ══════════════════════════════════════════════════════════════════════════════
# EKRAANID
# ══════════════════════════════════════════════════════════════════════════════

def algus_ekraan():
    """
    Kuva start-ekraan koos difficulty valikuga.
    Parendus 4: difficulty valik start-ekraanil (test_2 stiil).
    Parendus 5: animeeritud tiitel lainelise liikumisega.
    Tagastab valitud kiiruse (int) kui kasutaja vajutab ENTER.
    """
    # kiirusvalikud: (kuvatav nimi, FPS väärtus)
    difficulty_valikud = [
        ("1 — Lihtne",    6),    # 6 frame sekundis = aeglane
        ("2 — Keskmine", 10),    # 10 fps — standardne
        ("3 — Raske",    15),    # 15 fps — kiire
        ("4 — Hull",     22),    # 22 fps — väga kiire
    ]
    valitud = 1   # algselt on valitud "Keskmine"

    tick = 0    # animatsiooniloendur
    while True:
        tick += 1                      # suurenda loendajat iga kaadri tagant
        ekraan.fill(TAUST)             # tühjenda ekraan taustvärviga
        joonista_grid()                # ruudustiku jooned

        # Parendus 5: animeeritud tiitel — laineline üles-alla liikumine
        laine   = int(6 * math.sin(tick * 0.05))    # −6 kuni +6 pikselit
        tiitel  = fond_suur.render("SINU-MODE", True, USS_PEA)
        rect    = tiitel.get_rect(center=(LAIUS // 2, 100 + laine))
        ekraan.blit(tiitel, rect)

        # alampealkiri
        alam = fond_vike.render("Ussimäng  •  Mikk-Gregor Edition", True, HALL)
        ekraan.blit(alam, alam.get_rect(center=(LAIUS // 2, 150)))

        # Parendus 4: difficulty valikumenüü
        tekst_koht("Vali raskusaste:", fond_kesk, VALGE, LAIUS//2 - 150, 200)
        for i, (nimi, _) in enumerate(difficulty_valikud):
            varv = USS_PEA if i == valitud else HALL   # valitud on roheline
            pref = "► " if i == valitud else "   "     # nool valitud ees
            tekst_koht(pref + nimi, fond_norm, varv, LAIUS//2 - 120, 245 + i * 38)

        # legend: selgitab toidutüübid värvilahenditega
        y0 = 410
        tekst_koht("Toidud:", fond_norm, VALGE, LAIUS//2 - 150, y0)
        pygame.draw.rect(ekraan, PUNANE,  (LAIUS//2 - 145, y0+30, 16, 16), border_radius=3)
        tekst_koht("Tavaline  (+1 punkt)",    fond_vike, VALGE,  LAIUS//2 - 122, y0+32)
        pygame.draw.rect(ekraan, KOLLANE, (LAIUS//2 - 145, y0+55, 16, 16), border_radius=3)
        tekst_koht("Boonus  (+3 punkti, vilgub)", fond_vike, KOLLANE, LAIUS//2 - 122, y0+57)
        pygame.draw.rect(ekraan, LILLA,   (LAIUS//2 - 145, y0+80, 16, 16), border_radius=3)
        tekst_koht("Mürk  (−1 elu, X-märk)",  fond_vike, LILLA,  LAIUS//2 - 122, y0+82)

        # klahvijuhend allosas
        tekst_koht("↑↓ vali raskusaste   •   ENTER alusta   •   ESC välju",
                   fond_vike, HALL, LAIUS//2 - 200, KORGUS - 30)

        pygame.display.update()   # kuva kogu uuendus ekraanil

        # sündmuste käsitlemine start-ekraanil
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()       # sulge aken X-ga
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()   # ESC väljub
                if event.key in (pygame.K_UP, pygame.K_w):
                    valitud = (valitud - 1) % len(difficulty_valikud)   # liigu üles
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    valitud = (valitud + 1) % len(difficulty_valikud)   # liigu alla
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return difficulty_valikud[valitud][1]   # tagasta kiirus

        kell.tick(30)   # start-ekraan töötab 30 fps-ga


def game_over_ekraan(skoor):
    """
    Kuva game-over ekraan.
    Parendus 5: rekord nähtav, animeeritud pulseeriv pealkiri.
    Tagastab True (mängi uuesti) või väljub.
    """
    tick = 0   # animatsiooniloendur
    while True:
        tick += 1
        ekraan.fill(TAUST)
        joonista_grid()

        # pulseeriv punane tekst — skaleeritav heledus sinuslainena
        # Allikas: test_2 game_over() efekt, täiendatud pulseerimisega
        heledus = int(200 + 55 * math.sin(tick * 0.08))   # 145–255 vahel
        over_surf = fond_suur.render("GAME OVER", True, (min(255, heledus), 0, 0))
        ekraan.blit(over_surf, over_surf.get_rect(center=(LAIUS//2, KORGUS//2 - 90)))

        tekst_keskele(f"Skoor: {skoor}",          fond_kesk, VALGE,    -10)
        tekst_keskele(f"Kõigi aegade rekord: {parim_skoor}", fond_kesk, KOLLANE,  40)
        tekst_keskele("C = mängi uuesti   •   Q = välju", fond_norm, HALL, 110)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return True    # kasutaja soovib uuesti mängida
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()     # kasutaja soovib väljuda

        kell.tick(30)   # game-over ekraan 30 fps-ga


def paus_overlay(skoor, kiirus):
    """
    Joonista poolläbipaistev pausipaneel mängupildi peale.
    Parendus 5: paus-funktsioon klahviga P.
    """
    # poolläbipaistev must kiht üle ekraani
    overlay = pygame.Surface((LAIUS, KORGUS), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))   # alfa=160 tähendab 63% läbipaistmatust
    ekraan.blit(overlay, (0, 0))

    tekst_keskele("PAUS",                         fond_suur, VALGE,  -80)
    tekst_keskele("P = jätka   •   Q = välju",    fond_norm, HALL,   -20)
    tekst_keskele(f"Skoor: {skoor}  |  Kiirus: {kiirus}", fond_norm, USS_PEA, 30)


# ══════════════════════════════════════════════════════════════════════════════
# PÕHIMÄNG
# ══════════════════════════════════════════════════════════════════════════════

def mang(alg_kiirus):
    """
    Põhimängutsükkel.
    alg_kiirus — mängu algkiirus (FPS) difficulty valikust.

    Parendus 2: 3 elu — uss lähtestub elu kaotuse korral.
    Parendus 4: live kiiruse muutmine klahvidega 1-4.
    """
    global parim_skoor   # kasuta globaalset rekordit

    # ── mängu algolukord ─────────────────────────────────────────────────────
    uss    = Uss([LAIUS // PLOKI // 2, KORGUS // PLOKI // 2])  # uss ekraani keskel
    toidud = [Toit(uss.keha)]   # alustame ühe tavalist toiduga
    skoor  = 0             # jooksev skoor
    elud   = 3             # Parendus 2: alusta 3 eluga
    kiirus = alg_kiirus    # jooksev FPS (muudetav live)
    paus   = False         # pausi olek
    tick   = 0             # üldine kaadriloendur

    boonus_timer = 0   # loendur eri toidutüüpide ilmumise jaoks

    # ── põhitsükkel ──────────────────────────────────────────────────────────
    while True:
        tick += 1   # suurenda kaadriloendurit

        # ── sündmuste käsitlemine ─────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   # sulge aken

            if event.type == pygame.KEYDOWN:
                # väljumisklahvid
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

                # paus sisse/välja
                if event.key == pygame.K_p:
                    paus = not paus

                if not paus:
                    # liikumisklahvid: nooleklahvid + WASD (test_2 stiil)
                    if event.key in (pygame.K_LEFT,  pygame.K_a):
                        uss.suu_suund(-1,  0)   # vasak
                    if event.key in (pygame.K_RIGHT, pygame.K_d):
                        uss.suu_suund( 1,  0)   # parem
                    if event.key in (pygame.K_UP,    pygame.K_w):
                        uss.suu_suund( 0, -1)   # üles
                    if event.key in (pygame.K_DOWN,  pygame.K_s):
                        uss.suu_suund( 0,  1)   # alla

                    # Parendus 4: live kiiruse muutmine numbrite 1-4 abil
                    if event.key == pygame.K_1:
                        kiirus = 6    # lihtne
                    if event.key == pygame.K_2:
                        kiirus = 10   # keskmine
                    if event.key == pygame.K_3:
                        kiirus = 15   # raske
                    if event.key == pygame.K_4:
                        kiirus = 22   # hull

        # ── pausi olek ────────────────────────────────────────────────────
        if paus:
            # joonista mäng + overlay pausis
            ekraan.fill(TAUST)
            joonista_grid()
            for t in toidud:
                t.joonista(ekraan, tick)
            uss.joonista(ekraan)
            joonista_hud(skoor, elud, kiirus)
            paus_overlay(skoor, kiirus)
            pygame.display.update()
            kell.tick(10)   # pausis pole vaja kiiret tsüklit
            continue        # hüppa tsükli algusesse

        # ── ussi liikumine ────────────────────────────────────────────────
        uss.liigu()
        pea = uss.pea_pos   # hangi pea positsioon kontrollimiseks

        # ── piiri kontroll ────────────────────────────────────────────────
        # Allikas: test_2 mängupiiride kontroll (snake_pos < 0 jne)
        if pea[0] < 0 or pea[0] >= LAIUS  // PLOKI or \
           pea[1] < 0 or pea[1] >= KORGUS // PLOKI:
            elud -= 1   # Parendus 2: kaota elu, ärge lõpetage kohe
            if elud <= 0:
                if skoor > parim_skoor:
                    parim_skoor = skoor   # uuenda rekordit
                if game_over_ekraan(skoor):
                    return alg_kiirus   # tagasta kiirus uue mängu käivitamiseks
            else:
                uss.reset([LAIUS//PLOKI//2, KORGUS//PLOKI//2])  # lähtesta uss

        # ── kokkupõrge iseendaga ──────────────────────────────────────────
        if uss.kontrolli_kokkupoerget():
            elud -= 1   # Parendus 2: kaota elu
            if elud <= 0:
                if skoor > parim_skoor:
                    parim_skoor = skoor
                if game_over_ekraan(skoor):
                    return alg_kiirus
            else:
                uss.reset([LAIUS//PLOKI//2, KORGUS//PLOKI//2])

        # ── toiduga kokkupõrge ────────────────────────────────────────────
        soodik = None   # see toit söödi (kui üldse)
        for t in toidud:
            if pea == t.pos:
                soodik = t   # leitud kattuvus
                break

        if soodik:
            toidud.remove(soodik)   # eemalda söödud toit listist

            if soodik.tyyp == "myrk":
                # Parendus 1: mürk võtab elu, ei anna punkte
                elud -= 1
                if elud <= 0:
                    if skoor > parim_skoor:
                        parim_skoor = skoor
                    if game_over_ekraan(skoor):
                        return alg_kiirus
                    else:
                        return alg_kiirus
                else:
                    uss.reset([LAIUS//PLOKI//2, KORGUS//PLOKI//2])
            else:
                # tavaline või boonus: lisa punktid ja kasva
                skoor += soodik.punktid
                if skoor > parim_skoor:
                    parim_skoor = skoor   # uuenda rekord jooksvalt
                uss.soo()   # uss kasvab järgmisel sammul

                # iga 5 punkti tagant kiirus kasvab automaatselt
                if skoor % 5 == 0:
                    kiirus = min(kiirus + 1, 30)   # max 30 fps

            # lisa ekraanile uus toit (tavaline)
            toidud.append(Toit(uss.keha))

        # ── boonus/mürgi automaatne ilmumine ─────────────────────────────
        # Parendus 1: perioodiliselt ilmub boonus- või mürgitoit lisaks
        boonus_timer += 1
        if boonus_timer >= kiirus * 15:   # ~15 sekundi järel
            boonus_timer = 0
            on_erit = any(t.tyyp in ("boonus", "myrk") for t in toidud)
            if not on_erit:   # ärge pane kahte erit korraga
                erit = random.choice(["boonus", "myrk"])
                toidud.append(Toit(uss.keha, erit))

        # ── eluea jälgimine (boonus/mürk kaob aja pärast) ────────────────
        toidud = [t for t in toidud
                  if t.tyyp == "tavaline" or t.eluiga > 0]   # eemalda aegunud
        for t in toidud:
            if t.tyyp != "tavaline":
                t.eluiga -= 1   # lühenda eluiga ühe kaadri võrra

        # ── joonistamine ──────────────────────────────────────────────────
        ekraan.fill(TAUST)            # tühjenda eelmine kaader
        joonista_grid()               # ruudustiku jooned

        for t in toidud:
            t.joonista(ekraan, tick)  # joonista kõik toidud (tick vilkumiseks)

        uss.joonista(ekraan)          # joonista uss lüli kaupa
        joonista_hud(skoor, elud, kiirus)  # joonista infopaneel

        pygame.display.update()       # kuva kogu pilt ekraanile
        kell.tick(kiirus)             # oota nii kaua et FPS = kiirus


# ══════════════════════════════════════════════════════════════════════════════
# PROGRAMMI KÄIVITUS
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # põhitsükkel: start-ekraan > mäng > uuesti, kuni kasutaja väljub
    while True:
        alg_kiirus = algus_ekraan()   # näita start-ekraani, hangi kiirus
        mang(alg_kiirus)              # käivita mäng, see lõpeb game-over-ga
        # game_over_ekraan() tagastab True = uuesti, False pole võimalik (sys.exit)
