# ============================================================
#  solver.py  –  Solveur A* pour Sokoban
# ============================================================
import heapq
from copy import deepcopy
from build_game import move_player, BOX, TARGET, BOX_ON_TARGET, PLAYER_ON_TARGET, is_solved, has_deadlock


def heuristic(matrix):
    boxes, targets = [], []
    for r, row in enumerate(matrix):
        for c, cell in enumerate(row):
            if cell == BOX:
                boxes.append((r, c))
            if cell in (TARGET, BOX_ON_TARGET, PLAYER_ON_TARGET):
                targets.append((r, c))
    if not targets or not boxes:
        return 0
    return sum(min(abs(bx-tx)+abs(by-ty) for tx,ty in targets) for bx,by in boxes)


def matrix_hash(matrix):
    return tuple(tuple(row) for row in matrix)


def a_star_solver(initial_matrix):
    """
    Retourne la liste de directions qui résout le niveau, ou None.
    Intègre la détection de deadlock pour élaguer l'arbre de recherche.
    """
    start_h = heuristic(initial_matrix)
    queue = [(start_h, 0, initial_matrix, [])]
    visited = set()

    while queue:
        f, g, current, path = heapq.heappop(queue)

        state = matrix_hash(current)
        if state in visited:
            continue
        visited.add(state)

        if is_solved(current):
            return path

        for direction in ("UP", "DOWN", "LEFT", "RIGHT"):
            new_matrix, moved = move_player(current, direction)
            if not moved:
                continue
            new_state = matrix_hash(new_matrix)
            if new_state in visited:
                continue
            # Élagage : deadlock détecté → on n'explore pas cet état
            if has_deadlock(new_matrix):
                continue
            new_g = g + 1
            new_h = heuristic(new_matrix)
            heapq.heappush(queue, (new_g + new_h, new_g, new_matrix, path + [direction]))

    return None
