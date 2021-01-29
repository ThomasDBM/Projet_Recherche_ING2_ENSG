# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 11:28:25 2021

@author: thoma_000
"""

#importation des modules
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D


#execution de code_visu_ephemeride pour pouvoir obtenir les coordonnées des satellites à l'heure voulue
exec(open("code ephemeride elliott/Position_satellites.py").read()) # attention au chemin


#ouverture du fichier obtenu apres conversion dans Circé
fichier_vue_ciel = open ("Resultat/Limite_vue_du_ciel_392845.800932_conv1.csv",'r',encoding="utf8") #attention au chemin   
#lecture du fichier
points= fichier_vue_ciel.readlines()
#fermeturdu fichier
fichier_vue_ciel.close()


def traitement_points_lambert(points):
    """
    traite les données du fichier de point(avant d'être passé par circé) pour le renvoyer sous forme de liste

    Parameters
    ----------
    points : fichier
        Fichier contenant les points.

    Returns
    -------
    liste contenant les points

    """
    points_traites=[]
    for k in range(len(points)):
        
        coords=points[k].split(',')
        coords[2]=coords[2][:-1]
        
        points_traites.append([float(coords[0]),float(coords[1]),float(coords[2])])
    return(points_traites)
        
def traitement_points_ITRF(points):
    """
    traite les données du fichier de point(avant d'être passé par circé) pour le renvoyer sous forme de liste

    Parameters
    ----------
    points : fichier
        Fichier contenant les points.

    Returns
    -------
    liste contenant les points

    """
    points_traites=[]
    for k in range(17,len(points)):
        
        coords=points[k].split(' ')
        
        points_traites.append([float(coords[2]),float(coords[5]),float(coords[7])])
    return(points_traites)

def creation_triangles(points,centre):
    """
    associe les points 3 par trois afin de pouvoir tracer les la séparation entre la zone visible et non visible

    Parameters
    ----------
    points : liste
        contient tous les points calculés.
    centre : TYPE
        coordonées du point d'origine des calculs.

    Returns
    -------
    une liste de triangles definis par leur trois sommets.
    """
    
    triangles=[]
    
    for i in range(len(points)-1):
        sommeti=(points[i][0],points[i][1],points[i][2])
        sommetip1=(points[i+1][0],points[i+1][1],points[i+1][2])
        triangles.append((centre,sommeti,sommetip1))
        
    triangles.append((centre,(points[-1][0],points[-1][1],points[-1][2]),(points[0][0],points[0][1],points[0][2])))
    return(triangles)


def traitement_sat(sat):
    """
    traite les données issue du fichier du satellite

    Parameters
    ----------
    sat :list
        liste contenant les coordonnées des satellites au debut et a lfin de la tranche de 15 minute qui contient l'heure demandée.

    Returns
    -------
    les coordonnées moyennes des satellites durant ces 15 minutes

    """
    coords_sat=[]
    for k in range(len(sat[0])):
        xsat=((float(sat[0][k][1])+float(sat[1][k][1]))/2)*10**3
        ysat=((float(sat[0][k][2])+float(sat[1][k][2]))/2)*10**3
        zsat=((float(sat[0][k][3])+float(sat[1][k][3]))/2)*10**3
        coords_sat.append([xsat,ysat,zsat])
    return(coords_sat)

def créer_vect_sattellite(coord_sat):
    """
    crée les vecteurs donnant la direction de chaque satellites

    Parameters
    ----------
    coord_sat :list
        liste contenant les coordonnées des satellites au debut et a lfin de la tranche de 15 minute qui contient l'heure demandée.

    Returns
    -------
    Les vecteurs unitaires de direction des satellites

    """
    vects_uni=[]   
    for k in range(len(coord_sat)): #len(coord_sat)
        
        vect=[coord_sat[k][0]-Xcentre,coord_sat[k][1]-Ycentre,coord_sat[k][2]-Zbase]
        norme=np.sqrt((vect[0]**2)+(vect[1]**2)+(vect[2]**2))
        
        vect_uni=[vect[0]/norme,vect[1]/norme,vect[2]/norme]
        
        vects_uni.append(vect_uni)
        
    return(vects_uni)

def trace_direction_gps(mu,coord_sat,color):  #ne fonctionne pas !!!
        """
        trace les directions des GPS

        Parameters
        ----------
        mu : integer
            indique la taille du segment indiquant le direction.
        
        coord_sat : list
            coordonnées des satellites.
        
        color: str
            couleur d'affichage.

        Returns
        -------
        none.

        """
        vects=créer_vect_sattellite(coord_sat)
        for k in range(len(coord_sat)): #len(coord_sat)
            ax.plot([Xcentre,Xcentre+mu*vects[k][0]],[Ycentre,Ycentre+mu*vects[k][1]],[Zbase,Zbase+mu*vects[k][2]],color)


def SatInVue(sats,Vue,centre): #ne fonctionne pas
    """
    
    recupère les satéllites visibles depuis le point

    Parameters
    ----------       
    sats : list
        coordonnées des satellites.
    
    Vue : list
        coordonées des points de limite de la vue du ciel
        
    centre: list
        coordonnées du point central

    Return
    -------
    la liste des satellites qui sont visibles
    
    """
    #création de la liste finale
    vects_in_vue=[]
    #vectorisation des direction des satellites
    vects=créer_vect_sattellite(sats)
    
    #pour chaques satellites
    for vect in vects:
        test=False   #on suppose qu'il n'est pas dedans
        A=np.array(Vue[1]) #on prend le premier point de la liste de vue du ciel
        for Bl in Vue:  #on parcours tous les autres pour créer des triangles sur toute la surface 
            B=np.array(Bl) 
            for Cl in Vue:     
                C=np.array(Cl)
                #création du plan passant par ABC
                AB=B-A
                AC=C-A
                n=np.cross(AB,AC)
                #calcul du point d'intersection entre le plan ABC et la droite passant par le centre et le sattellite
                mu=((n[0]*A[0]+n[1]*A[1]+n[2]*A[2])-(n[0]*centre[0]+n[1]*centre[1]+n[2]*centre[2]))/(n[0]*vect[0]+n[1]*vect[1]+n[2]*vect[2])
                Psat=np.array([centre[0]+mu*vect[0],centre[1]+mu*vect[1],centre[2]+mu*vect[2]])
                        
                #calcul des produits vectoriels
                PA=Psat-A
                PB=Psat-B
                PC=Psat-C
                PAPB=np.cross(PA,PB)
                PBPC=np.cross(PB,PC)
                PCPA=np.cross(PC,PA)
                
                #calcul de la valeur du cosinus de l'angle entre les trois vecteurs
                PAPBscalPBPC=(PAPB[0]*PBPC[0]+PAPB[1]*PBPC[1]+PAPB[2]*PBPC[2])/np.sqrt(((PAPB[0]*PBPC[0])**2)+((PAPB[1]*PBPC[1])**2)+((PAPB[2]*PBPC[2])**2))
                PAPBscalPCPA=(PAPB[0]*PCPA[0]+PAPB[1]*PCPA[1]+PAPB[2]*PCPA[2])/np.sqrt(((PAPB[0]*PCPA[0])**2)+((PAPB[1]*PCPA[1])**2)+((PAPB[2]*PCPA[2])**2))
                        
                #si il vaut 1, les trois vecteurs resultat des produits vectoriels sont colinéaires et de même sens <=> le point est dans le triangle <=> le satellite est visible
                if PAPBscalPBPC==PAPBscalPCPA==1:
                    test=True

        #si le satellite est visible on l'enregistre dans le doc        
        if test:
            vects_in_vue.append(vect)
        
    return(vects)

                
        
    
    
    
#on traite les pointsde vue du ciel
Pvue= traitement_points_ITRF(points)
# Pvue= traitement_points_lambert(points)

#on crée les variables es coordonées du centre
Xcentre=Pvue[0][0]
Ycentre=Pvue[0][1]
Zbase=Pvue[0][2]

#on créé les triangles 
triangles=creation_triangles(Pvue[2:], (Xcentre,Ycentre,Zbase))

#on lance la fonction présente dans code_visu_ephemeride, on traite ces données, on en fait des vecteur, et on cherche ceux qui sont visible
sattelites=co_sat(392845.800932)
coord_sat=traitement_sat(sattelites)
Sat_Vect=créer_vect_sattellite(coord_sat)
Sat_Vue=SatInVue(coord_sat,Pvue,[Xcentre,Ycentre,Zbase])


#affichage graphique 
fig2=plt.figure(2)
ax = Axes3D(fig2)
ax.set_title('donner un titre')
ax.set_xlabel('X')
ax.set_xlim(Xcentre-20,Xcentre+20)
ax.set_ylabel('Y')
ax.set_ylim(Ycentre-20,Ycentre+20)
ax.set_zlabel('Z')
ax.set_zlim(Zbase-10, Zbase+20)
ax.view_init(0,20)



#on peut tracer plusieur choses :

# #les trinagles de séparation zone visible/zone nonvisible
# for triangle in triangles:
#     trace = Poly3DCollection([triangle], alpha=0.7)
#     ax.add_collection3d(trace)
    
# #la direction des gps grace a la fonction(qui ne fonctionne pas)    
# trace_direction_gps(10,Sat_Vue,'r')

# #la direction de tous les gps
# for k in range(len(coord_sat)): #len(coord_sat)
#     ax.plot([Xcentre,Xcentre+15*Sat_Vect[k][0]],[Ycentre,Ycentre+15*Sat_Vect[k][1]],[Zbase,Zbase+15*Sat_Vect[k][2]],'r')

# #la direction des gps visibles
# for k in range(len(coord_sat)): #len(coord_sat)
#     ax.plot([Xcentre,Xcentre+15*Sat_Vue[k][0]],[Ycentre,Ycentre+15*Sat_Vue[k][1]],[Zbase,Zbase+15*Sat_Vue[k][2]],'r')

# #les segments entre le centre et les positions de chaque gps
# for k in range(len(coord_sat)): #len(coord_sat)
#     ax.plot([Xcentre,coord_sat[k][0]],[Ycentre,coord_sat[k][1]],[Zbase,coord_sat[k][2]],'r')

#le points central
ax.scatter3D(Xcentre,Ycentre,Zbase, c='r')

# #deux points de la vue du ciel qui s'opposent
# ax.scatter3D(Pvue[1][0],Pvue[1][1],Pvue[1][2], c='g')
# ax.scatter3D(Pvue[int(len(Pvue[1:])/2)+1][0],Pvue[int(len(Pvue[1:])/2)+1][1],Pvue[int(len(Pvue[1:])/2)+1][2], c='g')

# #la position des satellites
# for k in range(len(sattelites[0])):
#     ax.scatter3D(float(coord_sat[k][0]),float(coord_sat[k][1]),float(coord_sat[k][2]),c='g')

# #les points de limite de vue du ciel
# for point in Pvue[2:]:
#     ax.scatter3D(point[0],point[1],point[2], c='b')
