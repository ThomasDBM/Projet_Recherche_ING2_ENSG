# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 21:42:26 2021

modifie les fichier créés par Vu_du_ciel() dans le script du même nom pour qu'ils soient lisible par Circé

@author: thoma_000
"""

#on ouvre les fichiers
inpout=open ("Resultat/Limite_vue_du_ciel_392845.800932.csv",'r')
outpout=open("Resultat/Limite_vue_du_ciel_392845.800932_mod.csv",'w')
#on les lit
lignes=inpout.readlines()
#on ferme les fichiers
inpout.close()

# print(lignes)

#pour chaque ligne on modifie la facon dont elle est ecrite
for ligne in lignes:
    coords=ligne.split(',')
    outpout.write(coords[0]+'     '+coords[1]+'     '+coords[2])
    
#on ferme les fichiers
outpout.close()



