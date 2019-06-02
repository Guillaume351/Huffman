# -*- coding: utf-8 -*-
import pytest
import Huffman, Compresser, Decompresser

def testsHuffman():
    print("### Tests Huffman ###")
    assert Huffman.creerArbre(dict()) == [0,-1]#Arbre poids 0, caractere de fin de fichier seulement
    assert Huffman.creerArbre({100:3,101:1})==[4,[1,[0,-1],[1,101]],[3,100]]
    assert Huffman.creerArbre({100: 0}) == [0, [0, 100], [0, -1]]

    assert Huffman.remonterAuNoeudNonExplore([1,1,2,2,2]) == [1] #Doit remonter juste avant la derniere fois ou on a prit a gauche. 1 signifie gauche, 2 droite
    assert Huffman.remonterAuNoeudNonExplore([1]) == []

    assert Huffman.arbreVersBits([4,[1,[0,-1],[1,101]],[3,100]]) == "00111"


    print("### Huffman - OK ###")


def testsCompresser():
    print("### Tests Compresser ###")
    assert Compresser.ouvrirFichier([]) is EnvironmentError
    assert Compresser.ouvrirFichier([""]) == FileNotFoundError  # Doit faire une erreur de fichier invalide
    print("### Compresser - OK ###")

def testsDecompresser():
    print("### Tests Decompresser ###")
    assert Decompresser.ouvrirFichier([]) is EnvironmentError
    assert Decompresser.ouvrirFichier([""]) == FileNotFoundError #Doit faire une erreur de fichier invalide
    print("### Decompresser - OK ###")

if __name__ == "__main__":
    print("Debut du test de fonction. A noter : le programme va print des messages d'erreur volontaires provoques par les tests.")
    testsHuffman()
    testsCompresser()
    testsDecompresser()