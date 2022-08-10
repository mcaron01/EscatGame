# Import des bibliothèques
import random
from random import randint
import PySimpleGUI as sg


def initialisation_nom_joueur():
    joueur1 = 'joueur1'
    joueur2 = 'joueur2'

    layout = [[sg.Text('Veuillez saisir vos noms de jeu', size=(30, 2))],
              [sg.Text('Joueur 1', size=(30, 2)), sg.InputText()],
              [sg.Text('Joueur 2', size=(30, 2)), sg.InputText()],
              [sg.Button('Ok'), sg.Button('Annuler')]]

    window = sg.Window('EscaT Game', layout=layout, size=(700, 150))

    while True:
        event, values = window.read()
        if values[0] != '':
            joueur1 = values[0]
        if values[1] != '':
            joueur2 = values[1]
        if event == sg.WIN_CLOSED or event == 'Annuler' or event == 'Ok':
            break

    window.close()

    return (joueur1, joueur2)


def initialisation_plateau(nb_lignes=11, nb_colonnes=11):
    """
    Paramètres:
    nb_lignes : nombre de lignes pour le plateau, par défaut 11
    nb_colonnes : nombre de colonnes pour le plateau, par defaut 11

    Fonction qui permet d'initialiser le plateau du jeu de la façon suivate:
    - La position initiale de ‘Chaf’, le chat en chef, est tiree aleatoirement, parmi les
    quatorze position de la zone d’apparition des chats
    - Les positions initiales des robots sont tirees aleatoirement à chaque debut de manche
    """

    # Création plateau
    plateau = [["" for i in range(nb_colonnes)] for i in range(nb_lignes)]

    # Ajout des sorties
    plateau[0][5] = "S"
    plateau[4][0] = "S"
    plateau[4][10] = "S"

    # Ajout des gardiens
    plateau[1][2], plateau[1][8] = "W", "W"

    # Ajout des obstacles
    plateau[2][4], plateau[2][5], plateau[2][6] = "O", "O", "O"
    plateau[3][4], plateau[3][5], plateau[3][6] = "O", "O", "O"

    # Ajout des chats
    randligne = randint(7, 10)
    randcol = randint(3, 7)
    plateau[7][5] = "C"
    plateau[8][4], plateau[8][5], plateau[8][6] = "C", "C", "C"
    plateau[9][3], plateau[9][4], plateau[9][5], plateau[9][6], plateau[9][7] = "C", "C", "C", "C", "C"
    plateau[10][3], plateau[10][4], plateau[10][5], plateau[10][6], plateau[10][7] = "C", "C", "C", "C", "C"

    # Ajout de 'Chaf' aléatoirement parmis les 14 chats
    while plateau[randligne][randcol] != "C":
        randligne = randint(7, 10)
        randcol = randint(3, 7)
    plateau[randligne][randcol] = "Ç"

    # Ajout des robots
    for i in range(9):
        randligne = randint(0, 10)
        randcol = randint(0, 10)
        while plateau[randligne][randcol] != "":
            randligne = randint(0, 10)
            randcol = randint(0, 10)
        plateau[randligne][randcol] = 'R'

    return plateau


def cases_disponibles_chats(plateau, ligne, colonne):
    liste_cases_disponibles = []

    ### Les mouvements possibles sont haut, bas, gauche, droit, haut-droite, haut-gauche, bas-droite, bas-gauche

    ## Haut
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if ligne != 0:
        if plateau[ligne - 1][colonne] == "" or plateau[ligne - 1][colonne] == "S":
            liste_cases_disponibles.append([ligne - 1, colonne])

    ## Bas
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if ligne != 10:
        if plateau[ligne + 1][colonne] == "" or plateau[ligne + 1][colonne] == "S":
            liste_cases_disponibles.append([ligne + 1, colonne])

    ## Gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    if colonne != 0:
        if plateau[ligne][colonne - 1] == "" or plateau[ligne][colonne - 1] == "S":
            liste_cases_disponibles.append([ligne, colonne - 1])

            ## Droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas se déplacer vers la droite
    if colonne != 10:
        if plateau[ligne][colonne + 1] == "" or plateau[ligne][colonne + 1] == "S":
            liste_cases_disponibles.append([ligne, colonne + 1])

            ## Haut-droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas de déplacer vers la droite
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if colonne != 10 and ligne != 0:
        if plateau[ligne - 1][colonne + 1] == "" or plateau[ligne - 1][colonne + 1] == "S":
            liste_cases_disponibles.append([ligne - 1, colonne + 1])

            ## Haut-gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if colonne != 0 and ligne != 0:
        if plateau[ligne - 1][colonne - 1] == "" or plateau[ligne - 1][colonne - 1] == "S":
            liste_cases_disponibles.append([ligne - 1, colonne - 1])

    ## Bas-droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas se déplacer vers la droite
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if colonne != 10 and ligne != 10:
        if plateau[ligne + 1][colonne + 1] == "" or plateau[ligne + 1][colonne + 1] == "S":
            liste_cases_disponibles.append([ligne + 1, colonne + 1])

    ## Bas-gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if colonne != 0 and ligne != 10:
        if plateau[ligne + 1][colonne - 1] == "" or plateau[ligne + 1][colonne - 1] == "S":
            liste_cases_disponibles.append([ligne + 1, colonne - 1])

    return liste_cases_disponibles


def cases_disponibles_chaf(plateau, ligne, colonne):
    liste_cases_disponibles = []

    ### Les mouvements possibles sont haut, bas, gauche, droit, haut-droite, haut-gauche, bas-droite, bas-gauche

    ## Haut
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if ligne != 0:
        if plateau[ligne - 1][colonne] == "" or plateau[ligne - 1][colonne] == "S":
            liste_cases_disponibles.append([ligne - 1, colonne])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne - 1][colonne] == "R":
            if ligne != 1 and plateau[ligne - 2][colonne] == "" or plateau[ligne - 2][colonne] == "S":
                liste_cases_disponibles.append([ligne - 2, colonne])

    ## Bas
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if ligne != 10:
        if plateau[ligne + 1][colonne] == "" or plateau[ligne + 1][colonne] == "S":
            liste_cases_disponibles.append([ligne + 1, colonne])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne + 1][colonne] == "R":
            if ligne != 9:
                if plateau[ligne + 2][colonne] == "" or plateau[ligne + 2][colonne] == "S":
                    liste_cases_disponibles.append([ligne + 2, colonne])

    ## Gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    if colonne != 0:
        if plateau[ligne][colonne - 1] == "" or plateau[ligne][colonne - 1] == "S":
            liste_cases_disponibles.append([ligne, colonne - 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne][colonne - 1] == "R":
            if colonne != 1:
                if plateau[ligne][colonne - 2] == "" or plateau[ligne][colonne - 2] == "S":
                    liste_cases_disponibles.append([ligne, colonne - 2])

    ## Droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas se déplacer vers la droite
    if colonne != 10:
        if plateau[ligne][colonne + 1] == "" or plateau[ligne][colonne + 1] == "S":
            liste_cases_disponibles.append([ligne, colonne + 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne][colonne + 1] == "R":
            if colonne != 9:
                if plateau[ligne][colonne + 2] == "" or plateau[ligne][colonne + 2] == "S":
                    liste_cases_disponibles.append([ligne, colonne + 2])

    ## Haut-droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas de déplacer vers la droite
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if colonne != 10 and ligne != 0:
        if plateau[ligne - 1][colonne + 1] == "" or plateau[ligne - 1][colonne + 1] == "S":
            liste_cases_disponibles.append([ligne - 1, colonne + 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne - 1][colonne + 1] == "R":
            if colonne != 9 and ligne != 1:
                if plateau[ligne - 2][colonne + 2] == "" or plateau[ligne - 2][colonne + 2] == "S":
                    liste_cases_disponibles.append([ligne - 2, colonne + 2])

    ## Haut-gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if colonne != 0 and ligne != 0:
        if plateau[ligne - 1][colonne - 1] == "" or plateau[ligne - 1][colonne - 1] == "S":
            liste_cases_disponibles.append([ligne - 1, colonne - 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne - 1][colonne - 1] == "R":
            if colonne != 1 and ligne != 1:
                if plateau[ligne - 2][colonne - 2] == "" or plateau[ligne - 2][colonne - 2] == "S":
                    liste_cases_disponibles.append([ligne - 2, colonne - 2])

    ## Bas-droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas se déplacer vers la droite
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if colonne != 10 and ligne != 10:
        if plateau[ligne + 1][colonne + 1] == "" or plateau[ligne + 1][colonne + 1] == "S":
            liste_cases_disponibles.append([ligne + 1, colonne + 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne + 1][colonne + 1] == "R":
            if colonne != 9 and ligne != 9:
                if plateau[ligne + 2][colonne + 2] == "" or plateau[ligne + 2][colonne + 2] == "S":
                    liste_cases_disponibles.append([ligne + 2, colonne + 2])

    ## Bas-gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if colonne != 0 and ligne != 10:
        if plateau[ligne + 1][colonne - 1] == "" or plateau[ligne + 1][colonne - 1] == "S":
            liste_cases_disponibles.append([ligne + 1, colonne - 1])
            # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne + 1][colonne - 1] == "R":
            if colonne != 1 and ligne != 9:
                if plateau[ligne + 2][colonne - 2] == "" or plateau[ligne + 2][colonne - 2] == "S":
                    liste_cases_disponibles.append([ligne + 2, colonne - 2])

    return liste_cases_disponibles


def cases_disponibles_robots(plateau, ligne, colonne):
    liste_cases_disponibles = []

    # La zone d'apparition des chats est interdite aux robots
    liste_cases_interdites = [[7, 5], [8, 4], [8, 5], [8, 6], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7], [10, 3], [10, 4],
                              [10, 5], [10, 6], [10, 7]]

    ### Les quatres mouvements possibles sont haut, bas, gauche, droit

    ## Haut
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if ligne != 0 and [ligne - 1, colonne] not in liste_cases_interdites:
        if plateau[ligne - 1][colonne] == "" or plateau[ligne - 1][colonne] == "C" or plateau[ligne - 1][
            colonne] == "Ç":
            liste_cases_disponibles.append([ligne - 1, colonne])

    ## Bas
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if ligne != 10 and [ligne + 1, colonne] not in liste_cases_interdites:
        if plateau[ligne + 1][colonne] == "" or plateau[ligne + 1][colonne] == "C" or plateau[ligne + 1][
            colonne] == "Ç":
            liste_cases_disponibles.append([ligne + 1, colonne])

    ## Gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    if colonne != 0 and [ligne, colonne - 1] not in liste_cases_interdites:
        if plateau[ligne][colonne - 1] == "" or plateau[ligne][colonne - 1] == "C" or plateau[ligne][
            colonne - 1] == "Ç":
            liste_cases_disponibles.append([ligne, colonne - 1])

    ## Droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas se déplacer vers la droite
    if colonne != 10 and [ligne, colonne + 1] not in liste_cases_interdites:
        if plateau[ligne][colonne + 1] == "" or plateau[ligne][colonne + 1] == "C" or plateau[ligne][
            colonne + 1] == "Ç":
            liste_cases_disponibles.append([ligne, colonne + 1])

    return liste_cases_disponibles


def cases_disponibles_gardien(plateau, ligne, colonne):
    liste_cases_disponibles = []

    # La zone d'apparition des chats est interdite aux robots
    liste_cases_interdites = [[7, 5], [8, 4], [8, 5], [8, 6], [9, 3], [9, 4], [9, 5], [9, 6], [9, 7], [10, 3], [10, 4],
                              [10, 5], [10, 6], [10, 7]]

    ### Les mouvements possibles sont haut, bas, gauche, droit, haut-droite, haut-gauche, bas-droite, bas-gauche

    ## Haut
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if ligne != 0 and [ligne - 1, colonne] not in liste_cases_interdites:
        if plateau[ligne - 1][colonne] == "" or plateau[ligne - 1][colonne] == "C" or plateau[ligne - 1][
            colonne] == "Ç":
            liste_cases_disponibles.append([ligne - 1, colonne])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne - 1][colonne] == "R":
            if ligne != 1 and [ligne - 2, colonne] not in liste_cases_interdites:
                if plateau[ligne - 2][colonne] == "" or plateau[ligne - 2][colonne] == "C" or plateau[ligne - 2][
                    colonne] == "Ç":
                    liste_cases_disponibles.append([ligne - 2, colonne])

    ## Bas
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if ligne != 10 and [ligne + 1, colonne] not in liste_cases_interdites:
        if plateau[ligne + 1][colonne] == "" or plateau[ligne + 1][colonne] == "C" or plateau[ligne + 1][
            colonne] == "Ç":
            liste_cases_disponibles.append([ligne + 1, colonne])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne + 1][colonne] == "R":
            if ligne != 9 and [ligne + 2, colonne] not in liste_cases_interdites:
                if plateau[ligne + 2][colonne] == "" or plateau[ligne + 2][colonne] == "C" or plateau[ligne + 2][
                    colonne] == "Ç":
                    liste_cases_disponibles.append([ligne + 2, colonne])

    ## Gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    if colonne != 0 and [ligne, colonne - 1] not in liste_cases_interdites:
        if plateau[ligne][colonne - 1] == "" or plateau[ligne][colonne - 1] == "C" or plateau[ligne][
            colonne - 1] == "Ç":
            liste_cases_disponibles.append([ligne, colonne - 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne][colonne - 1] == "R":
            if colonne != 1 and [ligne, colonne - 2] not in liste_cases_interdites:
                if plateau[ligne][colonne - 2] == "" or plateau[ligne][colonne - 2] == "C" or plateau[ligne][
                    colonne - 2] == "Ç":
                    liste_cases_disponibles.append([ligne, colonne - 2])

    ## Droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas se déplacer vers la droite
    if colonne != 10 and [ligne, colonne + 1] not in liste_cases_interdites:
        if plateau[ligne][colonne + 1] == "" or plateau[ligne][colonne + 1] == "C" or plateau[ligne][
            colonne + 1] == "Ç":
            liste_cases_disponibles.append([ligne, colonne + 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne][colonne + 1] == "R":
            if colonne != 9 and [ligne, colonne + 2] not in liste_cases_interdites:
                if plateau[ligne][colonne + 2] == "" or plateau[ligne][colonne + 2] == "C" or plateau[ligne][
                    colonne + 2] == "Ç":
                    liste_cases_disponibles.append([ligne, colonne + 2])

    ## Haut-droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas de déplacer vers la droite
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if colonne != 10 and ligne != 0 and [ligne - 1, colonne + 1] not in liste_cases_interdites:
        if plateau[ligne - 1][colonne + 1] == "" or plateau[ligne - 1][colonne + 1] == "C" or plateau[ligne - 1][
            colonne + 1] == "Ç":
            liste_cases_disponibles.append([ligne - 1, colonne + 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne - 1][colonne + 1] == "R":
            if colonne != 9 and ligne != 1 and [ligne - 2, colonne + 2] not in liste_cases_interdites:
                if plateau[ligne - 2][colonne + 2] == "" or plateau[ligne - 2][colonne + 2] == "C" or \
                        plateau[ligne - 2][colonne + 2] == "Ç":
                    liste_cases_disponibles.append([ligne - 2, colonne + 2])

    ## Haut-gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    # Si on est sur la ligne 1, on ne peut pas se déplacer vers le haut
    if colonne != 0 and ligne != 0 and [ligne - 1, colonne - 1] not in liste_cases_interdites:
        if plateau[ligne - 1][colonne - 1] == "" or plateau[ligne - 1][colonne - 1] == "C" or plateau[ligne - 1][
            colonne - 1] == "Ç":
            liste_cases_disponibles.append([ligne - 1, colonne - 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne - 1][colonne - 1] == "R":
            if colonne != 1 and ligne != 1 and [ligne - 2, colonne - 2] not in liste_cases_interdites:
                if plateau[ligne - 2][colonne - 2] == "" or plateau[ligne - 2][colonne - 2] == "C" or \
                        plateau[ligne - 2][colonne - 2] == "Ç":
                    liste_cases_disponibles.append([ligne - 2, colonne - 2])

    ## Bas-droite
    # Si on est sur la colonne K (colonne 11), on ne peut pas se déplacer vers la droite
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if colonne != 10 and ligne != 10 and [ligne + 1, colonne + 1] not in liste_cases_interdites:
        if plateau[ligne + 1][colonne + 1] == "" or plateau[ligne + 1][colonne + 1] == "C" or plateau[ligne + 1][
            colonne + 1] == "Ç":
            liste_cases_disponibles.append([ligne + 1, colonne + 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne + 1][colonne + 1] == "R":
            if colonne != 9 and ligne != 9 and [ligne + 2, colonne + 2] not in liste_cases_interdites:
                if plateau[ligne + 2][colonne + 2] == "" or plateau[ligne + 2][colonne + 2] == "C" or \
                        plateau[ligne + 2][colonne + 2] == "Ç":
                    liste_cases_disponibles.append([ligne + 2, colonne + 2])

    ## Bas-gauche
    # Si on est sur la colonne A (colonne 1), on ne peut pas se déplacer vers la gauche
    # Si on est sur la ligne 11, on ne peut pas se déplacer vers le bas
    if colonne != 0 and ligne != 10 and [ligne + 1, colonne - 1] not in liste_cases_interdites:
        if plateau[ligne + 1][colonne - 1] == "" or plateau[ligne + 1][colonne - 1] == "C" or plateau[ligne + 1][
            colonne - 1] == "Ç":
            liste_cases_disponibles.append([ligne + 1, colonne - 1])
        # Si c'est un robot, on regarde si on peut sauter par dessus
        if plateau[ligne + 1][colonne - 1] == "R":
            if colonne != 1 and ligne != 9 and [ligne + 2, colonne - 2] not in liste_cases_interdites:
                if plateau[ligne + 2][colonne - 2] == "" or plateau[ligne + 2][colonne - 2] == "C" or \
                        plateau[ligne + 2][colonne - 2] == "Ç":
                    liste_cases_disponibles.append([ligne + 2, colonne - 2])

    return liste_cases_disponibles


def afficher_score(scorej1, joueur1, scorej2, joueur2):
    if scorej1 > scorej2:
        layout = [[sg.Text(joueur1 + ' a gagné', size=(30, 2))],
                  [sg.Text('Bravo !', size=(30, 2))]]
    elif scorej1 < scorej2:
        layout = [[sg.Text(joueur2 + ' a gagné', size=(30, 2))],
                  [sg.Text('Bravo !', size=(30, 2))]]
    else:
        layout = [[sg.Text('Il y a égalité', size=(30, 2))],
                  [sg.Text('Bravo aux deux joueurs !', size=(30, 2))]]

    # Creation de la fenetre pour la manche 1
    window = sg.Window('Résultats EscaT Game', layout=layout, size=(700, 150))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break

    # Fermeture de la fenetre
    window.close()


def main():
    # Choix pseudonyme des deux joueurs
    joueur1, joueur2 = initialisation_nom_joueur()

    # Parametres scores,chats_evades,chats_capturés
    score_j1 = 0
    score_j2 = 0
    chats_cap_j1 = 0
    chats_cap_j2 = 0
    chats_eva_j1 = 0
    chats_eva_j2 = 0

    # Lancement de la première manche

    nb_lignes = 11
    nb_colonnes = 11
    plateau = initialisation_plateau(nb_lignes, nb_colonnes)
    Nb_cat = 14
    manche_1_commence = False
    case_gardien = [[1, 2], [1, 8]]
    ligne, colonne = 0, 0

    layout = [[[sg.Text(joueur1, size=(15, 1)), sg.Text('Chat évadés'), sg.Text(0, key='-CHATSEVADESJ1-'),
                sg.Text('Chat capturés'), sg.Text(0, key='-CHATSCAPTURESJ1-'), sg.Text('Score'),
                sg.Text(0, key='-SCOREJ1-')],
               [sg.Text(joueur2, size=(15, 1)), sg.Text('Chat évadés'), sg.Text(0, key='-CHATSEVADESJ2-'),
                sg.Text('Chat capturés'), sg.Text(0, key='-CHATSCAPTURESJ2-'), sg.Text('Score'),
                sg.Text(0, key='-SCOREJ2-')],
               [sg.Text('Tour de '), sg.Text(key='-TOURJOUEUR-')],
               [sg.Button('Commencer la premiere manche'), sg.Button('annuler')]],
              [[sg.Button(plateau[i][j], button_color=('black'), size=(8, 4), key=(i, j),
                          pad=(0, 0)) for j in range(nb_colonnes)] for i in range(nb_lignes)]]

    # Creation de la fenetre pour la manche 1
    window = sg.Window('EscaT Game', layout=layout, size=(1000, 1000))

    ### Boucle de gestion des evenements

    ## On effecture le premier tour
    while manche_1_commence != True:
        # Lecture du dernier evenement
        event, values = window.read()
        # Dans ce cas, il faut lancer la manche avec le bouton 'Commencer la première manche'
        if event == 'Commencer la premiere manche':
            # On note que la manche est commence
            manche_1_commence = True
            window['Commencer la premiere manche'].Update("Premiere manche en cours")
            sg.Popup("Début de la première manche")

            ## Coloration du plateau
            # Coloration des cases contenant des chats
            for i in range(7, 11):
                for j in range(3, 8):
                    if plateau[i][j] == "C" or plateau[i][j] == "Ç":
                        window[i, j].Update(button_color=('black', 'NavajoWhite3'))

            # Coloration des cases obstacles (eau)
            for i in range(2, 4):
                for j in range(4, 7):
                    if plateau[i][j] == "O":
                        window[i, j].Update(button_color=('blue'))

            # Coloration des cases sorties
            window[0, 5].Update(button_color=('black', 'white'))
            window[4, 0].Update(button_color=('black', 'white'))
            window[4, 10].Update(button_color=('black', 'white'))

            # Coloration des cases gardiens
            window[1, 2].Update(button_color=('black', 'yellow'))
            window[1, 8].Update(button_color=('black', 'yellow'))

            ### Au tour de joueur 1 de commencer
            sg.Popup('Tour de joueur 1, appuie sur la case du chat que tu veux déplacer')
            window['-TOURJOUEUR-'].Update(joueur1)

            ## Déplacements des chats

            # On crée une variable pour stocker les chats déplacés
            chats_deplaces_ce_tour = []

            # Le joueur peut deplacer jusqu'a 7 chats
            if Nb_cat >= 7:
                nb_chat_limite = 7
            else:
                nb_chat_limite = Nb_cat

            # On crée une variable qui prend le nombre de chats moins 7 (cette variable servira
            # si jamais un joueur possède encore plus de 7 chats et qu'il clique sur un chat
            # qui ne peut pas être déplacé)
            nb_chats_moins_sept = Nb_cat - 7

            # Pour le nombre de chats qu'il reste à deplacer
            while len(chats_deplaces_ce_tour) < nb_chat_limite:
                # On choisit un chat
                event, values = window.read()
                ligne, colonne = event[0], event[1]

                # On regarde qu'il s'agit bien d'un chat et qu'il n'a pas été deja deplacé
                if ((plateau[ligne][colonne] == "C" or plateau[ligne][colonne] == 'Ç') and [ligne,
                                                                                            colonne] not in chats_deplaces_ce_tour):

                    # On regarde les cases dispo autour de ce chat
                    if plateau[ligne][colonne] == "C":
                        case_dispo = cases_disponibles_chats(plateau, ligne, colonne)
                    else:
                        case_dispo = cases_disponibles_chaf(plateau, ligne, colonne)

                    # S'il n'y a pas de case disponibles, on le fait remonter au joueur
                    if case_dispo == []:
                        sg.Popup('Vous ne pouvez pas déplacer ce chat')
                        # Si nb_chats_moins_sept est inférieur ou égale à 0 alors cela veut dire qu'il n'a pas d'autre occasion de deplacer un chat
                        if nb_chats_moins_sept <= 0:
                            # On ajoute donc le chat à la liste des chats déplacés ce tour
                            chats_deplaces_ce_tour.append([ligne, colonne])
                        else:
                            nb_chats_moins_sept -= 1

                    # S'il y a une case disponible
                    else:
                        # On affiche en rouge les cases disponibles
                        for el in case_dispo:
                            window[el[0], el[1]].Update(button_color=('black', 'red'))
                        # On recupere une nouvelle action de la part du joueur
                        event, values = window.read()
                        new_ligne, new_colonne = event[0], event[1]
                        # On vérifie que cette action soit bien possible
                        if [new_ligne, new_colonne] in case_dispo:
                            # On regarde si cette case est une sortie ou non
                            if plateau[new_ligne][new_colonne] == 'S':
                                # On met a jour les chats deplacés ce tour (on met 1000,1000 car sinon ca bloque la case sortie)
                                chats_deplaces_ce_tour.append([1000, 1000])

                                # On met à jour les scores
                                chats_eva_j1 += 1
                                window['-CHATSEVADESJ1-'].Update(chats_eva_j1)
                                # Si c'est un chat "classique", +1 point
                                if plateau[ligne][colonne] == "C":
                                    score_j1 += 1
                                    window['-SCOREJ1-'].Update(score_j1)
                                # Sinon 'est 'Chaf', +5 points
                                else:
                                    score_j1 += 5
                                    window['-SCOREJ1-'].Update(score_j1)

                                # On retire un chat du plateau
                                Nb_cat -= 1
                                plateau[ligne][colonne] = ""

                                ## On remet les couleurs à jour
                                # Le chat laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne],
                                                              button_color=('NavajoWhite3', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo:
                                    # Si c'était une sortie, on remet la case blanche
                                    if plateau[el[0]][el[1]] == "S":
                                        window[el[0], el[1]].Update(button_color=('red', 'white'))
                                    # Sinon c'est une case vide
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))

                            else:
                                # On déplace le chat
                                plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                                plateau[ligne][colonne] = ""

                                # On met a jour les chats deplacés ce tour
                                chats_deplaces_ce_tour.append([new_ligne, new_colonne])

                                ## On remet les couleurs à jour
                                # Le chat laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne],
                                                              button_color=('NavajoWhite3', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo:
                                    # Si c'était une sortie, on remet la case blanche
                                    if plateau[el[0]][el[1]] == "S":
                                        window[el[0], el[1]].Update(button_color=('red', 'white'))
                                    # Sinon c'est une case vide
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))

                                # On met à jour la couleur de la nouvelle case qui contient le chat
                                window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                      button_color=('red', 'NavajoWhite3'))

                        else:
                            sg.Popup('Vous ne pouvez pas déplacer ce chat ici !')
                            ## On remet les couleurs à jour

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo:
                                # Si c'était une sortie, on remet la case blanche
                                if plateau[el[0]][el[1]] == "S":
                                    window[el[0], el[1]].Update(button_color=('red', 'white'))
                                # Sinon c'est une case vide
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))



                # Si le joueur ne selectionne pas un chat ou qu'il selectionne un chat deja deplace ce tour
                else:
                    if [ligne, colonne] in chats_deplaces_ce_tour:
                        sg.Popup("Vous avez déja deplacé ce chat ce tour !")
                    else:
                        sg.Popup("Ceci n'est pas un chat !")

            ### Déplacements gardiens

            sg.Popup('Tour de joueur 2, appuie sur les gardiens pour les deplacer')
            window['-TOURJOUEUR-'].Update(joueur2)

            # On recupère le placement des gardiens
            gardien_restants_a_deplacer = list(case_gardien)
            while gardien_restants_a_deplacer != []:
                event, values = window.read()
                ligne, colonne = event[0], event[1]

                if [ligne, colonne] in gardien_restants_a_deplacer:

                    # On regarde les cases dispo autour de ce chat
                    case_dispo_gardien = cases_disponibles_gardien(plateau, ligne, colonne)
                    # S'il n'y a pas de case disponibles, on fait remonter au joueur que le gardien ne peut pas être deplacé
                    if case_dispo == []:
                        sg.Popup('Ce gardien ne peut pas être deplacé ce tour-ci')
                        # On supprime donc ce gardien de la liste des gardiens à deplacer
                        gardien_restants_a_deplacer.remove([ligne, colonne])

                    # Déplacement du gardien
                    else:
                        # On affiche en rouge les cases disponibles
                        for el in case_dispo_gardien:
                            window[el[0], el[1]].Update(button_color=('black', 'red'))
                        # On recupere une nouvelle action de la part du joueur
                        event, values = window.read()
                        new_ligne, new_colonne = event[0], event[1]
                        # On vérifie que cette action soit bien possible
                        if [new_ligne, new_colonne] in case_dispo_gardien:
                            # On regarde si cette case est un chat ou non
                            if plateau[new_ligne][new_colonne] == 'C' or plateau[new_ligne][new_colonne] == 'Ç':
                                # On déplace le gardien sur la case du chat
                                plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                                plateau[ligne][colonne] = ""
                                window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                      button_color=('NavajoWhite3', 'yellow'))

                                # On met a jour les cases gardiens
                                case_gardien.remove([ligne, colonne])
                                case_gardien.append([new_ligne, new_colonne])
                                gardien_restants_a_deplacer.remove([ligne, colonne])

                                # On retire un chat du plateau
                                Nb_cat -= 1

                                # On met à jour les scores
                                chats_cap_j2 += 1
                                window['-CHATSCAPTURESJ2-'].Update(chats_cap_j2)

                                ## On remet les couleurs à jour
                                # Le gardien laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo_gardien:
                                    # On prend les cases qui n'ont pas été selectionnées
                                    if el != [new_ligne, new_colonne]:
                                        # On regarde si c'est une case vide, sinon c'est un chat
                                        if plateau[el[0]][el[1]] == "":
                                            window[el[0], el[1]].Update(button_color=('red', 'black'))
                                        else:
                                            window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                            else:
                                # On déplace le gardien sur une case vide
                                plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                                plateau[ligne][colonne] = ""
                                window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                      button_color=('black', 'yellow'))

                                # On met a jour les cases gardiens
                                case_gardien.remove([ligne, colonne])
                                case_gardien.append([new_ligne, new_colonne])
                                gardien_restants_a_deplacer.remove([ligne, colonne])

                                ## On remet les couleurs à jour
                                # Le gardien laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo_gardien:
                                    # On prend les cases qui n'ont pas été selectionnées
                                    if el != [new_ligne, new_colonne]:
                                        # On regarde si c'est une case vide, sinon c'est un chat
                                        if plateau[el[0]][el[1]] == "":
                                            window[el[0], el[1]].Update(button_color=('red', 'black'))
                                        else:
                                            window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                        else:
                            sg.Popup('Vous ne pouvez pas déplacer le gardien ici !')
                            ## On remet les couleurs à jour
                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo_gardien:
                                # On regarde si c'est une case vide, sinon c'est un chat
                                if plateau[el[0]][el[1]] == "":
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))
                else:
                    sg.Popup("Ceci n'est pas un gardien ou ce gardien a déjà été déplacé")

            ### Déplacements des robots
            for k in range(nb_lignes):
                for l in range(nb_colonnes):
                    if plateau[k][l] == "R":
                        # On génére un nombre aléatoire entre 0 et 1
                        temp_aleatoire = random.random()
                        # Les robots ont une chance sur trois de se déplacer
                        if temp_aleatoire < 1 / 3:
                            # On regarde les cases disponibles autours du robot
                            case_dispo_robot = cases_disponibles_robots(plateau, k, l)

                            # S'il n'y a pas de cases disponibles, on ne déplace pas le robot
                            if case_dispo_robot == []:
                                pass
                            else:
                                # On choisit une case dispo aléatoirement
                                temp_case_choisie = random.randint(0, len(case_dispo_robot) - 1)
                                case_choisie = case_dispo_robot[temp_case_choisie]

                                ## On déplace le robot sur cette case choisie

                                # Si cette case est un chat, alors on l'attrape
                                if plateau[case_choisie[0]][case_choisie[1]] == "C" or plateau[case_choisie[0]][
                                    case_choisie[1]] == 'Ç':
                                    # On retire un chat du plateau
                                    Nb_cat -= 1

                                    # On déplace le robot sur cette case
                                    plateau[case_choisie[0]][case_choisie[1]] = "R"
                                    plateau[k][l] = ""

                                    # On met a jour l'affichage
                                    window[k, l].Update(plateau[k][l])
                                    window[case_choisie[0], case_choisie[1]].Update(
                                        plateau[case_choisie[0]][case_choisie[1]],
                                        button_color=('NavajoWhite3', 'black'))

                                    # On met à jour les scores
                                    chats_cap_j2 += 1
                                    window['-CHATSCAPTURESJ2-'].Update(chats_cap_j2)

                                # Si le robot se déplace juste vers une case vide
                                else:
                                    # On déplace le robot sur cette case
                                    plateau[case_choisie[0]][case_choisie[1]] = "R"
                                    plateau[k][l] = ""

                                    # On met a jour l'affichage
                                    window[k, l].Update(plateau[k][l])
                                    window[case_choisie[0], case_choisie[1]].Update(
                                        plateau[case_choisie[0]][case_choisie[1]],
                                        button_color=('NavajoWhite3', 'black'))
                        else:
                            pass

        else:
            # arrete la boucle quand on ferme la fenetre
            if event == sg.WIN_CLOSED:
                break
            sg.Popup("Veuillez appuyer sur le bouton 'Commencer la premiere manche'")

            ### Boucle de gestion des evenements

    ## On continue la partie jusqu'a qu'il y ait plus de chat sur le plateau
    while Nb_cat != 0:
        ### Au tour de joueur 1 de commencer
        sg.Popup('Tour de joueur 1, appuie sur la case du chat que tu veux déplacer')
        window['-TOURJOUEUR-'].Update(joueur1)

        ## Déplacements des chats

        # On crée une variable pour stocker les chats déplacés
        chats_deplaces_ce_tour = []

        # Le joueur peut deplacer jusqu'a 7 chats
        if Nb_cat >= 7:
            nb_chat_limite = 7
        else:
            nb_chat_limite = Nb_cat

        # On crée une variable qui prend le nombre de chats moins 7 (cette variable servira
        # si jamais un joueur possède encore plus de 7 chats et qu'il clique sur un chat
        # qui ne peut pas être déplacé)
        nb_chats_moins_sept = Nb_cat - 7

        # Pour le nombre de chats qu'il reste à deplacer
        while len(chats_deplaces_ce_tour) < nb_chat_limite:
            # On choisit un chat
            event, values = window.read()
            ligne, colonne = event[0], event[1]

            # On regarde qu'il s'agit bien d'un chat et qu'il n'a pas été deja deplacé
            if ((plateau[ligne][colonne] == "C" or plateau[ligne][colonne] == 'Ç') and [ligne,
                                                                                        colonne] not in chats_deplaces_ce_tour):

                # On regarde les cases dispo autour de ce chat
                if plateau[ligne][colonne] == "C":
                    case_dispo = cases_disponibles_chats(plateau, ligne, colonne)
                else:
                    case_dispo = cases_disponibles_chaf(plateau, ligne, colonne)
                # S'il n'y a pas de case disponibles, on le fait remonter au joueur
                if case_dispo == []:
                    sg.Popup('Vous ne pouvez pas déplacer ce chat')
                    # Si nb_chats_moins_sept est inférieur ou égale à 0 alors cela veut dire qu'il n'a pas d'autre occasion de deplacer un chat
                    if nb_chats_moins_sept <= 0:
                        # On ajoute donc le chat à la liste des chats déplacés ce tour
                        chats_deplaces_ce_tour.append([ligne, colonne])
                    else:
                        nb_chats_moins_sept -= 1

                # S'il y a une case disponible
                else:
                    # On affiche en rouge les cases disponibles
                    for el in case_dispo:
                        window[el[0], el[1]].Update(button_color=('black', 'red'))
                    # On recupere une nouvelle action de la part du joueur
                    event, values = window.read()
                    new_ligne, new_colonne = event[0], event[1]
                    # On vérifie que cette action soit bien possible
                    if [new_ligne, new_colonne] in case_dispo:
                        # On regarde si cette case est une sortie ou non
                        if plateau[new_ligne][new_colonne] == 'S':
                            # On met a jour les chats deplacés ce tour (on met 1000,1000 car sinon ca bloque la case sortie)
                            chats_deplaces_ce_tour.append([1000, 1000])

                            # On met à jour les scores
                            chats_eva_j1 += 1
                            window['-CHATSEVADESJ1-'].Update(chats_eva_j1)
                            # Si c'est un chat "classique", +1 point
                            if plateau[ligne][colonne] == "C":
                                score_j1 += 1
                                window['-SCOREJ1-'].Update(score_j1)
                            # Sinon c'est 'Chaf', +5 points
                            else:
                                score_j1 += 5
                                window['-SCOREJ1-'].Update(score_j1)

                            # On retire un chat du plateau
                            Nb_cat -= 1
                            plateau[ligne][colonne] = ""

                            ## On remet les couleurs à jour
                            # Le chat laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne],
                                                          button_color=('NavajoWhite3', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo:
                                # Si c'était une sortie, on remet la case blanche
                                if plateau[el[0]][el[1]] == "S":
                                    window[el[0], el[1]].Update(button_color=('red', 'white'))
                                # Sinon c'est une case vide
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))

                        else:
                            # On déplace le chat
                            plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                            plateau[ligne][colonne] = ""

                            # On met a jour les chats deplacés ce tour
                            chats_deplaces_ce_tour.append([new_ligne, new_colonne])

                            ## On remet les couleurs à jour
                            # Le chat laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne],
                                                          button_color=('NavajoWhite3', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo:
                                # Si c'était une sortie, on remet la case blanche
                                if plateau[el[0]][el[1]] == "S":
                                    window[el[0], el[1]].Update(button_color=('red', 'white'))
                                # Sinon c'est une case vide
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))

                            # On met à jour la couleur de la nouvelle case qui contient le chat
                            window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                  button_color=('red', 'NavajoWhite3'))

                    else:
                        sg.Popup('Vous ne pouvez pas déplacer ce chat ici !')
                        ## On remet les couleurs à jour

                        # On remet les cases rouges dans leurs bonnes couleurs
                        for el in case_dispo:
                            # Si c'était une sortie, on remet la case blanche
                            if plateau[el[0]][el[1]] == "S":
                                window[el[0], el[1]].Update(button_color=('red', 'white'))
                            # Sinon c'est une case vide
                            else:
                                window[el[0], el[1]].Update(button_color=('red', 'black'))



            # Si le joueur ne selectionne pas un chat ou qu'il selectionne un chat deja deplace ce tour
            else:
                if [ligne, colonne] in chats_deplaces_ce_tour:
                    sg.Popup("Vous avez déja deplacé ce chat ce tour !")
                elif event == sg.WIN_CLOSED:
                    break
                else:
                    sg.Popup("Ceci n'est pas un chat !")

        ### Déplacements gardiens

        sg.Popup('Tour de joueur 2, appuie sur les gardiens pour les deplacer')
        window['-TOURJOUEUR-'].Update(joueur2)

        # On recupère le placement des gardiens
        gardien_restants_a_deplacer = list(case_gardien)
        while gardien_restants_a_deplacer != []:
            event, values = window.read()
            ligne, colonne = event[0], event[1]

            if [ligne, colonne] in gardien_restants_a_deplacer:

                # On regarde les cases dispo autour de ce chat
                case_dispo_gardien = cases_disponibles_gardien(plateau, ligne, colonne)
                # S'il n'y a pas de case disponibles, on fait remonter au joueur que le gardien ne peut pas être deplacé
                if case_dispo == []:
                    sg.Popup('Ce gardien ne peut pas être deplacé ce tour-ci')
                    # On supprime donc ce gardien de la liste des gardiens à deplacer
                    gardien_restants_a_deplacer.remove([ligne, colonne])

                # Déplacement du gardien
                else:
                    # On affiche en rouge les cases disponibles
                    for el in case_dispo_gardien:
                        window[el[0], el[1]].Update(button_color=('black', 'red'))
                    # On recupere une nouvelle action de la part du joueur
                    event, values = window.read()
                    new_ligne, new_colonne = event[0], event[1]
                    # On vérifie que cette action soit bien possible
                    if [new_ligne, new_colonne] in case_dispo_gardien:
                        # On regarde si cette case est un chat ou non
                        if plateau[new_ligne][new_colonne] == 'C' or plateau[new_ligne][new_colonne] == 'Ç':
                            # On déplace le gardien sur la case du chat
                            plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                            plateau[ligne][colonne] = ""
                            window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                  button_color=('NavajoWhite3', 'yellow'))

                            # On met a jour les cases gardiens
                            case_gardien.remove([ligne, colonne])
                            case_gardien.append([new_ligne, new_colonne])
                            gardien_restants_a_deplacer.remove([ligne, colonne])

                            # On retire un chat du plateau
                            Nb_cat -= 1

                            # On met à jour les scores
                            chats_cap_j2 += 1
                            window['-CHATSCAPTURESJ2-'].Update(chats_cap_j2)

                            ## On remet les couleurs à jour
                            # Le gardien laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo_gardien:
                                # On prend les cases qui n'ont pas été selectionnées
                                if el != [new_ligne, new_colonne]:
                                    # On regarde si c'est une case vide, sinon c'est un chat
                                    if plateau[el[0]][el[1]] == "":
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                        else:
                            # On déplace le gardien sur une case vide
                            plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                            plateau[ligne][colonne] = ""
                            window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                  button_color=('black', 'yellow'))

                            # On met a jour les cases gardiens
                            case_gardien.remove([ligne, colonne])
                            case_gardien.append([new_ligne, new_colonne])
                            gardien_restants_a_deplacer.remove([ligne, colonne])

                            ## On remet les couleurs à jour
                            # Le gardien laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo_gardien:
                                # On prend les cases qui n'ont pas été selectionnées
                                if el != [new_ligne, new_colonne]:
                                    # On regarde si c'est une case vide, sinon c'est un chat
                                    if plateau[el[0]][el[1]] == "":
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                    else:
                        sg.Popup('Vous ne pouvez pas déplacer le gardien ici !')
                        ## On remet les couleurs à jour
                        # On remet les cases rouges dans leurs bonnes couleurs
                        for el in case_dispo_gardien:
                            # On regarde si c'est une case vide, sinon c'est un chat
                            if plateau[el[0]][el[1]] == "":
                                window[el[0], el[1]].Update(button_color=('red', 'black'))
                            else:
                                window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))
            else:
                if event == sg.WIN_CLOSED:
                    break
                else:
                    sg.Popup("Ceci n'est pas un gardien ou ce gardien a déjà été déplacé")

        ### Déplacements des robots
        for k in range(nb_lignes):
            for l in range(nb_colonnes):
                if plateau[k][l] == "R":
                    # On génére un nombre aléatoire entre 0 et 1
                    temp_aleatoire = random.random()
                    # Les robots ont une chance sur trois de se déplacer
                    if temp_aleatoire < 1 / 3:
                        # On regarde les cases disponibles autours du robot
                        case_dispo_robot = cases_disponibles_robots(plateau, k, l)

                        # S'il n'y a pas de cases disponibles, on ne déplace pas le robot
                        if case_dispo_robot == []:
                            pass
                        else:
                            # On choisit une case dispo aléatoirement
                            temp_case_choisie = random.randint(0, len(case_dispo_robot) - 1)
                            case_choisie = case_dispo_robot[temp_case_choisie]

                            ## On déplace le robot sur cette case choisie

                            # Si cette case est un chat, alors on l'attrape
                            if plateau[case_choisie[0]][case_choisie[1]] == "C" or plateau[case_choisie[0]][
                                case_choisie[1]] == 'Ç':
                                # On retire un chat du plateau
                                Nb_cat -= 1

                                # On déplace le robot sur cette case
                                plateau[case_choisie[0]][case_choisie[1]] = "R"
                                plateau[k][l] = ""

                                # On met a jour l'affichage
                                window[k, l].Update(plateau[k][l])
                                window[case_choisie[0], case_choisie[1]].Update(
                                    plateau[case_choisie[0]][case_choisie[1]], button_color=('NavajoWhite3', 'black'))

                                # On met à jour les scores
                                chats_cap_j2 += 1
                                window['-CHATSCAPTURESJ2-'].Update(chats_cap_j2)

                            # Si le robot se déplace juste vers une case vide
                            else:
                                # On déplace le robot sur cette case
                                plateau[case_choisie[0]][case_choisie[1]] = "R"
                                plateau[k][l] = ""

                                # On met a jour l'affichage
                                window[k, l].Update(plateau[k][l])
                                window[case_choisie[0], case_choisie[1]].Update(
                                    plateau[case_choisie[0]][case_choisie[1]], button_color=('NavajoWhite3', 'black'))
                    else:
                        pass

    # Fin de la première manche, début de la second manche
    update_button_premiere_manche = False
    while True:
        if update_button_premiere_manche == False:
            # Premiere manche en cours
            window["Commencer la premiere manche"].Update("Commencer la seconde manche")
            update_button_premiere_manche = True
        sg.Popup("Fin de la première manche, veuillez fermer la fenetre pour lancer la seconde manche")
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Commencer la premiere manche":
            break

    window.close()  # Destruction de la fenetre

    ##### Deuxième manche

    # Génération du deuxième plateau de jeu pour la second manche
    plateau = initialisation_plateau(nb_lignes, nb_colonnes)
    Nb_cat = 14
    manche_2_commence = False
    case_gardien = [[1, 2], [1, 8]]
    ligne, colonne = 0, 0

    layout = [[[sg.Text(joueur1, size=(15, 1)), sg.Text('Chat évadés'), sg.Text(chats_eva_j1, key='-CHATSEVADESJ1-'),
                sg.Text('Chat capturés'), sg.Text(chats_cap_j1, key='-CHATSCAPTURESJ1-'), sg.Text('Score'),
                sg.Text(score_j1, key='-SCOREJ1-')],
               [sg.Text(joueur2, size=(15, 1)), sg.Text('Chat évadés'), sg.Text(chats_eva_j2, key='-CHATSEVADESJ2-'),
                sg.Text('Chat capturés'), sg.Text(chats_cap_j2, key='-CHATSCAPTURESJ2-'), sg.Text('Score'),
                sg.Text(score_j2, key='-SCOREJ2-')],
               [sg.Text('Tour de '), sg.Text(key='-TOURJOUEURMANCHE2-')],
               [sg.Button("Commencer la seconde manche"), sg.Button('annuler')]],
              [[sg.Button(plateau[i][j], button_color=('black'), size=(8, 4), key=(i, j),
                          pad=(0, 0)) for j in range(nb_colonnes)] for i in range(nb_lignes)]]

    # Creation de la fenetre pour la manche 2
    window = sg.Window('EscaT Game', layout=layout, size=(1000, 1000))

    ### Boucle de gestion des evenements

    ## On effecture le premier tour
    while manche_2_commence != True:
        # Lecture du dernier evenement
        event, values = window.read()
        # Dans ce cas, il faut lancer la manche avec le bouton 'Commencer la première manche'
        if event == "Commencer la seconde manche":
            # On note que la manche est commence
            manche_2_commence = True
            window["Commencer la seconde manche"].Update("Seconde manche en cours")
            sg.Popup("Début de la seconde manche")

            ## Coloration du plateau
            # Coloration des cases contenant des chats
            for i in range(7, 11):
                for j in range(3, 8):
                    if plateau[i][j] == "C" or plateau[i][j] == "Ç":
                        window[i, j].Update(button_color=('black', 'NavajoWhite3'))

            # Coloration des cases obstacles (eau)
            for i in range(2, 4):
                for j in range(4, 7):
                    if plateau[i][j] == "O":
                        window[i, j].Update(button_color=('blue'))

            # Coloration des cases sorties
            window[0, 5].Update(button_color=('black', 'white'))
            window[4, 0].Update(button_color=('black', 'white'))
            window[4, 10].Update(button_color=('black', 'white'))

            # Coloration des cases gardiens
            window[1, 2].Update(button_color=('black', 'yellow'))
            window[1, 8].Update(button_color=('black', 'yellow'))

            ### Au tour de joueur 2 de commencer
            sg.Popup('Tour de joueur 2, appuie sur la case du chat que tu veux déplacer')
            window['-TOURJOUEURMANCHE2-'].Update(joueur2)

            ## Déplacements des chats

            # On crée une variable pour stocker les chats déplacés
            chats_deplaces_ce_tour = []

            # Le joueur peut deplacer jusqu'a 7 chats
            if Nb_cat >= 7:
                nb_chat_limite = 7
            else:
                nb_chat_limite = Nb_cat

            # On crée une variable qui prend le nombre de chats moins 7 (cette variable servira
            # si jamais un joueur possède encore plus de 7 chats et qu'il clique sur un chat
            # qui ne peut pas être déplacé)
            nb_chats_moins_sept = Nb_cat - 7

            # Pour le nombre de chats qu'il reste à deplacer
            while len(chats_deplaces_ce_tour) < nb_chat_limite:
                # On choisit un chat
                event, values = window.read()
                ligne, colonne = event[0], event[1]

                # On regarde qu'il s'agit bien d'un chat et qu'il n'a pas été deja deplacé
                if ((plateau[ligne][colonne] == "C" or plateau[ligne][colonne] == 'Ç') and [ligne,
                                                                                            colonne] not in chats_deplaces_ce_tour):

                    # On regarde les cases dispo autour de ce chat
                    if plateau[ligne][colonne] == "C":
                        case_dispo = cases_disponibles_chats(plateau, ligne, colonne)
                    else:
                        case_dispo = cases_disponibles_chaf(plateau, ligne, colonne)
                    # S'il n'y a pas de case disponibles, on le fait remonter au joueur
                    if case_dispo == []:
                        sg.Popup('Vous ne pouvez pas déplacer ce chat')
                        # Si nb_chats_moins_sept est inférieur ou égale à 0 alors cela veut dire qu'il n'a pas d'autre occasion de deplacer un chat
                        if nb_chats_moins_sept <= 0:
                            # On ajoute donc le chat à la liste des chats déplacés ce tour
                            chats_deplaces_ce_tour.append([ligne, colonne])
                        else:
                            nb_chats_moins_sept -= 1

                    # S'il y a une case disponible
                    else:
                        # On affiche en rouge les cases disponibles
                        for el in case_dispo:
                            window[el[0], el[1]].Update(button_color=('black', 'red'))
                        # On recupere une nouvelle action de la part du joueur
                        event, values = window.read()
                        new_ligne, new_colonne = event[0], event[1]
                        # On vérifie que cette action soit bien possible
                        if [new_ligne, new_colonne] in case_dispo:
                            # On regarde si cette case est une sortie ou non
                            if plateau[new_ligne][new_colonne] == 'S':
                                # On met a jour les chats deplacés ce tour (on met 1000,1000 car sinon ca bloque la case sortie)
                                chats_deplaces_ce_tour.append([1000, 1000])

                                # On met à jour les scores
                                chats_eva_j2 += 1
                                window['-CHATSEVADESJ2-'].Update(chats_eva_j2)
                                # Si c'est un chat "classique", +1 point
                                if plateau[ligne][colonne] == "C":
                                    score_j2 += 1
                                    window['-SCOREJ1-'].Update(score_j1)
                                # Sinon 'est 'Chaf', +5 points
                                else:
                                    score_j2 += 5
                                    window['-SCOREJ1-'].Update(score_j1)

                                # On retire un chat du plateau
                                Nb_cat -= 1
                                plateau[ligne][colonne] = ""

                                ## On remet les couleurs à jour
                                # Le chat laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne],
                                                              button_color=('NavajoWhite3', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo:
                                    # Si c'était une sortie, on remet la case blanche
                                    if plateau[el[0]][el[1]] == "S":
                                        window[el[0], el[1]].Update(button_color=('red', 'white'))
                                    # Sinon c'est une case vide
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))

                            else:
                                # On déplace le chat
                                plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                                plateau[ligne][colonne] = ""

                                # On met a jour les chats deplacés ce tour
                                chats_deplaces_ce_tour.append([new_ligne, new_colonne])

                                ## On remet les couleurs à jour
                                # Le chat laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne],
                                                              button_color=('NavajoWhite3', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo:
                                    # Si c'était une sortie, on remet la case blanche
                                    if plateau[el[0]][el[1]] == "S":
                                        window[el[0], el[1]].Update(button_color=('red', 'white'))
                                    # Sinon c'est une case vide
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))

                                # On met à jour la couleur de la nouvelle case qui contient le chat
                                window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                      button_color=('red', 'NavajoWhite3'))

                        else:
                            sg.Popup('Vous ne pouvez pas déplacer ce chat ici !')
                            ## On remet les couleurs à jour

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo:
                                # Si c'était une sortie, on remet la case blanche
                                if plateau[el[0]][el[1]] == "S":
                                    window[el[0], el[1]].Update(button_color=('red', 'white'))
                                # Sinon c'est une case vide
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))



                # Si le joueur ne selectionne pas un chat ou qu'il selectionne un chat deja deplace ce tour
                else:
                    if [ligne, colonne] in chats_deplaces_ce_tour:
                        sg.Popup("Vous avez déja deplacé ce chat ce tour !")
                    else:
                        sg.Popup("Ceci n'est pas un chat !")

            ### Déplacements gardiens

            sg.Popup('Tour de joueur 1, appuie sur les gardiens pour les deplacer')
            window['-TOURJOUEURMANCHE2-'].Update(joueur1)

            # On recupère le placement des gardiens
            gardien_restants_a_deplacer = list(case_gardien)
            while gardien_restants_a_deplacer != []:
                event, values = window.read()
                ligne, colonne = event[0], event[1]

                if [ligne, colonne] in gardien_restants_a_deplacer:

                    # On regarde les cases dispo autour de ce chat
                    case_dispo_gardien = cases_disponibles_gardien(plateau, ligne, colonne)
                    # S'il n'y a pas de case disponibles, on fait remonter au joueur que le gardien ne peut pas être deplacé
                    if case_dispo == []:
                        sg.Popup('Ce gardien ne peut pas être deplacé ce tour-ci')
                        # On supprime donc ce gardien de la liste des gardiens à deplacer
                        gardien_restants_a_deplacer.remove([ligne, colonne])

                    # Déplacement du gardien
                    else:
                        # On affiche en rouge les cases disponibles
                        for el in case_dispo_gardien:
                            window[el[0], el[1]].Update(button_color=('black', 'red'))
                        # On recupere une nouvelle action de la part du joueur
                        event, values = window.read()
                        new_ligne, new_colonne = event[0], event[1]
                        # On vérifie que cette action soit bien possible
                        if [new_ligne, new_colonne] in case_dispo_gardien:
                            # On regarde si cette case est un chat ou non
                            if plateau[new_ligne][new_colonne] == 'C' or plateau[new_ligne][new_colonne] == 'Ç':
                                # On déplace le gardien sur la case du chat
                                plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                                plateau[ligne][colonne] = ""
                                window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                      button_color=('NavajoWhite3', 'yellow'))

                                # On met a jour les cases gardiens
                                case_gardien.remove([ligne, colonne])
                                case_gardien.append([new_ligne, new_colonne])
                                gardien_restants_a_deplacer.remove([ligne, colonne])

                                # On retire un chat du plateau
                                Nb_cat -= 1

                                # On met à jour les scores
                                chats_cap_j1 += 1
                                window['-CHATSCAPTURESJ1-'].Update(chats_cap_j1)

                                ## On remet les couleurs à jour
                                # Le gardien laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo_gardien:
                                    # On prend les cases qui n'ont pas été selectionnées
                                    if el != [new_ligne, new_colonne]:
                                        # On regarde si c'est une case vide, sinon c'est un chat
                                        if plateau[el[0]][el[1]] == "":
                                            window[el[0], el[1]].Update(button_color=('red', 'black'))
                                        else:
                                            window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                            else:
                                # On déplace le gardien sur une case vide
                                plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                                plateau[ligne][colonne] = ""
                                window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                      button_color=('black', 'yellow'))

                                # On met a jour les cases gardiens
                                case_gardien.remove([ligne, colonne])
                                case_gardien.append([new_ligne, new_colonne])
                                gardien_restants_a_deplacer.remove([ligne, colonne])

                                ## On remet les couleurs à jour
                                # Le gardien laisse une case vide
                                window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                                # On remet les cases rouges dans leurs bonnes couleurs
                                for el in case_dispo_gardien:
                                    # On prend les cases qui n'ont pas été selectionnées
                                    if el != [new_ligne, new_colonne]:
                                        # On regarde si c'est une case vide, sinon c'est un chat
                                        if plateau[el[0]][el[1]] == "":
                                            window[el[0], el[1]].Update(button_color=('red', 'black'))
                                        else:
                                            window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                        else:
                            sg.Popup('Vous ne pouvez pas déplacer le gardien ici !')
                            ## On remet les couleurs à jour
                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo_gardien:
                                # On regarde si c'est une case vide, sinon c'est un chat
                                if plateau[el[0]][el[1]] == "":
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))
                else:
                    sg.Popup("Ceci n'est pas un gardien ou ce gardien a déjà été déplacé")

            ### Déplacements des robots
            for k in range(nb_lignes):
                for l in range(nb_colonnes):
                    if plateau[k][l] == "R":
                        # On génére un nombre aléatoire entre 0 et 1
                        temp_aleatoire = random.random()
                        # Les robots ont une chance sur trois de se déplacer
                        if temp_aleatoire < 1 / 3:
                            # On regarde les cases disponibles autours du robot
                            case_dispo_robot = cases_disponibles_robots(plateau, k, l)

                            # S'il n'y a pas de cases disponibles, on ne déplace pas le robot
                            if case_dispo_robot == []:
                                pass
                            else:
                                # On choisit une case dispo aléatoirement
                                temp_case_choisie = random.randint(0, len(case_dispo_robot) - 1)
                                case_choisie = case_dispo_robot[temp_case_choisie]

                                ## On déplace le robot sur cette case choisie

                                # Si cette case est un chat, alors on l'attrape
                                if plateau[case_choisie[0]][case_choisie[1]] == "C" or plateau[case_choisie[0]][
                                    case_choisie[1]] == 'Ç':
                                    # On retire un chat du plateau
                                    Nb_cat -= 1

                                    # On déplace le robot sur cette case
                                    plateau[case_choisie[0]][case_choisie[1]] = "R"
                                    plateau[k][l] = ""

                                    # On met a jour l'affichage
                                    window[k, l].Update(plateau[k][l])
                                    window[case_choisie[0], case_choisie[1]].Update(
                                        plateau[case_choisie[0]][case_choisie[1]],
                                        button_color=('NavajoWhite3', 'black'))

                                    # On met à jour les scores
                                    chats_cap_j1 += 1
                                    window['-CHATSCAPTURESJ1-'].Update(chats_cap_j1)

                                # Si le robot se déplace juste vers une case vide
                                else:
                                    # On déplace le robot sur cette case
                                    plateau[case_choisie[0]][case_choisie[1]] = "R"
                                    plateau[k][l] = ""

                                    # On met a jour l'affichage
                                    window[k, l].Update(plateau[k][l])
                                    window[case_choisie[0], case_choisie[1]].Update(
                                        plateau[case_choisie[0]][case_choisie[1]],
                                        button_color=('NavajoWhite3', 'black'))
                        else:
                            pass

        else:
            # arrete la boucle quand on ferme la fenetre
            if event == sg.WIN_CLOSED:
                break
            sg.Popup("Veuillez appuyer sur le bouton 'Commencer la seconde manche'")

            ### Boucle de gestion des evenements

    ## On continue la partie jusqu'a qu'il y ait plus de chat sur le plateau
    while Nb_cat != 0:
        ### Au tour de joueur 1 de commencer
        sg.Popup('Tour de joueur 2, appuie sur la case du chat que tu veux déplacer')
        window['-TOURJOUEURMANCHE2-'].Update(joueur2)

        ## Déplacements des chats

        # On crée une variable pour stocker les chats déplacés
        chats_deplaces_ce_tour = []

        # Le joueur peut deplacer jusqu'a 7 chats
        if Nb_cat >= 7:
            nb_chat_limite = 7
        else:
            nb_chat_limite = Nb_cat

        # On crée une variable qui prend le nombre de chats moins 7 (cette variable servira
        # si jamais un joueur possède encore plus de 7 chats et qu'il clique sur un chat
        # qui ne peut pas être déplacé)
        nb_chats_moins_sept = Nb_cat - 7

        # Pour le nombre de chats qu'il reste à deplacer
        while len(chats_deplaces_ce_tour) < nb_chat_limite:
            # On choisit un chat
            event, values = window.read()
            ligne, colonne = event[0], event[1]

            # On regarde qu'il s'agit bien d'un chat et qu'il n'a pas été deja deplacé
            if ((plateau[ligne][colonne] == "C" or plateau[ligne][colonne] == 'Ç') and [ligne,
                                                                                        colonne] not in chats_deplaces_ce_tour):

                # On regarde les cases dispo autour de ce chat
                if plateau[ligne][colonne] == "C":
                    case_dispo = cases_disponibles_chats(plateau, ligne, colonne)
                else:
                    case_dispo = cases_disponibles_chaf(plateau, ligne, colonne)
                # S'il n'y a pas de case disponibles, on le fait remonter au joueur
                if case_dispo == []:
                    sg.Popup('Vous ne pouvez pas déplacer ce chat')
                    # Si nb_chats_moins_sept est inférieur ou égale à 0 alors cela veut dire qu'il n'a pas d'autre occasion de deplacer un chat
                    if nb_chats_moins_sept <= 0:
                        # On ajoute donc le chat à la liste des chats déplacés ce tour
                        chats_deplaces_ce_tour.append([ligne, colonne])
                    else:
                        nb_chats_moins_sept -= 1

                # S'il y a une case disponible
                else:
                    # On affiche en rouge les cases disponibles
                    for el in case_dispo:
                        window[el[0], el[1]].Update(button_color=('black', 'red'))
                    # On recupere une nouvelle action de la part du joueur
                    event, values = window.read()
                    new_ligne, new_colonne = event[0], event[1]
                    # On vérifie que cette action soit bien possible
                    if [new_ligne, new_colonne] in case_dispo:
                        # On regarde si cette case est une sortie ou non
                        if plateau[new_ligne][new_colonne] == 'S':
                            # On met a jour les chats deplacés ce tour (on met 1000,1000 car sinon ca bloque la case sortie)
                            chats_deplaces_ce_tour.append([1000, 1000])

                            # On met à jour les scores
                            chats_eva_j2 += 1
                            window['-CHATSEVADESJ2-'].Update(chats_eva_j2)
                            # Si c'est un chat "classique", +1 point
                            if plateau[ligne][colonne] == "C":
                                score_j2 += 1
                                window['-SCOREJ2-'].Update(score_j2)
                            # Sinon c'est 'Chaf', +5 points
                            else:
                                score_j2 += 5
                                window['-SCOREJ2-'].Update(score_j2)

                            # On retire un chat du plateau
                            Nb_cat -= 1
                            plateau[ligne][colonne] = ""

                            ## On remet les couleurs à jour
                            # Le chat laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne],
                                                          button_color=('NavajoWhite3', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo:
                                # Si c'était une sortie, on remet la case blanche
                                if plateau[el[0]][el[1]] == "S":
                                    window[el[0], el[1]].Update(button_color=('red', 'white'))
                                # Sinon c'est une case vide
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))

                        else:
                            # On déplace le chat
                            plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                            plateau[ligne][colonne] = ""

                            # On met a jour les chats deplacés ce tour
                            chats_deplaces_ce_tour.append([new_ligne, new_colonne])

                            ## On remet les couleurs à jour
                            # Le chat laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne],
                                                          button_color=('NavajoWhite3', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo:
                                # Si c'était une sortie, on remet la case blanche
                                if plateau[el[0]][el[1]] == "S":
                                    window[el[0], el[1]].Update(button_color=('red', 'white'))
                                # Sinon c'est une case vide
                                else:
                                    window[el[0], el[1]].Update(button_color=('red', 'black'))

                            # On met à jour la couleur de la nouvelle case qui contient le chat
                            window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                  button_color=('red', 'NavajoWhite3'))

                    else:
                        sg.Popup('Vous ne pouvez pas déplacer ce chat ici !')
                        ## On remet les couleurs à jour

                        # On remet les cases rouges dans leurs bonnes couleurs
                        for el in case_dispo:
                            # Si c'était une sortie, on remet la case blanche
                            if plateau[el[0]][el[1]] == "S":
                                window[el[0], el[1]].Update(button_color=('red', 'white'))
                            # Sinon c'est une case vide
                            else:
                                window[el[0], el[1]].Update(button_color=('red', 'black'))



            # Si le joueur ne selectionne pas un chat ou qu'il selectionne un chat deja deplace ce tour
            else:
                if [ligne, colonne] in chats_deplaces_ce_tour:
                    sg.Popup("Vous avez déja deplacé ce chat ce tour !")
                elif event == sg.WIN_CLOSED:
                    break
                else:
                    sg.Popup("Ceci n'est pas un chat !")

        ### Déplacements gardiens

        sg.Popup('Tour de joueur 2, appuie sur les gardiens pour les deplacer')
        window['-TOURJOUEURMANCHE2-'].Update(joueur1)

        # On recupère le placement des gardiens
        gardien_restants_a_deplacer = list(case_gardien)
        while gardien_restants_a_deplacer != []:
            event, values = window.read()
            ligne, colonne = event[0], event[1]

            if [ligne, colonne] in gardien_restants_a_deplacer:

                # On regarde les cases dispo autour de ce chat
                case_dispo_gardien = cases_disponibles_gardien(plateau, ligne, colonne)
                # S'il n'y a pas de case disponibles, on fait remonter au joueur que le gardien ne peut pas être deplacé
                if case_dispo == []:
                    sg.Popup('Ce gardien ne peut pas être deplacé ce tour-ci')
                    # On supprime donc ce gardien de la liste des gardiens à deplacer
                    gardien_restants_a_deplacer.remove([ligne, colonne])

                # Déplacement du gardien
                else:
                    # On affiche en rouge les cases disponibles
                    for el in case_dispo_gardien:
                        window[el[0], el[1]].Update(button_color=('black', 'red'))
                    # On recupere une nouvelle action de la part du joueur
                    event, values = window.read()
                    new_ligne, new_colonne = event[0], event[1]
                    # On vérifie que cette action soit bien possible
                    if [new_ligne, new_colonne] in case_dispo_gardien:
                        # On regarde si cette case est un chat ou non
                        if plateau[new_ligne][new_colonne] == 'C' or plateau[new_ligne][new_colonne] == 'Ç':
                            # On déplace le gardien sur la case du chat
                            plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                            plateau[ligne][colonne] = ""
                            window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                  button_color=('NavajoWhite3', 'yellow'))

                            # On met a jour les cases gardiens
                            case_gardien.remove([ligne, colonne])
                            case_gardien.append([new_ligne, new_colonne])
                            gardien_restants_a_deplacer.remove([ligne, colonne])

                            # On retire un chat du plateau
                            Nb_cat -= 1

                            # On met à jour les scores
                            chats_cap_j1 += 1
                            window['-CHATSCAPTURESJ1-'].Update(chats_cap_j1)

                            ## On remet les couleurs à jour
                            # Le gardien laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo_gardien:
                                # On prend les cases qui n'ont pas été selectionnées
                                if el != [new_ligne, new_colonne]:
                                    # On regarde si c'est une case vide, sinon c'est un chat
                                    if plateau[el[0]][el[1]] == "":
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                        else:
                            # On déplace le gardien sur une case vide
                            plateau[new_ligne][new_colonne] = plateau[ligne][colonne]
                            plateau[ligne][colonne] = ""
                            window[new_ligne, new_colonne].Update(plateau[new_ligne][new_colonne],
                                                                  button_color=('black', 'yellow'))

                            # On met a jour les cases gardiens
                            case_gardien.remove([ligne, colonne])
                            case_gardien.append([new_ligne, new_colonne])
                            gardien_restants_a_deplacer.remove([ligne, colonne])

                            ## On remet les couleurs à jour
                            # Le gardien laisse une case vide
                            window[ligne, colonne].Update(plateau[ligne][colonne], button_color=('yellow', 'black'))

                            # On remet les cases rouges dans leurs bonnes couleurs
                            for el in case_dispo_gardien:
                                # On prend les cases qui n'ont pas été selectionnées
                                if el != [new_ligne, new_colonne]:
                                    # On regarde si c'est une case vide, sinon c'est un chat
                                    if plateau[el[0]][el[1]] == "":
                                        window[el[0], el[1]].Update(button_color=('red', 'black'))
                                    else:
                                        window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))

                    else:
                        sg.Popup('Vous ne pouvez pas déplacer le gardien ici !')
                        ## On remet les couleurs à jour
                        # On remet les cases rouges dans leurs bonnes couleurs
                        for el in case_dispo_gardien:
                            # On regarde si c'est une case vide, sinon c'est un chat
                            if plateau[el[0]][el[1]] == "":
                                window[el[0], el[1]].Update(button_color=('red', 'black'))
                            else:
                                window[el[0], el[1]].Update(button_color=('red', 'NavajoWhite3'))
            else:
                if event == sg.WIN_CLOSED:
                    break
                else:
                    sg.Popup("Ceci n'est pas un gardien ou ce gardien a déjà été déplacé")

        ### Déplacements des robots
        for k in range(nb_lignes):
            for l in range(nb_colonnes):
                if plateau[k][l] == "R":
                    # On génére un nombre aléatoire entre 0 et 1
                    temp_aleatoire = random.random()
                    # Les robots ont une chance sur trois de se déplacer
                    if temp_aleatoire < 1 / 3:
                        # On regarde les cases disponibles autours du robot
                        case_dispo_robot = cases_disponibles_robots(plateau, k, l)

                        # S'il n'y a pas de cases disponibles, on ne déplace pas le robot
                        if case_dispo_robot == []:
                            pass
                        else:
                            # On choisit une case dispo aléatoirement
                            temp_case_choisie = random.randint(0, len(case_dispo_robot) - 1)
                            case_choisie = case_dispo_robot[temp_case_choisie]

                            ## On déplace le robot sur cette case choisie

                            # Si cette case est un chat, alors on l'attrape
                            if plateau[case_choisie[0]][case_choisie[1]] == "C" or plateau[case_choisie[0]][
                                case_choisie[1]] == 'Ç':
                                # On retire un chat du plateau
                                Nb_cat -= 1

                                # On déplace le robot sur cette case
                                plateau[case_choisie[0]][case_choisie[1]] = "R"
                                plateau[k][l] = ""

                                # On met a jour l'affichage
                                window[k, l].Update(plateau[k][l])
                                window[case_choisie[0], case_choisie[1]].Update(
                                    plateau[case_choisie[0]][case_choisie[1]], button_color=('NavajoWhite3', 'black'))

                                # On met à jour les scores
                                chats_cap_j1 += 1
                                window['-CHATSCAPTURESJ1-'].Update(chats_cap_j1)

                            # Si le robot se déplace juste vers une case vide
                            else:
                                # On déplace le robot sur cette case
                                plateau[case_choisie[0]][case_choisie[1]] = "R"
                                plateau[k][l] = ""

                                # On met a jour l'affichage
                                window[k, l].Update(plateau[k][l])
                                window[case_choisie[0], case_choisie[1]].Update(
                                    plateau[case_choisie[0]][case_choisie[1]], button_color=('NavajoWhite3', 'black'))
                    else:
                        pass

    update_button_seconde_manche = False
    # Fin de la seconde manche
    while True:
        if update_button_seconde_manche == False:
            window["Commencer la seconde manche"].Update("Partie terminé - afficher les scores")
            update_button_seconde_manche = True
        sg.Popup("Fin de la second manche, femer le fenetre pour afficher les scores")
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Commencer la seconde manche":
            break

    window.close()  # Destruction de la fenetre

    afficher_score(score_j1, joueur1, score_j2, joueur2)


# Lancement d'une partie
main()