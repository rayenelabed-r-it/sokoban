# sokoban
Sokoban IA : Solveur Intelligent A* Ce projet est une implémentation du jeu classique Sokoban intégrant un moteur de résolution automatique basé sur l'algorithme de recherche A*. L'objectif est de démontrer l'efficacité des heuristiques dans la résolution de problèmes de planification de chemin complexes.

Architecture du Projet Le code est structuré de manière modulaire pour séparer la logique métier du rendu graphique :

main.py : Point d'entrée du programme. Il gère la boucle de jeu Pygame, les entrées utilisateur et orchestre l'appel au solveur A*.

build_game.py : Moteur physique du jeu. Contient les règles de collision, la gestion des poussées de caisses et le parseur de fichiers .txt pour les niveaux.

display_game.py : Gestionnaire de rendu graphique via Pygame.

Algorithme A* et Heuristique Le solveur utilise l'algorithme A* pour trouver le chemin optimal vers l'état final (toutes les caisses sur les cibles).

Fonction d'Évaluation L'IA calcule un score pour chaque mouvement : f(n) = g(n) + h(n)

g(n) : Le coût réel (nombre de pas déjà effectués).

h(n) : L'estimation de la distance restante via la Distance de Manhattan.

Optimisations Clés Évitement des cycles : Les configurations de grille déjà visitées sont stockées pour ne jamais calculer deux fois la même position.

Détection d'impossibilité : Si l'IA détecte un "Deadlock" (caisse bloquée dans un coin), elle arrête d'explorer cette branche.

📂 Gestion des Niveaux (.txt) Les niveaux sont chargés depuis le dossier /levels. Le format est le suivant :

: Mur
@ : Joueur

$ : Caisse

. : Cible
