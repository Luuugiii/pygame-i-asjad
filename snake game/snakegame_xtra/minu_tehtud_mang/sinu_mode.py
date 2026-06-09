"""
SINU-MODE Ussimäng
==================
Baas: tet_3.py (Mikk-Gregor)
Integreeritud: test_1.py (OOP cube/snake klassid, silmad)
              test_2.py (difficulty süsteem, puhas loogika)

Uued funktsioonid SINU-MODE:
  - Kolm toidutüüpi: tavaline (punane), boonus (kuldne, +3), mürk (lilla, -1 elu)
  - 3 elu süsteem — uss lähtestatakse, mäng ei lõpe kohe
  - Pea joonistamine silmadega (test_1 stiil)
  - Difficulty valik menüüs (test_2 stiil)
  - Animeeritud "SINU-MODE" tiitel start-ekraanil
  - Kõigi aegade rekord säilib seansi vältel
"""

import pygame
import random
import sys
import math

pygame.init()

# ── aken ────────────────────────────────────────────────────────
LAIUS = 1920
KORGUS = 1080
PLOKI = 20

ekraan = pygame.display.set_mode((LAIUS, KORGUS))
pygame.display.set_caption("SINU-MODE Ussimäng")
kell = pygame.time.Clock()

# ── värvid ────────────────────────────────────────────────────────
TAUST       = (10, 30, 10)
GRID        = (15, 45, 15)
USS_PEA     = (0, 255, 80)
USS_KEHA    = (0, 200, 60)
USS_JOON    = (0, 100, 30)
VALGE       = (255, 255, 255)
KOLLANE     = (255, 220, 0)
PUNANE      = (220, 40, 40)
LILLA       = (160, 0, 220)
HALL        = (120, 120, 120)
TUMESINI    = (20, 20, 60)
ORANZHH     = (255, 140, 0)

# toidutüübid: (nimi, varv, joonis_varv, punktid)
TOIT_TYYP = {
    "tavaline": (PUNANE,   (140, 0, 0),   1),
    "boonus":   (KOLLANE,  (180, 130, 0), 3),
    "myrk":     (LILLA,    (80, 0, 120), -1),   # kaotab elu
}

# ── fondid ────────────────────────────────────────────────────────
fond_suur  = pygame.font.SysFont("arial", 56, bold=True)
fond_kesk  = pygame.font.SysFont("arial", 32, bold=True)
fond_norm  = pygame.font.SysFont("arial", 24)
fond_vike  = pygame.font.SysFont("arial", 18)

# ── globaalsed mänguandmed ────────────────────────────────────────
parim_skoor = 0


# ══════════════════════════════════════════════════════════════════
# OOP KLASSID  (test_1.py põhjal, kohandatud)
# ══════════════════════════════════════════════════════════════════

class Kuup:
    """Üks ussi lüli (test_1 cube klass, kohandatud SINU-MODE visuaalile)."""

    def __init__(self, pos, suund_x=1, suund_y=0):
        self.pos     = list(pos)   # [col, row]  ruudustiku koordinaadid
        self.suund_x = suund_x
        self.suund_y = suund_y

    def liigu(self, dx, dy):
        self.suund_x = dx
        self.suund_y = dy
        self.pos[0] += dx
        self.pos[1] += dy

    def joonista(self, surf, on_pea=False):
        x = self.pos[0] * PLOKI
        y = self.pos[1] * PLOKI
        r = pygame.Rect(x + 1, y + 1, PLOKI - 2, PLOKI - 2)

        varv = USS_PEA if on_pea else USS_KEHA
        pygame.draw.rect(surf, varv, r, border_radius=4)
        pygame.draw.rect(surf, USS_JOON, r, 1, border_radius=4)

        if on_pea:
            # silmad — test_1 stiil, aga skaleeritud
            c = PLOKI // 2
            rad = 3
            # suund määrab silmade asukoha
            if self.suund_x == 1:    # parem
                s1 = (x + PLOKI - 5, y + 5)
                s2 = (x + PLOKI - 5, y + PLOKI - 7)
            elif self.suund_x == -1: # vasak
                s1 = (x + 4, y + 5)
                s2 = (x + 4, y + PLOKI - 7)
            elif self.suund_y == -1: # üles
                s1 = (x + 5, y + 4)
                s2 = (x + PLOKI - 7, y + 4)
            else:                    # alla
                s1 = (x + 5, y + PLOKI - 5)
                s2 = (x + PLOKI - 7, y + PLOKI - 5)

            pygame.draw.circle(surf, (0, 0, 0), s1, rad)
            pygame.draw.circle(surf, (0, 0, 0), s2, rad)
            pygame.draw.circle(surf, VALGE, s1, rad - 1)
            pygame.draw.circle(surf, VALGE, s2, rad - 1)


class Uss:
    """Uss kui lülide nimekiri (test_1 snake klass, lihtsustatud)."""

    def __init__(self, start_pos):
        self.reset(start_pos)

    def reset(self, start_pos):
        self.keha    = [Kuup(start_pos, 1, 0)]
        self.suund_x = 1
        self.suund_y = 0
        self.kasva   = False

    @property
    def pea_pos(self):
        return self.keha[0].pos[:]

    def suu_suund(self, dx, dy):
        """Muuda suunda (ei luba tagasipööret)."""
        if dx == -self.suund_x and dy == -self.suund_y:
            return
        self.suund_x = dx
        self.suund_y = dy

    def liigu(self):
        uus_pos = [
            self.keha[0].pos[0] + self.suund_x,
            self.keha[0].pos[1] + self.suund_y,
        ]
        uus_lyly = Kuup(uus_pos, self.suund_x, self.suund_y)
        self.keha.insert(0, uus_lyly)

        if self.kasva:
            self.kasva = False
        else:
            self.keha.pop()

    def soo(self):
        self.kasva = True

    def kontrolli_kokkupoerget(self):
        p = self.keha[0].pos
        return p in [l.pos for l in self.keha[1:]]

    def joonista(self, surf):
        for i, lyly in enumerate(self.keha):
            lyly.joonista(surf, on_pea=(i == 0))


# ══════════════════════════════════════════════════════════════════
# TOIDUD
# ══════════════════════════════════════════════════════════════════

class Toit:
    def __init__(self, uss_keha, tyyp=None):
        self.tyyp = tyyp or self._vali_tyyp()
        self.pos  = self._loo_pos(uss_keha)
        varv_data = TOIT_TYYP[self.tyyp]
        self.varv      = varv_data[0]
        self.joon_varv = varv_data[1]
        self.punktid   = varv_data[2]
        self.eluiga    = 100 if self.tyyp != "tavaline" else 9999  # boonus kaob

    def _vali_tyyp(self):
        # 70% tavaline, 20% boonus, 10% mürk
        r = random.random()
        if r < 0.70:
            return "tavaline"
        elif r < 0.90:
            return "boonus"
        else:
            return "myrk"

    def _loo_pos(self, uss_keha):
        uss_pos = [l.pos for l in uss_keha]
        while True:
            x = random.randrange(0, LAIUS  // PLOKI)
            y = random.randrange(0, KORGUS // PLOKI)
            if [x, y] not in uss_pos:
                return [x, y]

    def joonista(self, surf, tick):
        x = self.pos[0] * PLOKI
        y = self.pos[1] * PLOKI
        r = pygame.Rect(x + 1, y + 1, PLOKI - 2, PLOKI - 2)

        # boonus vilgub
        if self.tyyp == "boonus":
            alfa = int(180 + 70 * math.sin(tick * 0.15))
            s = pygame.Surface((PLOKI - 2, PLOKI - 2), pygame.SRCALPHA)
            s.fill((*self.varv, alfa))
            surf.blit(s, (x + 1, y + 1))
        else:
            pygame.draw.rect(surf, self.varv, r, border_radius=3)

        pygame.draw.rect(surf, self.joon_varv, r, 1, border_radius=3)

        # mürgi peal X
        if self.tyyp == "myrk":
            pygame.draw.line(surf, VALGE, (x+3, y+3), (x+PLOKI-4, y+PLOKI-4), 2)
            pygame.draw.line(surf, VALGE, (x+PLOKI-4, y+3), (x+3, y+PLOKI-4), 2)


# ══════════════════════════════════════════════════════════════════
# ABIFUNKTSIOONID
# ══════════════════════════════════════════════════════════════════

def joonista_grid():
    for x in range(0, LAIUS, PLOKI):
        pygame.draw.line(ekraan, GRID, (x, 0), (x, KORGUS))
    for y in range(0, KORGUS, PLOKI):
        pygame.draw.line(ekraan, GRID, (0, y), (LAIUS, y))


def joonista_hud(skoor, elud, kiirus):
    # taustariba
    pygame.draw.rect(ekraan, (0, 50, 0), (0, 0, LAIUS, 36))

    sk = fond_norm.render(f"Skoor: {skoor}", True, VALGE)
    ekraan.blit(sk, (10, 6))

    rek = fond_norm.render(f"Rekord: {parim_skoor}", True, KOLLANE)
    ekraan.blit(rek, (200, 6))

    kii = fond_norm.render(f"Kiirus: {kiirus}", True, USS_PEA)
    ekraan.blit(kii, (400, 6))

    # elud südametena
    for i in range(elud):
        pygame.draw.circle(ekraan, PUNANE, (LAIUS - 30 - i * 28, 18), 10)


def tekst_keskele(tekst, fond, varv, y_nihe=0):
    pilt = fond.render(tekst, True, varv)
    rect = pilt.get_rect(center=(LAIUS // 2, KORGUS // 2 + y_nihe))
    ekraan.blit(pilt, rect)


def tekst_koht(tekst, fond, varv, x, y):
    pilt = fond.render(tekst, True, varv)
    ekraan.blit(pilt, (x, y))


# ══════════════════════════════════════════════════════════════════
# EKRAANID
# ══════════════════════════════════════════════════════════════════

def algus_ekraan():
    """Start-ekraan koos difficulty valikuga (test_2 stiil)."""
    difficulty_valikud = [
        ("1 — Lihtne",    6),
        ("2 — Keskmine", 10),
        ("3 — Raske",    15),
        ("4 — Hull",     22),
    ]
    valitud = 1  # indeks

    tick = 0
    while True:
        tick += 1
        ekraan.fill(TAUST)
        joonista_grid()

        # animeeritud tiitel
        laine = int(4 * math.sin(tick * 0.05))
        tiitel = fond_suur.render("SINU-MODE", True, USS_PEA)
        rect   = tiitel.get_rect(center=(LAIUS // 2, 120 + laine))
        ekraan.blit(tiitel, rect)

        alam = fond_vike.render("Ussimäng  •  Mikk-Gregor Edition", True, HALL)
        ekraan.blit(alam, alam.get_rect(center=(LAIUS // 2, 170)))

        # difficulty nupu
        tekst_koht("Vali raskusaste:", fond_kesk, VALGE, LAIUS//2 - 160, 230)
        for i, (nimi, _) in enumerate(difficulty_valikud):
            varv  = USS_PEA if i == valitud else HALL
            pref  = "► " if i == valitud else "   "
            tekst_koht(pref + nimi, fond_norm, varv, LAIUS//2 - 130, 275 + i * 38)

        # legend
        y0 = 450
        tekst_koht("Toidud:", fond_norm, VALGE, LAIUS//2 - 160, y0)
        pygame.draw.rect(ekraan, PUNANE,  (LAIUS//2 - 155, y0+30, 16, 16), border_radius=3)
        tekst_koht("Tavaline  (+1)", fond_vike, VALGE, LAIUS//2 - 133, y0+32)
        pygame.draw.rect(ekraan, KOLLANE, (LAIUS//2 - 155, y0+55, 16, 16), border_radius=3)
        tekst_koht("Boonus  (+3)", fond_vike, KOLLANE, LAIUS//2 - 133, y0+57)
        pygame.draw.rect(ekraan, LILLA,   (LAIUS//2 - 155, y0+80, 16, 16), border_radius=3)
        tekst_koht("Mürk  (−elu)", fond_vike, LILLA, LAIUS//2 - 133, y0+82)

        tekst_koht("↑↓ vali   •   ENTER alusta   •   ESC välju",
                   fond_vike, HALL, LAIUS//2 - 170, KORGUS - 36)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if event.key in (pygame.K_UP, pygame.K_w):
                    valitud = (valitud - 1) % len(difficulty_valikud)
                if event.key in (pygame.K_DOWN, pygame.K_s):
                    valitud = (valitud + 1) % len(difficulty_valikud)
                if event.key in (pygame.K_RETURN, pygame.K_c):
                    return difficulty_valikud[valitud][1]

        kell.tick(30)


def game_over_ekraan(skoor):
    """YOU DIED stiil (test_2), eestikeelsete tekstidega."""
    tick = 0
    while True:
        tick += 1
        ekraan.fill(TAUST)
        joonista_grid()

        # pulseeriv punane tiitel
        alfa_scale = int(200 + 55 * math.sin(tick * 0.08))
        over_surf  = fond_suur.render("GAME OVER", True,
                                       (min(255, alfa_scale), 0, 0))
        ekraan.blit(over_surf, over_surf.get_rect(center=(LAIUS//2, KORGUS//2 - 80)))

        tekst_keskele(f"Skoor: {skoor}",      fond_kesk, VALGE,   0)
        tekst_keskele(f"Rekord: {parim_skoor}", fond_kesk, KOLLANE, 50)
        tekst_keskele("C = uuesti   •   Q = välju", fond_norm, HALL, 120)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

        kell.tick(30)


def paus_overlay(skoor, kiirus):
    overlay = pygame.Surface((LAIUS, KORGUS), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    ekraan.blit(overlay, (0, 0))

    tekst_keskele("PAUS", fond_suur, VALGE, -80)
    tekst_keskele("P = jätka   •   Q = välju", fond_norm, HALL, -20)
    tekst_keskele(f"Skoor: {skoor}  |  Kiirus: {kiirus}", fond_norm, USS_PEA, 30)


# ══════════════════════════════════════════════════════════════════
# PÕHIMÄNG
# ══════════════════════════════════════════════════════════════════

def mang(alg_kiirus):
    global parim_skoor

    uss    = Uss([LAIUS // PLOKI // 2, KORGUS // PLOKI // 2])
    toidud = [Toit(uss.keha)]        # alguses üks toit
    skoor  = 0
    elud   = 3
    kiirus = alg_kiirus
    paus   = False
    tick   = 0

    # boonus-toidu ajastus
    boonus_timer = 0

    while True:
        tick += 1

        # ── sündmused ──────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    pygame.quit(); sys.exit()

                if event.key == pygame.K_p:
                    paus = not paus

                if not paus:
                    if event.key in (pygame.K_LEFT,  pygame.K_a): uss.suu_suund(-1,  0)
                    if event.key in (pygame.K_RIGHT, pygame.K_d): uss.suu_suund( 1,  0)
                    if event.key in (pygame.K_UP,    pygame.K_w): uss.suu_suund( 0, -1)
                    if event.key in (pygame.K_DOWN,  pygame.K_s): uss.suu_suund( 0,  1)

                    # kiiruse vahetamine nagu test_1 / tet_3
                    if event.key == pygame.K_1: kiirus = 6
                    if event.key == pygame.K_2: kiirus = 10
                    if event.key == pygame.K_3: kiirus = 15
                    if event.key == pygame.K_4: kiirus = 22

        # ── paus ───────────────────────────────────────────────
        if paus:
            ekraan.fill(TAUST)
            joonista_grid()
            for t in toidud: t.joonista(ekraan, tick)
            uss.joonista(ekraan)
            joonista_hud(skoor, elud, kiirus)
            paus_overlay(skoor, kiirus)
            pygame.display.update()
            kell.tick(10)
            continue

        # ── liikumine ──────────────────────────────────────────
        uss.liigu()
        pea = uss.pea_pos

        # ── piiride kontroll ───────────────────────────────────
        if pea[0] < 0 or pea[0] >= LAIUS//PLOKI or \
           pea[1] < 0 or pea[1] >= KORGUS//PLOKI:
            elud -= 1
            if elud <= 0:
                if skoor > parim_skoor: parim_skoor = skoor
                if game_over_ekraan(skoor):
                    return alg_kiirus   # tagasta kiirus uue mängu jaoks
            else:
                uss.reset([LAIUS//PLOKI//2, KORGUS//PLOKI//2])

        # ── kokkupõrge iseendaga ───────────────────────────────
        if uss.kontrolli_kokkupoerget():
            elud -= 1
            if elud <= 0:
                if skoor > parim_skoor: parim_skoor = skoor
                if game_over_ekraan(skoor):
                    return alg_kiirus
            else:
                uss.reset([LAIUS//PLOKI//2, KORGUS//PLOKI//2])

        # ── toiduga kokkupõrge ─────────────────────────────────
        soodik = None
        for t in toidud:
            if pea == t.pos:
                soodik = t
                break

        if soodik:
            toidud.remove(soodik)

            if soodik.tyyp == "myrk":
                elud -= 1
                if elud <= 0:
                    if skoor > parim_skoor: parim_skoor = skoor
                    if game_over_ekraan(skoor):
                        return alg_kiirus
                    else:
                        return alg_kiirus
            else:
                skoor += soodik.punktid
                if skoor > parim_skoor: parim_skoor = skoor
                uss.soo()

                # iga 5 punkti taga kiirus tõuseb
                if skoor % 5 == 0:
                    kiirus = min(kiirus + 1, 30)

            # lisa uus toit
            toidud.append(Toit(uss.keha))

        # ── boonus-toidu ilmumine ──────────────────────────────
        boonus_timer += 1
        if boonus_timer >= kiirus * 15:  # ~15 sekundi tagant
            boonus_timer = 0
            on_boonus = any(t.tyyp in ("boonus", "myrk") for t in toidud)
            if not on_boonus:
                tyyp = random.choice(["boonus", "myrk"])
                toidud.append(Toit(uss.keha, tyyp))

        # ── eluea kontroll ────────────────────────────────────
        toidud = [t for t in toidud
                  if t.tyyp == "tavaline" or t.eluiga > 0]
        for t in toidud:
            if t.tyyp != "tavaline":
                t.eluiga -= 1

        # ── joonistamine ───────────────────────────────────────
        ekraan.fill(TAUST)
        joonista_grid()

        for t in toidud:
            t.joonista(ekraan, tick)

        uss.joonista(ekraan)
        joonista_hud(skoor, elud, kiirus)

        pygame.display.update()
        kell.tick(kiirus)


# ══════════════════════════════════════════════════════════════════
# KÄIVITUS
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    while True:
        alg_kiirus = algus_ekraan()
        mang(alg_kiirus)
