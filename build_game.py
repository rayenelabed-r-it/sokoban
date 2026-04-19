# ============================================================
#  build_game.py  –  Logique du Sokoban
# ============================================================
from copy import deepcopy
import os

# Constantes numériques
WALL             = -1
EMPTY            =  0
TARGET           =  1
BOX              =  2
PLAYER           =  3
BOX_ON_TARGET    =  4
PLAYER_ON_TARGET =  5

# Alias courts pour la rétrocompatibilité
wall             = WALL
empty            = EMPTY
target           = TARGET
box              = BOX
player           = PLAYER
box_on_target    = BOX_ON_TARGET
player_on_target = PLAYER_ON_TARGET

DIRECTIONS = {
    "UP":    (-1,  0),
    "DOWN":  ( 1,  0),
    "LEFT":  ( 0, -1),
    "RIGHT": ( 0,  1),
}


# ----------------------------------------------------------
#  Déplacement du joueur
# ----------------------------------------------------------
def move_player(matrix, direction):
    """
    Retourne une NOUVELLE matrice après déplacement.
    La matrice originale n'est jamais modifiée.
    Retourne aussi un booléen : True si le joueur a bougé.
    """
    matrix = deepcopy(matrix)

    # Trouver le joueur
    curr_x, curr_y = _find_player(matrix)
    if curr_x is None:
        return matrix, False

    dx, dy = DIRECTIONS.get(direction, (0, 0))
    nx, ny = curr_x + dx, curr_y + dy
    ax, ay = nx + dx, ny + dy

    rows, cols = len(matrix), len(matrix[0])

    if not (0 <= nx < rows and 0 <= ny < cols):
        return matrix, False
    if matrix[nx][ny] == WALL:
        return matrix, False

    target_cell = matrix[nx][ny]

    if target_cell in (EMPTY, TARGET):
        _update_cell(matrix, curr_x, curr_y, nx, ny)
        return matrix, True

    elif target_cell in (BOX, BOX_ON_TARGET):
        if not (0 <= ax < rows and 0 <= ay < cols):
            return matrix, False
        if matrix[ax][ay] in (EMPTY, TARGET):
            _push_box(matrix, nx, ny, ax, ay)
            _update_cell(matrix, curr_x, curr_y, nx, ny)
            return matrix, True

    return matrix, False


def _find_player(matrix):
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell in (PLAYER, PLAYER_ON_TARGET):
                return r, c
    return None, None


def _update_cell(matrix, x, y, nx, ny):
    matrix[x][y]   = TARGET if matrix[x][y] == PLAYER_ON_TARGET else EMPTY
    matrix[nx][ny] = PLAYER_ON_TARGET if matrix[nx][ny] == TARGET else PLAYER


def _push_box(matrix, nx, ny, ax, ay):
    matrix[ax][ay] = BOX_ON_TARGET if matrix[ax][ay] == TARGET else BOX


# ----------------------------------------------------------
#  Condition de victoire
# ----------------------------------------------------------
def is_solved(matrix):
    """Vrai si aucune caisse n'est hors cible."""
    return not any(BOX in row for row in matrix)


# ----------------------------------------------------------
#  Détection de deadlock (caisse coincée dans un coin)
# ----------------------------------------------------------
def has_deadlock(matrix):
    """
    Détecte les deadlocks simples : caisse dans un coin de murs
    alors qu'elle n'est pas sur une cible.
    """
    rows, cols = len(matrix), len(matrix[0])
    for r in range(rows):
        for c in range(cols):
            if matrix[r][c] == BOX:
                if _is_corner_deadlock(matrix, r, c, rows, cols):
                    return True
    return False


def _is_corner_deadlock(matrix, r, c, rows, cols):
    """Une caisse est en deadlock si elle est bloquée horizontalement ET verticalement."""
    blocked_up    = r == 0 or matrix[r-1][c] == WALL
    blocked_down  = r == rows-1 or matrix[r+1][c] == WALL
    blocked_left  = c == 0 or matrix[r][c-1] == WALL
    blocked_right = c == cols-1 or matrix[r][c+1] == WALL

    return (blocked_up or blocked_down) and (blocked_left or blocked_right)


# ----------------------------------------------------------
#  Chargement d'un niveau
# ----------------------------------------------------------
def _resolve_path(filename):
    """Résout le chemin relatif à l'emplacement de ce script (compatible Windows/Linux)."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Normalise les séparateurs (/ ou \) selon l'OS
    parts = filename.replace("\\", "/").split("/")
    return os.path.join(base_dir, *parts)


def load_level(filename):
    mapping = {
        '#': WALL, ' ': EMPTY, '$': BOX, '.': TARGET,
        '@': PLAYER, '*': BOX_ON_TARGET, '+': PLAYER_ON_TARGET,
    }
    filename = _resolve_path(filename.replace("/", os.sep))
    matrix = []
    try:
        with open(filename, 'r') as f:
            for line in f:
                row = [mapping[ch] for ch in line.rstrip('\n') if ch in mapping]
                if row:
                    matrix.append(row)
        max_w = max(len(r) for r in matrix)
        for r in matrix:
            while len(r) < max_w:
                r.append(EMPTY)
        return matrix
    except FileNotFoundError:
        print(f"Erreur : Le fichier '{filename}' est introuvable.")
        return None


# ----------------------------------------------------------
#  Métadonnées des niveaux par difficulté
# ----------------------------------------------------------
DIFFICULTY_LEVELS = {
    "Facile":    ["levels/level_easy_1.txt",   "levels/level_easy_2.txt",   "levels/level_easy_3.txt"],
    "Moyen":     ["levels/level_medium_1.txt",  "levels/level_medium_2.txt",  "levels/level_medium_3.txt"],
    "Difficile": ["levels/level_hard_1.txt",    "levels/level_hard_2.txt",    "levels/level_hard_3.txt"],
}