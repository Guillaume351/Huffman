# -*- coding: utf-8 -*-
import sys
import es
import Huffman


def ouvrirFichier(arguments):
    """
    Ouvre le fichier si il est présent et vérifie que son extension est valide. Exemple extension invalide : .hff
    Erreur si il n’est pas valide, sinon appelle la fonction traiterFichier
    :param nomFichier:
    :return:
    """
    if (len(arguments) == 0):
        print("Pas d'arguments donnes. Le programme ne s'executera pas")
        return EnvironmentError
    bavard = False
    if (arguments[0] == "-b" or arguments[
        0] == "--bavard"):  # On verifie l'argument en première position, qui peut etre bavard
        nomFichier = arguments[1]
        bavard = True
    else:
        nomFichier = arguments[0]
    try:
        fichier = open(nomFichier, 'rb')
    except IOError:
        print("Fichier invalide")
        return FileNotFoundError
    if (len(nomFichier) >= 4 and nomFichier[len(nomFichier) - 4:] == ".hff"):
        print("Ce fichier est deja compresse !")
        return ValueError

    texteInBytes, dictCarac = Huffman.listerCarac(fichier)
    if (len(texteInBytes) <= 1):  # Si le fichier est vide ou contient un seul caractere
        print("Fichier vide ou trop petit. Le programme ne s'executera pas")
        return
    traiterFichier(dictCarac, texteInBytes, nomFichier, bavard)


def traiterFichier(dictCarac, texteInBytes, nomFichier, bavard):
    arbre = Huffman.creerArbre(dictCarac)
    table = Huffman.etablirTable(arbre)

    strBitsArbre = (Huffman.arbreVersBits(arbre))  # Recupere structure infixe de l'abre en string de 0 et 1

    strBitsTexte = Huffman.convertirTexte(texteInBytes, table)
    strBitsTexte += str(table[-1])  # On ajoute le carac de fin de texte

    strBitsArbreEtTexte = strBitsArbre + strBitsTexte

    bytesArbreEtTexte = []
    for i in range(len(strBitsArbreEtTexte) // 8):  # Cette boucle convertit string de 0 et 1 vers liste de bytes
        value = ""
        for k in range(8):  # On recupere les 8 bits suivants
            if (8 * i + k < len(strBitsArbreEtTexte)):  # Si on ne depasse pas le nombre de bits
                value += strBitsArbreEtTexte[8 * i + k]
            else:  # On complete avec des 0 pour avoir des bytes entiers
                value += "0"
        bytesArbreEtTexte.append(int(value, 2))  # On convertit en bytes
    listeBytesCarac = []
    listeCaracTemporaire = []

    k = 0
    for carac, bits in table.items():  # On fait passer le rang du carac de fin de fichier en premier

        if (carac == -1):  # On ajoute le rang du caractère de fin de fichier
            listeBytesCarac.append(k)
        else:  # Dans une autre liste on ajoute à la suite les caractères
            listeCaracTemporaire.append(carac)
        k += 1
    listeBytesCarac += listeCaracTemporaire  # On a ici rang du caractere de fin de fichier puis liste des autres caracteres
    listeBytesCarac.append(listeBytesCarac[-1])  # ON double le dernier caractere

    if (bavard):
        print(Huffman.afficher_arbre(arbre, [1], "##### ARBRE #####\n(" + str(arbre[0]) + ")"))
        Huffman.afficher_table(table)

    enregistrerFichier(listeBytesCarac + bytesArbreEtTexte, nomFichier)


def enregistrerFichier(donnees, nomFichier):
    """
    Créer un fichier en .hff contenant dans l’ordre la structure de l’arbre, les caractères de l’arbre puis le texte sous forme de bits
    :param donnees: liste de bytes
    :return:
    """
    fichier = open(nomFichier + ".hff", 'wb')
    for b in donnees:
        es.write_byte(fichier, b)


if __name__ == "__main__":
    ouvrirFichier((sys.argv[1:]))
