# ============================================================
#  menu.py  –  Écran de sélection de difficulté et de niveau
# ============================================================
import pygame
from build_game import DIFFICULTY_LEVELS

BG_COLOR     = (15, 15, 35)
TITLE_COLOR  = (255, 220, 80)
NORMAL_COLOR = (200, 200, 220)
SELECT_COLOR = (80, 200, 120)
HOVER_COLOR  = (255, 160, 40)
BOX_COLOR    = (30, 30, 60)
BOX_BORDER   = (80, 80, 140)


def run_menu(screen):
    """
    Affiche le menu de sélection.
    Retourne (difficulty_name: str, level_path: str) ou None si quitter.
    """
    screen = pygame.display.set_mode((640, 520))
    pygame.display.set_caption("Sokoban - Menu")

    font_title = pygame.font.SysFont("Arial", 42, bold=True)
    font_sub   = pygame.font.SysFont("Arial", 28, bold=True)
    font_btn   = pygame.font.SysFont("Arial", 22)
    font_hint  = pygame.font.SysFont("Arial", 16)

    difficulties = list(DIFFICULTY_LEVELS.keys())
    sel_diff  = 0
    sel_lvl   = 0
    mouse_pos = (0, 0)
    clock     = pygame.time.Clock()

    while True:
        W, H = screen.get_width(), screen.get_height()

        # Positions fixes recalculees a chaque frame (meme logique rendu + clic)
        btn_w, btn_h = 160, 48
        total_w = len(difficulties) * btn_w + (len(difficulties) - 1) * 20
        sx = (W - total_w) // 2
        diff_rects = [pygame.Rect(sx + i * (btn_w + 20), 155, btn_w, btn_h)
                      for i in range(len(difficulties))]

        levels   = DIFFICULTY_LEVELS[difficulties[sel_diff]]
        btn_w2   = 120
        total_w2 = len(levels) * btn_w2 + (len(levels) - 1) * 20
        sx2      = (W - total_w2) // 2
        lvl_rects = [pygame.Rect(sx2 + j * (btn_w2 + 20), 273, btn_w2, btn_h)
                     for j in range(len(levels))]

        play_rect = pygame.Rect(W // 2 - 110, 355, 220, 58)

        # ── Evenements ────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    return None
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return difficulties[sel_diff], levels[sel_lvl]

            if event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Difficulte
                for i, r in enumerate(diff_rects):
                    if r.collidepoint(event.pos):
                        sel_diff = i
                        sel_lvl  = 0
                        # Recalculer levels apres changement de difficulte
                        levels = DIFFICULTY_LEVELS[difficulties[sel_diff]]
                # Niveau
                for j, r in enumerate(lvl_rects):
                    if r.collidepoint(event.pos):
                        sel_lvl = j
                # JOUER
                if play_rect.collidepoint(event.pos):
                    return difficulties[sel_diff], levels[sel_lvl]

        # ── Rendu ─────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Titre
        t = font_title.render("SOKOBAN", True, TITLE_COLOR)
        screen.blit(t, t.get_rect(center=(W // 2, 60)))

        # Difficulte
        sub = font_sub.render("Difficulte :", True, NORMAL_COLOR)
        screen.blit(sub, sub.get_rect(center=(W // 2, 125)))

        for i, rect in enumerate(diff_rects):
            selected = (i == sel_diff)
            hovered  = rect.collidepoint(mouse_pos)
            color    = SELECT_COLOR if selected else (HOVER_COLOR if hovered else BOX_COLOR)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, BOX_BORDER, rect, 2, border_radius=8)
            txt_c = (20, 20, 20) if selected or hovered else NORMAL_COLOR
            lbl = font_btn.render(difficulties[i], True, txt_c)
            screen.blit(lbl, lbl.get_rect(center=rect.center))

        # Niveau
        sub2 = font_sub.render("Niveau :", True, NORMAL_COLOR)
        screen.blit(sub2, sub2.get_rect(center=(W // 2, 250)))

        for j, rect in enumerate(lvl_rects):
            selected = (j == sel_lvl)
            hovered  = rect.collidepoint(mouse_pos)
            color    = SELECT_COLOR if selected else (HOVER_COLOR if hovered else BOX_COLOR)
            pygame.draw.rect(screen, color, rect, border_radius=8)
            pygame.draw.rect(screen, BOX_BORDER, rect, 2, border_radius=8)
            txt_c = (20, 20, 20) if selected or hovered else NORMAL_COLOR
            lbl = font_btn.render(f"Niveau {j+1}", True, txt_c)
            screen.blit(lbl, lbl.get_rect(center=rect.center))

        # Bouton JOUER
        play_hov = play_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, (70, 220, 100) if play_hov else (50, 180, 80),
                         play_rect, border_radius=12)
        pygame.draw.rect(screen, (20, 120, 40), play_rect, 3, border_radius=12)
        play_lbl = font_sub.render("JOUER", True, (255, 255, 255))
        screen.blit(play_lbl, play_lbl.get_rect(center=play_rect.center))

        # Selection courante + aide
        info = font_hint.render(
            f"Selection : {difficulties[sel_diff]}  -  Niveau {sel_lvl + 1}",
            True, (160, 200, 160))
        screen.blit(info, info.get_rect(center=(W // 2, 435)))

        hint = font_hint.render(
            "Entree / Espace = Jouer   |   Q = Quitter",
            True, (100, 100, 140))
        screen.blit(hint, hint.get_rect(center=(W // 2, 490)))

        pygame.display.flip()
        clock.tick(60)