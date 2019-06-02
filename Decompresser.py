# coding=utf-8
import es
import sys
import Huffman


def ouvrirFichier(arguments):
    """
    Ouvre le fichier et vérifie que son contenu/son extension est valide. Ouvre le fichier si il est présent et vérifie que son contenu/son extension est valide
    Erreur si il n’est pas valide, sinon appelle la fonction traiterFichier
    :param nomFichier:
    :return:
    """
    if (len(arguments) == 0):
        print("Pas d'arguments donnes. Le programme ne s'executera pas")
        return EnvironmentError
    bavard = False
    if (arguments[0] == "-b" or arguments[0] == "--bavard"):
        nomFichier = arguments[1]
        bavard = True
    else:
        nomFichier = arguments[0]
    try:
        fichier = open(nomFichier, 'rb')
    except IOError:
        print("Fichier invalide")
        return FileNotFoundError

    if (len(nomFichier) < 4 or nomFichier[len(nomFichier) - 4:] != ".hff"):
        print("Mauvaise extension! Ce n'est pas un fichier compresse")
        return ValueError
    listeBits = list(es.bits(fichier))
    traiterFichier(listeBits, nomFichier, bavard)


def traiterFichier(bitsDuFichier, nomFichier, bavard):
    """
    Fait appel aux fonctions Huffman (dans Huffman.py) pour déterminer la structure de l’arbre, séparer les bit arbre des bits caractères des bits de texte et récupérer le texte, puis appelle la fonction enregistrerFichier
    :param bitsDuFichier: liste de bits
    :return: 
    """
    listeBits, listeCaracs = separerCarac(
        bitsDuFichier)  # bitsDuFichier ne contient plus que arbre + texte apres cette ligne

    nombreDeFeuilles = 0

    def reconArbre(arbre, listeBits):
        nonlocal nombreDeFeuilles
        if (listeBits[0] == 1):  # Si on est sur une feuille
            if (nombreDeFeuilles != listeCaracs[0]):
                if (nombreDeFeuilles >= listeCaracs[0]):  # Pour ne pas compter le carac de fin de fichier qui decale
                    carac = listeCaracs[nombreDeFeuilles]
                else:
                    carac = listeCaracs[nombreDeFeuilles + 1]
            else:
                carac = -1  # Caractere de fin de fichier
            nombreDeFeuilles += 1
            return [0, carac]  # On retourne la feuille
        else:
            k = 0  # Cette partie permet de détecter à quel endroit est la branche droite. Pour cela, elle compte le nombre de sous branches (0) et le nombre de caracteres (1) jusqu'a qu'ils s'egalisent. La fin de la branche est donc au k ieme bit
            count = [0, 0]
            for i in listeBits:
                k += 1
                if (i == 0):
                    count[0] += 1
                else:
                    count[1] += 1
                if (count[0] == count[1]):
                    break

            return [0, reconArbre(arbre, listeBits[1:]), reconArbre(arbre, listeBits[k:])]  # On retourne le noeud

    arbre = reconArbre([], listeBits)
    if (bavard):
        print(Huffman.afficher_arbre(arbre, [1], "(" + str(arbre[0]) + ")"))
    donnees = Huffman.convertirHuffman(bitsDuFichier[2 * len(listeCaracs) - 1:], arbre)
    enregistrerFichier(donnees, nomFichier)


def separerCarac(listeBits):
    finCarac = False
    listeCarac = []
    while (not finCarac):
        caracActuel = ""
        for k in range(8):  # On rajoute 8 bits dans un string
            caracActuel += str(listeBits.pop(0))
        if (listeCarac.count(int(caracActuel, 2)) != 0 and int(caracActuel, 2) != listeCarac[
            0]):  # Si le carac actuel existe deja et que ce n'est pas le premier, car le premier est le rang du carac de fin de caractere
            finCarac = True
        else:
            listeCarac.append(int(caracActuel, 2))  # Conversion du string de 8 bits en byte
    return listeBits, listeCarac


def enregistrerFichier(donnees, nomFichier):
    """
    Créer un fichier contenant dans les octets du texte décompressé
    :param texte: liste de bits
    :return:
    """

    fichier = open(nomFichier[:len(nomFichier) - 4], 'wb')  # On retire .hff
    for b in donnees:
        es.write_byte(fichier, b)  # On ecrit tous les bytes dans le fichier


if __name__ == "__main__":
    ouvrirFichier((sys.argv[1:]))
