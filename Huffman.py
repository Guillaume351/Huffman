# -*- coding: utf-8 -*-
import es

def listerCarac(fichier):
    """
    Liste les caractères et retourne un dictionnaire contenant chaque caractère associé à son poids
    :param fichier: binary file
    :return: liste de bytes correspondant au texte, dictionnaire des caracteres et leur poids
    """
    finDeFichier = False
    texteInBytes = []
    dictCarac = dict()
    while (finDeFichier == False):
        carac = es.one_byte(fichier)
        if (carac != None):
            texteInBytes.append(carac)
            if (carac not in dictCarac):
                dictCarac[carac] = 1
            else:
                dictCarac[carac] += 1
        else:
            finDeFichier = True #Caractère nul, donc fin de fichier
    return texteInBytes, dictCarac


def creerArbre(dictCarac):
    """
    Associe les « feuilles » pour créer l’arbre de Huffman sous forme de liste de listes
    :param dictCarac: Dictionnaire contenant les caracteres et leur poids
    :return: retourne l'arbre
    """
    liste_de_feuilles_disponibles = []
    for c in dictCarac.items():
        liste_de_feuilles_disponibles.append([c[1],c[0]])

    liste_de_feuilles_disponibles.append([0,-1 ]) # Caractere de fin de fichier ajouté

    while (len(liste_de_feuilles_disponibles) > 1): #Tant que toutes les feuilles ne sont pas associées
        somme_branches = liste_de_feuilles_disponibles[-1][0]+liste_de_feuilles_disponibles[0][0] #On prend somme des poids de deux branches au hasard
        mini1,mini2 = -1,0
        for i in range(len(liste_de_feuilles_disponibles)): # On cherche la combinaison de branche ayant le poids le plus faible
            for k in range(len(liste_de_feuilles_disponibles)):
                poids = liste_de_feuilles_disponibles[i][0]+liste_de_feuilles_disponibles[k][0]
                if(poids <= (somme_branches) and i !=k ):
                    somme_branches = abs(poids)
                    mini1 = i
                    mini2 = k
        liste1 = liste_de_feuilles_disponibles[mini1]
        liste2 = liste_de_feuilles_disponibles[mini2]
        liste_de_feuilles_disponibles.remove(liste_de_feuilles_disponibles[max(mini1,mini2)]) #On retire les listes qui sont associées
        liste_de_feuilles_disponibles.remove(liste_de_feuilles_disponibles[min(mini1,mini2)])
        liste_de_feuilles_disponibles.append([liste1[0]+liste2[0], liste1 if(liste1[0] < liste2[0])else liste2, liste2 if(liste1[0] < liste2[0])else liste1])#On ajoute la somme des poids devant,On met la feuille la plus faible à gauche


    return liste_de_feuilles_disponibles[0] #Retourne l'arbre


def afficher_arbre(arbre, cheminParcouru, texte):
    """
    Affiche l’arbre dans la console
    """
    endroitActuel = arbre.copy()
    for k in cheminParcouru:
        endroitActuel = endroitActuel[k]
    texte += "\n  "
    for k in range(len(cheminParcouru) -1):
        if((cheminParcouru[k] == 1) and ((cheminParcouru[k:].count(2) !=cheminParcouru[k:].count(1)) or len(cheminParcouru[k:]) <= 2)):
            #SI on a prit à gauche ici, et que on a davantage prit à droite qu'à gauche, alors cet endroit n'est pas bouclé, donc on ajoute un |
            texte+="|       "
        else:
            texte+="        "
    texte+= "\--"+str(cheminParcouru[-1]-1)+"--(" + str(endroitActuel[0]) + ")"
    if (len(endroitActuel) != 2):  # Si on est pas dans une feuille
        cheminParcouru.append(1)
    else: #Si on est dans une feuille
        texte+=" "+es.string_from_byte(endroitActuel[1]) #On ajoute le caractère
        if (cheminParcouru.count(1) == 0):  # Si on est totalement à droite et que l'on est sur une feuille
            return texte

        cheminParcouru = remonterAuNoeudNonExplore(cheminParcouru)
        cheminParcouru.append(2)  # On prend à droite à cette case
    return afficher_arbre(arbre, cheminParcouru, texte)


def afficher_table(table):
    """
    Print la table dans la console
    :param table:
    :return:
    """
    print("##### TABLE #####")
    for carac,chemin in table.items():
        print(es.string_from_byte(carac).ljust(6)  +"===>  " + chemin)

def remonterAuNoeudNonExplore(cheminParcouru):
    """
    Remonte au dernier noeud non explore,  c'est a dire la derniere fois que l'on a prit a gauche puis prend à droite
    :param cheminParcouru:
    :return cheminParcouru:
    """
    unAtteint = False
    while (not unAtteint):
        if (cheminParcouru[len(cheminParcouru) - 1] == 2):
            del cheminParcouru[-1]
        else:
            unAtteint = True

    del cheminParcouru[-1]  # On remonte encore à la case juste au dessus
    return cheminParcouru

def arbreVersBits(arbre, cheminParcouru = [1], parcoursArbre = "0"):
    """
    Convertit la structure de l’arbre qui est sous forme d’une composition de listes en bits selon le parcours infixe.
    (Retourne la structure de l’arbre sous forme de bits (selon le parcours infixe))
    :param arbre:
    :param cheminParcouru:
    :param parcoursArbre:
    :return:
    """
    endroitActuel = arbre.copy()

    for k in cheminParcouru:#Endroit Actuel contient le noeud en cours de traitement
        endroitActuel = endroitActuel[k]

    if (len(endroitActuel) != 2):  # Si on est pas dans une feuille
        cheminParcouru.append(1)
        parcoursArbre+="0"
        return arbreVersBits(arbre, cheminParcouru,parcoursArbre)

    else:
        parcoursArbre += "1"
        if (cheminParcouru.count(1) == 0):  # Si on est totalement à droite et que l'on est sur une feuille
            return parcoursArbre

        cheminParcouru = remonterAuNoeudNonExplore(cheminParcouru)
        cheminParcouru.append(2)# On prend à droite à cette case

        return arbreVersBits(arbre, cheminParcouru, parcoursArbre)

def convertirTexte(texte, table):
    """
    Convertir le texte en byte en bits selon la table de Huffman
    Retourne une string de 0 et de 1 correspondant aux bits du texte de compressé
    :param texte:
    :param table:
    :return:
    """
    strDeBitsDuTexte = ""
    for t in texte:
        strDeBitsDuTexte += str(table[t])  # On rajoute les 0 et les 1 correspondant a chaque carac sous forme de string
    return strDeBitsDuTexte

def convertirHuffman(bitsTexte,arbre):
    """
    Décompresse les bits en octets selon l’arbre utilisé pour la compression
    (Retourne les octets correspondant au texte décompressé)
    """
    texte = []#liste de bits (representes par int de 0 et de 1)
    endroitActuel = arbre
    for bit in bitsTexte:
        bit +=1# car bit = 0 ou 1, et on veut bit = 1 pour gauche et bit = 2 pour droite
        if(len(endroitActuel[bit]) == 2):#Si l'endroit actuel est une feuille
            if(endroitActuel[bit][1] == -1):#Si on est a la fin du texte
                break
            texte.append(endroitActuel[bit][1])
            endroitActuel = arbre
        else:#Si ce n'est pas une feuille
            endroitActuel = endroitActuel[bit]
    return texte

def etablirTable(arbre, cheminParcouru= [1], table = dict()):
    """
    Fonction récursive
    (Retourne une liste contenant chaque caractère (sous forme d’octet) de l’arbre et son encodage de Huffman sous forme de bits (Table de Huffman))
    :param arbre:
    :param cheminParcouru: utilise pour se reperer lors de l'iteration suivante
    :param table:
    :return:
    """
    endroitActuel = arbre.copy() #Copie pour ne pas affecter l'arbre pendant l'algo

    for k in cheminParcouru:
        endroitActuel = endroitActuel[k]

    if(len(endroitActuel)!= 2): #Si on est pas dans une feuille
        cheminParcouru.append(1) #1 signifie gauche dans l'arbre, 2 signifie droite
        return etablirTable(arbre,cheminParcouru, table)

    else: # On est dans une feuille
        table[endroitActuel[1]] = ""

        for x in cheminParcouru: #Le chemin est stocké sous forme de string de 0 et de 1
            table[endroitActuel[1]] += str(x - 1)  # au lieu d'avoir 1 et 2, on veut 0 et 1

        if (cheminParcouru.count(1) == 0):  # Si on est totalement à droite et que l'on est sur une feuille(count 1 nous dit le nombre de fois que l'on a prit a gauche)
            return table

        cheminParcouru = remonterAuNoeudNonExplore(cheminParcouru)
        cheminParcouru.append(2) #On prend à droite à cette case
        return etablirTable(arbre, cheminParcouru, table)