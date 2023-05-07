# importation des modules
import random as rd
import numpy as np

# définition des variables initiales
nb_eleves = 400
nb_contraintes = 50
nb_chambres = 100


# définition des fonctions initiales
def score_eleves_chiants(contrainte, nb_eleves):
    """
    permet de mesurer la "chiantise" d'un élève, plus un élève est incompatible avec les autres
    plus il est considéré comme chiant (et donc sera moins prioritaire à l'internat)
    """
    retour = [(i, 0) for i in range(nb_eleves)]  # (num_eleve, score_chiant)
    for elt in contrainte:
        retour[elt[0]][1] += 1
        retour[elt[1]][1] += 1
    return retour

def separer_chiants_ou_non(score_eleve, nb_eleves):
    """
    permet déterminer si un élève est chiant ou non
    un élève est considéré chiant si il apparait dans au moins une des contraintes
    """
    retour = [list(), list()]  # [non chiants, chiants]
    for i in range(len(score_eleve)):
        if score_eleve[i][1] == 0: # il n'est pas chiant
            retour[0].append(i)
        else:
            retour[1].append(score_eleve[i])
    return retour


def generation_matrice_contrainte(contraintes, nb_eleves):
    retour = np.identity(nb_eleves)  # c'est plus pratique d'utiliser la matrice identité
    for elt in contraintes:
        retour[elt[0], elt[1]] = 1
        retour[elt[1], elt[0]] = 1
    return retour


# fonction principale
def main(contraintes, nb_eleves, nb_chambres):
    chiantise = score_eleves_chiants(contraintes, nb_eleves)
    eleves_pas_chiants, eleves_chiants = separer_chiants_ou_non(chiantise, nb_eleves)

    # cas 1: il y a plus d'élèves non-chiants que de places disponibles
    if len(eleves_pas_chiants) >= nb_chambres:
        retour = rd.sample(eleves_pas_chiants, nb_chambres)
        return retour

    elif len(eleves_pas_chiants) > 0:
        retour = eleves_pas_chiants.copy()
        # il faut maintenant caser les élèves chiants
        matrice_contrainte = generation_matrice_contrainte(contraintes, nb_eleves)
        classement = sorted(eleves_chiants, key = lambda eleve : eleve[1], reverse=True)  # on classe en fonction du score de chiantise dans l'ordre décroissant
        eleves_dispo = [eleves_chiants[i][0] for i in range(len(eleves_chiants))]
        chambres_restantes = nb_chambres - len(retour)
        while chambres_restantes > 0:
            if len(eleve_a_placer) == 0 or len(classement) == 0:
                print("ERREUR: L'algorithme ne parvient pas à conclure!!!")
                print(f"nb_élèves: {nb_eleves}, nb_chambres: {nb_chambres}, nb_contraintes: {len(contraintes)}")
                print(f"contraintes:\n {contraintes}")
                return "ERREUR_GENERATION"
            eleve_a_placer, score = classement.pop()
            if eleve_a_placer not in eleves_dispo:
                continue
            retour.append(eleve_a_placer)
            for i in range(len(matrice_contrainte)):
                if matrice_contrainte[eleve_a_placer][i] == 1:
                    eleves_dispo.remove(i)
        return retour
        