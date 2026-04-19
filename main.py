# ============================================================
#  main.py  –  Boucle de jeu principale Sokoban
# ============================================================
import pygame
import time
import os
from copy import deepcopy

from build_game   import move_player, load_level, is_solved, has_deadlock, DIFFICULTY_LEVELS
from display_game import (draw_grid, draw_hud, draw_hint_bar,
                          draw_victory, draw_deadlock_warning, TILE_SIZE)
from solver       import a_star_solver
from scores       import get_best, update_best
from menu         import run_menu

HUD_HEIGHT  = 44   # barre du haut
HINT_HEIGHT = 28   # barre de contrôles en bas
MAX_UNDO    = 50   # taille maximale de la pile d'annulation


def run_game(screen, difficulty, level_path):
    """
    Lance une partie. Retourne : "menu" | "next" | "quit"
    """
    level_name = os.path.splitext(os.path.basename(level_path))[0].replace("_", " ").title()

    matrix = load_level(level_path)
    if matrix is None:
        return "menu"

    initial_state = deepcopy(matrix)
    best_score    = get_best(level_path)

    cols = len(matrix[0])
    rows = len(matrix)
    W    = max(cols * TILE_SIZE, 480)
    H    = rows * TILE_SIZE + HUD_HEIGHT + HINT_HEIGHT
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption(f"Sokoban – {level_name}")

    font_hud   = pygame.font.SysFont("Arial", 18, bold=True)
    font_hint  = pygame.font.SysFont("Arial", 15)
    font_big   = pygame.font.SysFont("Arial", 36, bold=True)
    font_small = pygame.font.SysFont("Arial", 21)

    moves_count   = 0
    solved        = False
    solving       = False
    is_new_record = False
    deadlocked    = False

    # Pile d'annulation : liste de (matrix, moves_count)
    undo_stack = []

    clock = pygame.time.Clock()

    def _render(show_deadlock=False):
        screen.fill((12, 12, 28))
        game_rect = pygame.Rect(0, HUD_HEIGHT, W, H - HUD_HEIGHT - HINT_HEIGHT)
        game_surf = screen.subsurface(game_rect)
        draw_grid(game_surf, matrix, deadlock=show_deadlock and deadlocked)
        draw_hud(screen, font_hud, moves_count, best_score, level_name, difficulty, W)
        draw_hint_bar(screen, font_hint, W, H, undo_available=bool(undo_stack))
        if show_deadlock and deadlocked:
            draw_deadlock_warning(screen, font_hint, W, H)
        if solved:
            draw_victory(screen, font_big, font_small,
                         moves_count, best_score, is_new_record, W, H)
        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return "quit"
                if event.key == pygame.K_ESCAPE:
                    return "menu"
                if event.key == pygame.K_n and solved:
                    return "next"

                # Reset
                if event.key == pygame.K_r:
                    matrix        = deepcopy(initial_state)
                    moves_count   = 0
                    solved        = False
                    deadlocked    = False
                    is_new_record = False
                    undo_stack.clear()

                if solved or solving:
                    continue

                # ── Undo (Z) ──────────────────────────────────
                if event.key == pygame.K_z and undo_stack:
                    matrix, moves_count = undo_stack.pop()
                    deadlocked = has_deadlock(matrix)
                    continue

                # ── Déplacements manuels ──────────────────────
                direction = {
                    pygame.K_UP:    "UP",
                    pygame.K_DOWN:  "DOWN",
                    pygame.K_LEFT:  "LEFT",
                    pygame.K_RIGHT: "RIGHT",
                }.get(event.key)

                if direction:
                    new_matrix, moved = move_player(matrix, direction)
                    if moved:
                        # Sauvegarder l'état avant dans la pile d'annulation
                        undo_stack.append((deepcopy(matrix), moves_count))
                        if len(undo_stack) > MAX_UNDO:
                            undo_stack.pop(0)
                        matrix       = new_matrix
                        moves_count += 1
                        deadlocked   = has_deadlock(matrix)

                        if is_solved(matrix):
                            solved        = True
                            is_new_record = update_best(level_path, moves_count)
                            best_score    = get_best(level_path)

                # ── Solveur IA (A) ────────────────────────────
                if event.key == pygame.K_a:
                    solving  = True
                    solution = a_star_solver(deepcopy(matrix))
                    if solution:
                        for move in solution:
                            undo_stack.append((deepcopy(matrix), moves_count))
                            if len(undo_stack) > MAX_UNDO:
                                undo_stack.pop(0)
                            matrix, _ = move_player(matrix, move)
                            moves_count += 1
                            _render(show_deadlock=False)
                            time.sleep(0.22)
                        if is_solved(matrix):
                            solved        = True
                            is_new_record = update_best(level_path, moves_count)
                            best_score    = get_best(level_path)
                    else:
                        print("Aucune solution trouvée.")
                    solving = False

        _render(show_deadlock=True)
        clock.tick(30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 520))

    while True:
        result = run_menu(screen)
        if result is None:
            break

        difficulty, level_path = result
        levels = DIFFICULTY_LEVELS[difficulty]
        idx    = levels.index(level_path)

        while idx < len(levels):
            outcome = run_game(screen, difficulty, levels[idx])
            if outcome == "quit":
                pygame.quit()
                return
            elif outcome == "menu":
                break
            elif outcome == "next":
                idx += 1
                if idx >= len(levels):
                    print(f"Difficulté '{difficulty}' terminée !")
                    break

    pygame.quit()


if __name__ == "__main__":
    main()
