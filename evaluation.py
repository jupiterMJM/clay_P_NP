# fichier pour vérifier le fichier main

# importation des modules
import random as rd
import main as m
import time as t
import numpy as np


# définition des variables initiales
nb_eleves_max = 100
nb_contraintes_max = 10
nb_chambres_max = 10


# création des fonctions initiales
def generation_incompatibilite(nb_contraintes, nb_eleves):
    """
    je crois que pour n élèves il y a au plus n(n+1)/2 contraintes possibles
    hypothèse établie sur les premiers entiers mais non vérifiée
    """
    assert nb_contraintes <= int(nb_eleves*(nb_eleves-1)/2)
    retour = list()
    while len(retour) < nb_contraintes:
        contrainte = rd.sample(range(nb_eleves), 2)
        contrainte = (min(contrainte), max(contrainte))
        if contrainte not in retour:
            retour.append(contrainte)
    return retour

def verification(proposition, contraintes):
    # print(proposition)
    if type(proposition) == str:
        return proposition
    for elt in contraintes:
        if not(elt[0] in proposition and elt[1] in proposition):
            pass  # tout va bien
        else:
            print("ERREUR_ALGO_NON_VALIDE")
            print(f"contraintes imposées: {contraintes}")
            print(f"proposition: {proposition}")
            return "ERREUR_ALGO_NON_VALIDE"
    return "PROPOSITION_VALIDE"

def count_zero_par_ligne(matrice):
    """
    >>> count_zero_par_ligne(np.array([[1, 1, 2], [0, 0, 0], [1, 0, 1]]))
    [0, 3, 1]
    """
    retour = [np.count_nonzero(matrice[i] == 0) for i in range(len(matrice))]
    return retour

def test_insolubilite(contrainte, nb_eleves, nb_chambres):
    """
    fonction non vérifiée, basée sur une hypothèse établie sur les premiers entiers
    je pense que cela permetterait d'ailleurs d'offrir un nouvel algorithme possible
    pour l'instant, je pense que:
        test_insolubilite() is True => problème insoluble
        attention reciproque fausse pour l'instant!
    hypothèse:
        en notant n=nb_chambre et A la matrice-contrainte alors:
        le problème est résoluble ssi il existe au moins n lignes de A^n comportant n-1 coeff égaux à 0
    >>> test_insolubilite([(1, 4), (3, 4), (0, 1), (0, 6), (0, 4), (1, 6)], 7, 5)
    True
    >>> test_insolubilite([(0, 2)], 3, 3)
    True
    """
    print(contrainte)
    matrice = m.generation_matrice_contrainte(contrainte, nb_eleves)
    # print(matrice)
    power = np.linalg.matrix_power(matrice, nb_chambres)
    # print(power)
    indic = power[power==0]
    transfo = np.count_nonzero(np.array(count_zero_par_ligne(power)) >= nb_chambres - 1)
    return transfo < nb_chambres  # True si insoluble

# fonction pour tester la robustesse de l'algorithme
def test(nb_test):
    for _ in range(nb_test):
        nb_eleves = rd.randint(2, nb_eleves_max)
        nb_contraintes = rd.randint(1, min(int(nb_eleves*(nb_eleves-1)/2), nb_contraintes_max))
        nb_chambres = rd.randint(1, min(nb_chambres_max, nb_eleves))
        print(f"\n {nb_contraintes} {nb_eleves} {nb_chambres}")
        contraintes = generation_incompatibilite(nb_contraintes, nb_eleves)
        print(contraintes)
        retour = m.main(contraintes, nb_eleves, nb_chambres)
        if retour == None:
            print("none", contraintes, nb_eleves, nb_chambres)
        if retour == "INSOLUBLE":
            return "INSOLUBLE"
        if retour == "ERREUR_GENERATION":
            return "ERREUR_GENERATION"
        if verification(retour, contraintes) == "ERREUR_ALGO_NON_VALIDE":
            print(nb_eleves, nb_chambres, nb_contraintes)
            return
        print("\n")
        
def test_clay(nb_contraintes, verbose=True):
    debut = t.time()
    contraintes = generation_incompatibilite(nb_contraintes, 400)
    mil = t.time()
    retour = m.main(contraintes, 400, 100)
    fin = t.time()
    check=verification(retour, contraintes)
    if verbose:
        print(retour)
        print(check)
        print(f"gen_contrainte: {mil-debut}, main: {fin-mil}, verif: {t.time()-fin}")
    return check


def test_clay_puissant(nb_max_contraintes, nb_test_par_contrainte):
    for nb_contrainte in range(1, nb_max_contraintes):
        indic = 0
        for _ in range(nb_test_par_contrainte):
            if test_clay(nb_contrainte, False) == "INSOLUBLE":
                indic += 1
        print(nb_contrainte, indic)
