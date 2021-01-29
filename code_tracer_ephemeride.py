# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 16:25:31 2021

@author: Utilisateur
"""

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
import code_visu_ephemeride

##############################################################################
################      MANIPULATIONS    ######################################
#############      MISE EN FORME DES DONNEES    ##############################
##############################################################################

def petite_conversion_coord_float(data_one_sat):
    '''
    Convertis les coords de position de str à float

    Parameters
    ----------
    data_one_sat : TYPE list
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    for l in data_one_sat:
        l[1] = float(l[1])
        l[2] = float(l[2])
        l[3] = float(l[3])
    
    return data_one_sat

def liste_pour_graphique(data_one_sat):
    '''
    Crée à partir des données sur une journée d'un seul satellite une liste contenant 
    uniquement les coord comme suit
    [ [tous les X_ccordinates] , [tous les Y-coordinates] , [tous les Z-coordinates] ]
    Cela permet de plot ces positions via la fonction "tracer".
    
    Parameters
    ----------
    data_one_sat : TYPE list
        DESCRIPTION.

    Returns
    -------
    the_list : TYPE list
        DESCRIPTION.

    '''
    the_list = [[],[],[]]
    for l in data_one_sat:
        the_list[0].append(l[1])
        the_list[1].append(l[2])
        the_list[2].append(l[3])
    
    return the_list

def sat_machin(chemin):
    #Choix du fichier
    fichier_ephemeride = code_visu_ephemeride.choisir_fichier_specifique(chemin)
    
    #Choix du satellite 
    nom_sat = code_visu_ephemeride.choix_satellite(fichier_ephemeride)
    print("\nVous avez choisi le satellite : ",nom_sat)
    
    #extraction des coordonnées du satellite choisi avec vérification d la correction d'horloge
    
    coordonnees = code_visu_ephemeride.coord_satellite( fichier_ephemeride, nom_sat )
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','exponent-X-deviation','exponent-Y-deviation','exponent-Z-deviation','exponent-clock-deviation']

    
    #prise en compte de la déviation de position
    coord_avec_devia_pos = code_visu_ephemeride.deviation_position(fichier_ephemeride,coordonnees)
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','X-deviation','Y-deviation','Z-deviation','exponent-clock-deviation']
    
    
    #prise en compte de la déviation d'horloge
    coord_avec_devia_pos_et_clock_corr = code_visu_ephemeride.deviation_horloge(fichier_ephemeride,coord_avec_devia_pos)
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','X-deviation','Y-deviation','Z-deviation','clock-deviation']

    
    #affichage de la position avec déviation et seconde de la semaine avec correction et déviation horloge
    coord_finales_et_secondeofweek = code_visu_ephemeride.prise_en_compte(fichier_ephemeride, coord_avec_devia_pos_et_clock_corr)
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'seconde of week','X-deviation','Y-deviation','Z-deviation','clock-deviation']
    return petite_conversion_coord_float(coord_finales_et_secondeofweek)

def sat_machin_2(chemin,number):
    #Choix du fichier
    fichier_ephemeride = code_visu_ephemeride.choisir_fichier_specifique(chemin)
    
    #Choix du satellite 
    nom_sat = code_visu_ephemeride.choix_satellite_2(fichier_ephemeride,number)
    print("\nVous avez choisi le satellite : ",nom_sat)
    
    #extraction des coordonnées du satellite choisi avec vérification d la correction d'horloge
    
    coordonnees = code_visu_ephemeride.coord_satellite( fichier_ephemeride, nom_sat )
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','exponent-X-deviation','exponent-Y-deviation','exponent-Z-deviation','exponent-clock-deviation']

    
    #prise en compte de la déviation de position
    coord_avec_devia_pos = code_visu_ephemeride.deviation_position(fichier_ephemeride,coordonnees)
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','X-deviation','Y-deviation','Z-deviation','exponent-clock-deviation']
    
    
    #prise en compte de la déviation d'horloge
    coord_avec_devia_pos_et_clock_corr = code_visu_ephemeride.deviation_horloge(fichier_ephemeride,coord_avec_devia_pos)
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','X-deviation','Y-deviation','Z-deviation','clock-deviation']

    
    #affichage de la position avec déviation et seconde de la semaine avec correction et déviation horloge
    coord_finales_et_secondeofweek = code_visu_ephemeride.prise_en_compte(fichier_ephemeride, coord_avec_devia_pos_et_clock_corr)
    # ['nom','X-coordinate','Y-coordinate','Z-coordinate,'seconde of week','X-deviation','Y-deviation','Z-deviation','clock-deviation']
    return petite_conversion_coord_float(coord_finales_et_secondeofweek)
  

##############################################################################
####################     TRACER      #########################################
##############################################################################

  
def tracer_3sat(coord1,coord2,coord3):
    '''
    Trace sur un graphe en 3D les coord sur un jour de 2 satellites de coord coord1 et coord2

    Parameters
    ----------
    coord1 : TYPE list des donnees d'un sat sur 1 jour
        DESCRIPTION.
    coord2 : TYPE list des donnees d'un sat sur 1 jour
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    #Affichage
    [X_s1,Y_s1,Z_s1] = liste_pour_graphique(coord1)
    [X_s2,Y_s2,Z_s2] = liste_pour_graphique(coord2)
    [X_s3,Y_s3,Z_s3] = liste_pour_graphique(coord3)
   
    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    ax.set_title('PG01 PG02 PG03 le 12.09.2019')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.scatter(X_s1,Y_s1,Z_s1, zdir='z', c= 'blue')
    ax.scatter(X_s2,Y_s2,Z_s2, zdir='z', c= 'green')
    ax.scatter(X_s3,Y_s3,Z_s3, zdir='z', c= 'red')
    plt.savefig("Visualisation/PG01-2-3_12.09.2021.png")
    
def tracer_ts_sat():
    '''
    Trace sur un graphique les positions à l'instant 1 de tous les satellites du fichier igs20704.sp3

    Returns
    -------
    None.

    '''
    #intialisation
    Liste_coords_t0 = []
    #Jremplissage avec 1ere coord de chaque sat d'un fichier
    for k in range(32):
        coord = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20704.sp3',k+1)
        Liste_coords_t0.append(coord[0])
    #pr tracer
    [X_s1,Y_s1,Z_s1] = liste_pour_graphique(Liste_coords_t0)
    
    fig = plt.figure(2)
    #ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    ax.set_title('31 satellites GPS semaine 2070')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.scatter(X_s1,Y_s1,Z_s1, zdir='z', c= 'red')
    plt.savefig("Visualisation/tous-sat-t0-20704.png")
    
def tracer_1sat_all_week(number):
    '''
    Trace sur un graphe en 3D les coord sur une semaine d'un satellites

    Parameters
    ----------
    number : TYPE integer
        DESCRIPTION. le nom du satellite

    Returns
    -------
    None.

    '''
    #coord
    coord_j0 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20700.sp3',number)
    coord_j1 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20701.sp3',number)
    coord_j2 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20702.sp3',number)
    coord_j3 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20703.sp3',number)
    coord_j4 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20704.sp3',number)
    coord_j5 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20705.sp3',number)
    coord_j6 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20706.sp3',number)
    
    #Affichage
    [X_s0,Y_s0,Z_s0] = liste_pour_graphique(coord_j0)
    [X_s1,Y_s1,Z_s1] = liste_pour_graphique(coord_j1)
    [X_s2,Y_s2,Z_s2] = liste_pour_graphique(coord_j2)
    [X_s3,Y_s3,Z_s3] = liste_pour_graphique(coord_j3)
    [X_s4,Y_s4,Z_s4] = liste_pour_graphique(coord_j4)
    [X_s5,Y_s5,Z_s5] = liste_pour_graphique(coord_j5)
    [X_s6,Y_s6,Z_s6] = liste_pour_graphique(coord_j6)
   
    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    ax.set_title('PG'+str(number)+' semaine 2070')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.scatter(X_s1,Y_s1,Z_s1, zdir='z', c= 'blue')
    ax.scatter(X_s2,Y_s2,Z_s2, zdir='z', c= 'green')
    ax.scatter(X_s3,Y_s3,Z_s3, zdir='z', c= 'red')
    ax.scatter(X_s1,Y_s1,Z_s1, zdir='z', c= 'pink')
    ax.scatter(X_s2,Y_s2,Z_s2, zdir='z', c= 'purple')
    ax.scatter(X_s3,Y_s3,Z_s3, zdir='z', c= 'brown')
    ax.scatter(X_s3,Y_s3,Z_s3, zdir='z', c= 'black')

    plt.savefig("Visualisation/All_week_PG"+str(number)+".png")
    
def tracer_1sat_dmyy(number):
    '''
    Trace sur un graphe en 3D les coord d'un satellite sur 1jour à 4 dates :
        t0 , t0+1jour, to+1semaine, t0+1mois, t0+1an, t0+12ans

    Parameters
    ----------
    number : TYPE integer
        DESCRIPTION. le nom du satellite

    Returns
    -------
    None.

    '''
    #coord
    coord_j0 = sat_machin_2('fichiers_ephemerides/1548_week_GPS/igs15480.sp3',number)
    coord_j1 = sat_machin_2('fichiers_ephemerides/1548_week_GPS/igs15481.sp3',number)
    coord_j3 = sat_machin_2('fichiers_ephemerides/1552_week_GPS/igs15520.sp3',number)
    coord_j4 = sat_machin_2('fichiers_ephemerides/1600_week_GPS/igs16000.sp3',number)
    coord_j5 = sat_machin_2('fichiers_ephemerides/2122_week_GPS/igs21220.sp3',number)
    
    #Affichage
    [X_s0,Y_s0,Z_s0] = liste_pour_graphique(coord_j0)
    [X_s1,Y_s1,Z_s1] = liste_pour_graphique(coord_j1)
    [X_s3,Y_s3,Z_s3] = liste_pour_graphique(coord_j3)
    [X_s4,Y_s4,Z_s4] = liste_pour_graphique(coord_j4)
    [X_s5,Y_s5,Z_s5] = liste_pour_graphique(coord_j5)
   
    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    ax.set_title('PG01')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot(X_s0,Y_s0,Z_s0, zdir='z', c= 'red')
    ax.plot(X_s1,Y_s1,Z_s1, zdir='z', c= 'green')
    ax.plot(X_s3,Y_s3,Z_s3, zdir='z', c= 'blue')
    ax.plot(X_s4,Y_s4,Z_s4, zdir='z', c= 'black')
    ax.plot(X_s5,Y_s5,Z_s5, zdir='z', c= 'purple')
    ax.scatter(X_s0[0],Y_s0[0],Z_s0[0], zdir='z', c= 'red')


    plt.savefig("Visualisation/Comparison_dmyy"+str(number)+".png")

##############################################################################
##################     PRECISION POSITION      ###############################
##############################################################################
    
def distance_3D(List1,List2):
    '''
    Calcul la distance euclidienne entre 2points ayant 3 coordonnées

    Parameters
    ----------
    List1 : TYPE [X-coord, Y-coord, Z-coord]
        DESCRIPTION. coord en km
    List2 : TYPE [X-coord, Y-coord, Z-coord]
        DESCRIPTION. coord en km

    Returns distance en km
    -------
    TYPE
        DESCRIPTION.

    '''
    return numpy.sqrt( (List1[0]-List2[0])**2 + (List1[1]-List2[1])**2 + (List1[2]-List2[2])**2 )
    
def ecart(coord_j1,coord_j2,number):
    '''
    Retourne l'écart de position du satellite n°number entre 2 jours choisis
    Parameters
    ----------
    coord_j1 : TYPE list
        DESCRIPTION. list de list des coord du sat n°number sur un jour
    coord_j2 : TYPE
        DESCRIPTION. list de list des coord du sat n°number sur un autre jour
    number : TYPE integer
        DESCRIPTION. le numéro du satellite à étudier

    Returns
    -------
    ecart_minimal : TYPE float
        DESCRIPTION. L'écart de position 

    '''

    
    #On compare la première position du satellite car on met l'indice 0
    x1,y1,z1 = coord_j1[0][1],coord_j1[0][2],coord_j1[0][3]
    
    #initialisation
    ecart_minimal = distance_3D([x1,y1,z1],coord_j2[0-1][1:4])
    
    #L_tt_ecart=[]
    
    for sat in coord_j2:
        ecart = distance_3D([x1,y1,z1],sat[1:4])
        # if ecart<1000:
        #     L_tt_ecart.append([ecart,sat[4]])
        if ecart < ecart_minimal:   #mise à jour de l'écart minimal
            ecart_minimal = ecart
            
    return ecart_minimal
    
    

if __name__ == "__main__" :
    
    
    
    #trace trajet 3 satellites sur 24h le jeudi
    coord_s1 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20704.sp3',1)
    coord_s2 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20704.sp3',2)
    coord_s3 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20704.sp3',3)
    
    tracer_3sat(coord_s1, coord_s2, coord_s3)
    
    
    
    #tracer toute une semaine 1 satellite
    tracer_1sat_all_week(12)
    
    
    #precision position sat 12 de dimanche à lundi
    coord_jour1 = sat_machin_2('fichiers_ephemerides/2070_week_GPS/igs20700.sp3',12)
    coord_jour2 = sat_machin_2('fichiers_ephemerides/2076_week_GPS/igs20760.sp3',12)
    
    precision = ecart(coord_jour1,coord_jour2,12)
    print(precision)
    
    