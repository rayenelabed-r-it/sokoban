# ============================================================
#  display_game.py  –  Rendu visuel Pygame
# ============================================================
import pygame
from build_game import WALL, EMPTY, TARGET, BOX, PLAYER, BOX_ON_TARGET, PLAYER_ON_TARGET

TILE_SIZE = 64

COLORS = {
    WALL:             (45,  45,  75),
    EMPTY:            (225, 220, 205),
    TARGET:           (255, 190,  60),
    BOX:              (165,  90,  40),
    PLAYER:           (30,  144, 255),
    BOX_ON_TARGET:    (50,  210,  80),
    PLAYER_ON_TARGET: (0,   200, 255),
}

BORDER_COLORS = {
    WALL:             (20,  20,  50),
    EMPTY:            (195, 190, 175),
    TARGET:           (200, 130,  20),
    BOX:              (100,  50,  15),
    PLAYER:           (10,  100, 200),
    BOX_ON_TARGET:    (20,  140,  30),
    PLAYER_ON_TARGET: (0,   130, 200),
}


def draw_grid(screen, matrix, deadlock=False):
    """Dessine la grille. Si deadlock=True, teinte rouge les caisses bloquées."""
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            x = c * TILE_SIZE
            y = r * TILE_SIZE
            rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

            bg     = COLORS.get(cell, (0, 0, 0))
            border = BORDER_COLORS.get(cell, (0, 0, 0))

            pygame.draw.rect(screen, bg, rect)
            pygame.draw.rect(screen, border, rect, 2)

            cx, cy = x + TILE_SIZE // 2, y + TILE_SIZE // 2
            r2 = TILE_SIZE // 2 - 6

            if cell == TARGET:
                _draw_cross(screen, cx, cy, r2, (200, 130, 20))

            elif cell == BOX:
                inner = rect.inflate(-16, -16)
                color = (200, 50, 50) if deadlock else (120, 60, 20)
                pygame.draw.rect(screen, color, inner, border_radius=4)
                if deadlock:
                    # Croix rouge sur caisse bloquée
                    _draw_cross(screen, cx, cy, r2 - 10, (255, 100, 100), width=4)

            elif cell == BOX_ON_TARGET:
                inner = rect.inflate(-16, -16)
                pygame.draw.rect(screen, (30, 160, 30), inner, border_radius=4)
                _draw_cross(screen, cx, cy, r2 - 8, (20, 100, 20))

            elif cell == PLAYER:
                pygame.draw.circle(screen, (10, 100, 200), (cx, cy), r2)
                pygame.draw.circle(screen, (200, 230, 255), (cx, cy), r2 // 2)

            elif cell == PLAYER_ON_TARGET:
                pygame.draw.circle(screen, (0, 140, 200), (cx, cy), r2)
                pygame.draw.circle(screen, (200, 240, 255), (cx, cy), r2 // 2)
                _draw_cross(screen, cx, cy, r2 - 8, (0, 80, 160))


def _draw_cross(surface, cx, cy, size, color, width=3):
    pygame.draw.line(surface, color, (cx - size, cy), (cx + size, cy), width)
    pygame.draw.line(surface, color, (cx, cy - size), (cx, cy + size), width)


def draw_hud(screen, font, moves_count, best_score, level_name, difficulty, width):
    """Barre HUD : difficulté | niveau | coups | record."""
    pygame.draw.rect(screen, (18, 18, 42), (0, 0, width, 44))
    pygame.draw.line(screen, (80, 80, 140), (0, 44), (width, 44), 1)

    best_str = f"🏆 {best_score}" if best_score is not None else "🏆 —"
    txt = font.render(
        f"  {difficulty}  ·  {level_name}  ·  Coups : {moves_count}  ·  {best_str}",
        True, (255, 215, 60)
    )
    screen.blit(txt, (8, 10))


def draw_hint_bar(screen, font, width, height, undo_available):
    """Barre de contrôles en bas."""
    pygame.draw.rect(screen, (18, 18, 42), (0, height - 28, width, 28))
    pygame.draw.line(screen, (80, 80, 140), (0, height - 28), (width, height - 28), 1)
    undo_color = (160, 230, 160) if undo_available else (100, 100, 130)
    hint = font.render(
        "  Flèches=déplacer   Z=annuler   A=IA   R=reset   ESC=menu",
        True, undo_color if undo_available else (130, 130, 160)
    )
    screen.blit(hint, (6, height - 24))


def draw_victory(screen, font_big, font_small, moves_count, best_score, is_new_record, width, height):
    """Overlay de victoire."""
    overlay = pygame.Surface((width, height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    screen.blit(overlay, (0, 0))

    title_color = (80, 255, 150) if is_new_record else (255, 230, 80)
    title_text  = "🎉 Nouveau record !" if is_new_record else "✅ Niveau terminé !"

    t1 = font_big.render(title_text, True, title_color)
    t2 = font_small.render(f"Résolu en {moves_count} coups", True, (255, 255, 255))

    best_str = f"(record : {best_score} coups)" if best_score else ""
    t3 = font_small.render(best_str, True, (180, 180, 180))
    t4 = font_small.render("N = Niveau suivant   R = Recommencer   ESC = Menu", True, (200, 200, 200))

    screen.blit(t1, t1.get_rect(center=(width//2, height//2 - 70)))
    screen.blit(t2, t2.get_rect(center=(width//2, height//2 - 20)))
    screen.blit(t3, t3.get_rect(center=(width//2, height//2 + 20)))
    screen.blit(t4, t4.get_rect(center=(width//2, height//2 + 65)))


def draw_deadlock_warning(screen, font, width, height):
    """Message d'avertissement de deadlock."""
    txt = font.render("⚠  Deadlock détecté !  Appuyez sur Z pour annuler ou R pour reset.", True, (255, 80, 80))
    pygame.draw.rect(screen, (60, 10, 10), (0, 44, width, 32))
    screen.blit(txt, txt.get_rect(center=(width//2, 60)))
