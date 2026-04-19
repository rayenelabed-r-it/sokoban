# ============================================================
#  scores.py  –  Gestion des meilleurs scores (JSON)
# ============================================================
import json
import os

import os as _os
SCORES_FILE = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "scores.json")


def load_scores():
    """Retourne le dict des scores. Clé = chemin du niveau."""
    if os.path.exists(SCORES_FILE):
        try:
            with open(SCORES_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_scores(scores: dict):
    """Écrit le dict dans le fichier JSON."""
    try:
        with open(SCORES_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except IOError as e:
        print(f"Impossible de sauvegarder les scores : {e}")


def get_best(level_path: str) -> int | None:
    """Retourne le meilleur score (nb de coups) pour un niveau, ou None."""
    scores = load_scores()
    return scores.get(level_path)


def update_best(level_path: str, moves: int) -> bool:
    """
    Met à jour le meilleur score si moves est meilleur (moins).
    Retourne True si c'est un nouveau record.
    """
    scores = load_scores()
    prev   = scores.get(level_path)
    if prev is None or moves < prev:
        scores[level_path] = moves
        save_scores(scores)
        return True
    return False


def format_score(level_path: str) -> str:
    """Retourne une chaîne lisible pour le HUD."""
    best = get_best(level_path)
    return f"Record : {best} 🏆" if best is not None else "Record : —"