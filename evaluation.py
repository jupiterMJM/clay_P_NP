# fichier pour vérifier le fichier main

# importation des modules
import random as rd


# définition des variables initiales
nb_eleves_max = 400
nb_contraintes_max = 50
nb_chambres_max = 100


# création des fonctions initiales
def generation_incompatibilite(nb_contraintes, nb_eleves):
    retour = list()
    while len(retour) < nb_contraintes:
        contrainte = rd.sample(range(nb_eleves), 2)
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
