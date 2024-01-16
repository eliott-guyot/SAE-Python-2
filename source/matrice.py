"""
Une implémentation des matrices 2D en python
Détailler ici la modélisation choisie en donnant au moins un exemple
"""
""" Matrices : API n 1 """


def new_matrice(nb_lignes, nb_colonnes, valeur_par_defaut):
    """crée une nouvelle matrice en mettant la valeur par défaut dans chacune de ses cases.

    Args:
        nb_lignes (int): le nombre de lignes de la matrice
        nb_colonnes (int): le nombre de colonnes de la matrice
        valeur_par_defaut : La valeur que prendra chacun des éléments de la matrice

    Returns:
        une nouvelle matrice qui contient la valeur par défaut dans chacune de ses cases
    """

    return [[valeur_par_defaut for _ in range(nb_colonnes)] for _ in range(nb_lignes)]



def set_val(matrice, ligne, colonne, nouvelle_valeur):
    """permet de modifier la valeur de l'élément qui se trouve à la ligne et à la colonne
    spécifiées. Cet élément prend alors la valeur nouvelle_valeur

    Args:
        matrice : une matrice
        ligne (int) : le numéro d'une ligne (la numérotation commence à zéro)
        colonne (int) : le numéro d'une colonne (la numérotation commence à zéro)
        nouvelle_valeur : la nouvelle valeur que l'on veut mettre dans la case

    Returns:
        None
    """
    
    matrice[ligne][colonne] = nouvelle_valeur


def get_nb_lignes(matrice):
    """permet de connaître le nombre de lignes d'une matrice

    Args:
        matrice : une matrice

    Returns:
        int : le nombre de lignes de la matrice
    """
    
    return len(matrice)


def get_nb_colonnes(matrice):
    """permet de connaître le nombre de colonnes d'une matrice

    Args:
        matrice : une matrice

    Returns:
        int : le nombre de colonnes de la matrice
    """
    
    return len(matrice[0])


def get_val(matrice, ligne, colonne):
    """permet de connaître la valeur de l'élément de la matrice dont on connaît
    le numéro de ligne et le numéro de colonne.

    Args:
        matrice : une matrice
        ligne (int) : le numéro d'une ligne (la numérotation commence à zéro)
        colonne (int) : le numéro d'une colonne (la numérotation commence à zéro)

    Returns:
        la valeur qui est dans la case située à la ligne et la colonne spécifiées
    """
    
    return matrice[ligne][colonne]

def affiche(matrice, taille_cellule=4):
    """permet d'afficher une matrice dans le terminal

    Args:
        matrice : une matrice
        taille_cellule (int, optional): la taille d'une cellule. Defaults to 4.
    """
    
    for ligne in range(get_nb_lignes(matrice)):
        print("|", end="")
        for colonne in range(get_nb_colonnes(matrice)):
            print(str(get_val(matrice, ligne, colonne)).center(4) + "|", end="")
        print()


def affiche_labyrinthe(matrice, taille_cellule=4):
    for ligne in range(get_nb_lignes(matrice)):
        for colonne in range(get_nb_colonnes(matrice)):
            val = get_val(matrice, ligne, colonne)
            val = str(val).center(3) if val is not None else "███"
            print(val, end="")
        print()

#-----------------------------------------
# entrées sorties dans des fichiers
#-----------------------------------------

def sauve_matrice(matrice, nom_fichier):
    """Sauvegarde la matrice dans un fichier csv dont chaque ligne
    représente une ligne de la matrice et les valeurs sont spérarées
    par des virgules (',')

    Args:
        matrice (matrice): une matrice selon la modélisation précisée
        dans la documentation du module
        nom_fichier (str): le nom d'un chemin vers un fichier
                           par exemple "./matrice1.csv" ou "../sauvegardes/matrice3.csv"
    Returns:
        None
    """
    fichier = open(nom_fichier, 'w')
    for no_ligne in range(get_nb_lignes(matrice)):
        ligne = ''
        for no_colonne in range(get_nb_colonnes(matrice)):
            valeur = get_val(matrice, no_ligne, no_colonne)
            if valeur is None:
                ligne += ','
            else:
                ligne += str(valeur) + ','
        ligne = ligne[:-1]+'\n'
        fichier.write(ligne)
    fichier.close()


def lignes_et_colonnes(nom_fichier):
    """renvoie un tuple contenant le nombre de lignes et le nombre de colonnes d'une matrice
       dans un fichier csv

    Args:
        nom_fichier (str): le nom d'un chemin vers un fichier
                           par exemple "./matrice1.csv" ou "../sauvegardes/matrice3.csv"
    Returns:
        tuple: un tuple de deux nombres entiers (nombre_de_lignes, nombre_de_colonnes) de la matrice
               contenu dans le fichier
    """
    fichier = open(nom_fichier, 'r')
    nb_lignes = 0
    for ligne in fichier:
        nb_lignes += 1
    nb_colonnes  = len(ligne.split(","))
    return (nb_lignes, nb_colonnes)


def copie_matrice(matrice):
    nouvelle_matrice = new_matrice(get_nb_lignes(matrice), get_nb_colonnes(matrice), None)

    for no_ligne in range(get_nb_lignes(matrice)):
        for no_colonne in range(get_nb_colonnes(matrice)):
            set_val(nouvelle_matrice, no_ligne, no_colonne, get_val(matrice, no_ligne, no_colonne))
    
    return nouvelle_matrice


def charge_matrice(nom_fichier, type_valeur='int'):
    """Charge une matrice à partir d'un fichier csv dont chaque ligne
    représente une ligne de la matrice et les valeurs (des entiers ou des str)
    sont séparées par des virgules (',')

    Args:
        nom_fichier (str): le nom d'un chemin vers un fichier
                           par exemple "./matrice1.csv" ou "../sauvegardes/matrice3.csv"
        type_valeur (str, optional): le type des valeurs ('int' ou 'str'. Defaults to 'int'.
    Returns:
        matrice (matrice): une matrice selon la modélisation précisée
        dans la documentation du module
    """
    (nb_lignes, nb_colonnes) = lignes_et_colonnes(nom_fichier)
    ma_matrice = new_matrice(nb_lignes, nb_colonnes, None)
    fichier = open(nom_fichier, 'r')
    no_ligne = 0
    for ligne in fichier:
        liste_des_valeurs = ligne[:-1].split(",")
        no_colonne = 0
        for valeur in liste_des_valeurs:
            if valeur == '':
                valeur = None
            elif type_valeur == 'int':
                valeur = int(valeur)
            else:
                valeur = valeur
            set_val(ma_matrice, no_ligne, no_colonne, valeur)                
            no_colonne += 1
        no_ligne += 1
    return ma_matrice
