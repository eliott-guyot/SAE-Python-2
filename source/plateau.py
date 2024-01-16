"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module plateau.py
        Ce module contient l'implémentation de la structure de données
        qui gère le plateau jeu aussi qu'un certain nombre de fonctions
        permettant d'observer le plateau et d'aider l'IA à prendre des décisions
"""
import random

import case
import const


def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """

    return plateau["taille"][0]


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """

    return plateau["taille"][1]


def pos_ouest(plateau, pos):
    """retourne la position de la case à l'ouest de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    
    ouest=[pos[0],pos[1]-1]
    if ouest[1] < 0:
        ouest[1]=get_nb_colonnes(plateau)-1
    return tuple(ouest)


def pos_est(plateau, pos):
    """retourne la position de la case à l'est de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    
    est=[pos[0],pos[1]+1]
    if est[1] >=get_nb_colonnes(plateau):
        est[1]=0
    return tuple(est)

def pos_nord(plateau, pos):
    """retourne la position de la case au nord de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    
    nord=[pos[0]-1,pos[1]]
    if nord[0]<0:
        nord[0]=get_nb_lignes(plateau)-1
    return tuple(nord)


def pos_sud(plateau, pos):
    """retourne la position de la case au sud de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    
    sud=[pos[0]+1,pos[1]]
    if sud[0] >=get_nb_lignes(plateau):
        sud[0]=0
    return tuple(sud)


def pos_arrivee(plateau,pos,direction):
    """ calcule la position d'arrivée si on part de pos et qu'on va dans
    la direction indiquée en tenant compte que le plateau est un tore
    si la direction n'existe pas la fonction retourne None
    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire d'entiers qui donne la position de départ
        direction (str): un des caractère NSEO donnant la direction du déplacement

    Returns:
        None|tuple: None ou une paire d'entiers indiquant la position d'arrivée
    """
    if direction == 'N':
        return pos_nord(plateau, pos)

    elif direction == 'S':
        return pos_sud(plateau, pos)
    
    elif direction == 'E':
        return pos_est(plateau, pos)
    
    elif direction == 'O':
        return pos_ouest(plateau, pos)

    else:
        return None


def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """

    return plateau["cases"][pos[0]][pos[1]]


def get_objet(plateau, pos):
    """retourne l'objet qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        str: le caractère symbolisant l'objet
    """

    return case.get_objet(get_case(plateau, pos))


def poser_pacman(plateau, pacman, pos):
    """pose un pacman en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le pacman
        pos (tuple): une paire (lig,col) de deux int
    """
    
    plateau["pacmans"].add((pacman, pos))
    case.poser_pacman(get_case(plateau, pos), pacman)


def poser_fantome(plateau, fantome, pos):
    """pose un fantome en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int
    """

    plateau["fantomes"].add((fantome, pos))
    case.poser_fantome(get_case(plateau, pos), fantome)


def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (int): un entier représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """
    
    case.poser_objet(get_case(plateau, pos), objet)


def Plateau(la_chaine):
    """Construit un plateau à partir d'une chaine de caractère contenant les informations
        sur le contenu du plateau (voir sujet)

    Args:
        la_chaine (str): la chaine de caractères décrivant le plateau

    Returns:
        dict: le plateau correspondant à la chaine. None si l'opération a échoué
    """
    # Initialise le plateau
    lignes = la_chaine.split("\n")
    plateau = {
        "taille": (0, 0),
        "cases": [],
        "pacmans": set(),
        "fantomes": set()
    }
    
    # Définit la taille du plateau
    taille = lignes[0].split(";")
    plateau["taille"] = (int(taille[0]), int(taille[1]))

    # Construit le labirynthe
    for y in range(plateau["taille"][0]):
        plateau["cases"].append([])

        for elem in lignes[y + 1]:
            if elem == const.AUCUN:
                plateau["cases"][y].append(case.Case())

            elif elem in const.LES_OBJETS:
                plateau["cases"][y].append(case.Case(objet=elem))

            else:
                plateau["cases"][y].append(case.Case(mur=True))

    # Place les pacmans
    nb_pacmans = int(lignes[plateau["taille"][0] + 1])
    for i in range(nb_pacmans):
        pacman = lignes[plateau["taille"][0] + 2 + i].split(";")
        x, y = int(pacman[1]), int(pacman[2])
        plateau["pacmans"].add((pacman[0], (x, y)))
        case.poser_pacman(get_case(plateau, (x, y)), pacman[0])

    # Place les fantomes
    nb_fantomes = int(lignes[plateau["taille"][0] + 2 + nb_pacmans])
    for i in range(nb_fantomes):
        fantome = lignes[plateau["taille"][0] + 3 + nb_pacmans + i].split(";")
        x, y = int(fantome[1]), int(fantome[2])
        plateau["fantomes"].add((fantome[0], (x, y)))
        case.poser_fantome(get_case(plateau, (x, y)), fantome[0])

    return plateau

    
def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """

    plateau["cases"][pos[0]][pos[1]] = une_case
    

def enlever_pacman(plateau, pacman, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """

    if case.prendre_pacman(get_case(plateau, pos), pacman):
        plateau["pacmans"].remove((pacman, pos))
        return True
    
    return False


def enlever_fantome(plateau, fantome, pos):
    """enlève un fantome qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """

    if fantome in plateau["fantomes"]:
        plateau["fantomes"].remove((fantome, pos))

    return case.prendre_fantome(get_case(plateau, pos), fantome)


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """
    
    return case.prendre_objet(get_case(plateau, pos))
        

def deplacer_pacman(plateau, pacman, pos, direction, passemuraille=False):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau si c'est possible

    Args:
        plateau (dict): Le plateau considéré
        pacman (str): La lettre identifiant le pacman à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement
        passemuraille (bool): un booléen indiquant si le pacman est passemuraille ou non

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du pacman 
                   (None si le pacman n'a pas pu se déplacer)
    """
    if (pacman, pos) not in plateau["pacmans"]:
        return 

    nouvelle_pos = pos_arrivee(plateau, pos, direction)
    if nouvelle_pos is None:
        return 

    case_depart = get_case(plateau, pos)
    nouvelle_case = get_case(plateau, nouvelle_pos)

    if case.est_mur(nouvelle_case) and not passemuraille:
        return
    
    case.prendre_pacman(case_depart, pacman)
    case.poser_pacman(nouvelle_case, pacman)
    plateau["pacmans"].remove((pacman, pos))
    plateau["pacmans"].add((pacman, nouvelle_pos))
    return nouvelle_pos


def deplacer_fantome(plateau, fantome, pos, direction):
    """Déplace dans la direction indiquée un fantome se trouvant en position pos
        sur le plateau

    Args:
        plateau (dict): Le plateau considéré
        fantome (str): La lettre identifiant le fantome à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du fantome
                   None si le joueur n'a pas pu se déplacer
    """
    if (fantome, pos) not in plateau["fantomes"]:
        return 

    nouvelle_pos = pos_arrivee(plateau, pos, direction)
    if nouvelle_pos is None:
        return 
    
    case_depart = get_case(plateau, pos)
    nouvelle_case = get_case(plateau, nouvelle_pos)

    if case.est_mur(nouvelle_case):
        return 
    
    case.prendre_fantome(case_depart, fantome)
    case.poser_fantome(nouvelle_case, fantome)
    plateau["fantomes"].remove((fantome, pos))
    plateau["fantomes"].add((fantome, nouvelle_pos))
    return nouvelle_pos


def case_vide(plateau):
    """choisi aléatoirement sur la plateau une case qui n'est pas un mur et qui
       ne contient ni pacman ni fantome ni objet

    Args:
        plateau (dict): le plateau

    Returns:
        (int,int): la position choisie
    """
    x, y = random.randint(0, get_nb_lignes(plateau) - 1), random.randint(0, get_nb_colonnes(plateau) - 1)
    case_choisie = get_case(plateau, (x, y))
    
    while case.est_mur(case_choisie) or case.get_objet(case_choisie) != const.AUCUN or case.get_pacmans(case_choisie) or case.get_fantomes(case_choisie):
        x, y = random.randint(0, get_nb_lignes(plateau) - 1), random.randint(0, get_nb_colonnes(plateau) - 1)
        case_choisie = get_case(plateau, (x, y))

    return (x, y)


def directions_possibles(plateau,pos,passemuraille=False):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
        passemuraille (bool): indique si on s'autorise à passer au travers des murs
    
    Returns:
        str: une chaine de caractères indiquant les directions possibles
              à partir de pos
    """
    directions = ""
    for direction in const.DIRECTIONS:
        pos_arr = pos_arrivee(plateau, pos, direction)
        case_arr = get_case(plateau, pos_arr)

        if not case.est_mur(case_arr) or passemuraille:
            directions += direction

    return directions
    

#---------------------------------------------------------#


def analyse_plateau(plateau, pos, direction, distance_max):
    """calcul les distances entre la position pos est les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
    Returns:
        dict: un dictionnaire de listes. 
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist,ident) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """ 
    res = {
        "objets": [],
        "pacmans": [],
        "fantomes": []
    }
    cases_parcourues = set()

    def _inondation(plateteau, pos, distance):
        if distance > distance_max or pos in cases_parcourues:
            return

        for direction in directions_possibles(plateau, pos):
            distance_intersection = prochaine_intersection(plateau, pos, direction)
            pos_arr = pos
            for i in range(distance_intersection):
                pos_arr = pos_arrivee(plateau, pos, direction)

                if pos_arr not in cases_parcourues and distance + i <= distance_max:    
                    case_arr = get_case(plateau, pos_arr)
                    fantomes = case.get_fantomes(case_arr)

                    for fantome in fantomes:
                        res["fantomes"].append((distance + i, fantome)) 

                    pacmans = case.get_pacmans(case_arr)
                    for pacman in pacmans:
                        res["pacmans"].append((distance + i, pacman))

                    objet = case.get_objet(case_arr)
                    if objet != const.AUCUN:
                        res["objets"].append((distance + i, objet))

                    cases_parcourues.add(pos_arr)

            if distance_intersection != -1:
                _inondation(plateau, pos_arr, distance + distance_intersection)

    _inondation(plateau, pos, 0)
    return res


def prochaine_intersection(plateau,pos,direction):
    """calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        int: un entier indiquant la distance à la prochaine intersection
             -1 si la direction mène à un cul de sac.
    """
    def _est_intersection(plateau, pos):
        if len(directions_possibles(plateau, pos)) > 2:
            return True
        
        return False

    distance = 0
    prochaine_position = pos_arrivee(plateau, pos, direction)

    while not _est_intersection(plateau, prochaine_position):
        distance += 1
        prochaine_position = pos_arrivee(plateau, prochaine_position, direction)

        if prochaine_position == pos:
            return -1
    
    return distance

# A NE PAS DEMANDER
def plateau_2_str(plateau):
        res = str(get_nb_lignes(plateau))+";"+str(get_nb_colonnes(plateau))+"\n"
        pacmans = []
        fantomes = []
        for lig in range(get_nb_lignes(plateau)):
            ligne = ""
            for col in range(get_nb_colonnes(plateau)):
                la_case = get_case(plateau,(lig, col))
                if case.est_mur(la_case):
                    ligne += "#"
                    les_pacmans = case.get_pacmans(la_case)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                else:
                    obj = case.get_objet(la_case)
                    les_pacmans = case.get_pacmans(la_case)
                    les_fantomes= case.get_fantomes(la_case)
                    ligne += str(obj)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                    for fantome in les_fantomes:
                        fantomes.append((fantome,lig,col))
            res += ligne+"\n"
        res += str(len(pacmans))+'\n'
        for pac, lig, col in pacmans:
            res += str(pac)+";"+str(lig)+";"+str(col)+"\n"
        res += str(len(fantomes))+"\n"
        for fantome, lig, col in fantomes:
            res += str(fantome)+";"+str(lig)+";"+str(col)+"\n"
        return res

