# fichier pour vérifier le fichier main

# importation des modules
import random as rd
import main as m


# définition des variables initiales
nb_eleves_max = 400
nb_contraintes_max = 50
nb_chambres_max = 100


# création des fonctions initiales
def generation_incompatibilite(nb_contraintes, nb_eleves):
    """
    je crois que pour n élèves il y a au plus n(n+1)/2 contraintes possibles
    hypothèse établie sur les premiers entiers mais non vérifiée
    """
    assert nb_contraintes <= int(nb_eleves(nb_eleves+1)/2)
    retour = list()
    while len(retour) < nb_contraintes:
        contrainte = rd.sample(range(nb_eleves), 2)
        contrainte = (min(contrainte), max(contrainte))
        if contrainte not in retour:
            retour.append(contrainte)
    return retour

def verification(proposition, contraintes):
    for elt in contraintes:
        if not(elt[0] in proposition and elt[1] in proposition):
            pass  # tout va bien
        else:
            print("ERREUR_ALGO_NON_VALIDE")
            print(f"contraintes imposées: {contraintes}")
            print(f"proposition: {proposition}")
            return "ERREUR_ALGO_NON_VALIDE"
        

# fonction pour tester la robustesse de l'algorithme
def test(nb_test):
    for _ in range(nb_test):
        nb_eleves = rd.randint(2, nb_eleves_max)
        nb_contraintes = rd.randint(1, min(int(nb_eleves(nb_eleves+1)/2), nb_contraintes_max))
        nb_chambres = rd.randint(1, min(nb_chambres_max, nb_eleves))
        contraintes = generation_incompatibilite(nb_contraintes)
        retour = m.main(contraintes, nb_eleves, nb_chambres)
        if retour == "ERREUR_GENERATION":
            return
        if verification(retour, contraintes) == "ERREUR_ALGO_NON_VALIDE":
            print(nb_eleves, nb_chambres, nb_contraintes)
            return
        