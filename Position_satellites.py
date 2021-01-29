# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:42:02 2021

@author: Utilisateur
"""

import numpy as np
import copy

def choisir_fichier(nom):
    '''
    Traduit fichier ephemeride sous forme de liste dont chaque ligne est un élément de la liste

    Returns
    -------
    contenu : TYPE list
        DESCRIPTION. list qui contient info fichier ephemerides choisis

    '''
    nom_fichier = nom
    
    fichier1 = open('code ephemeride elliott/2070_week_GPS/'+nom_fichier,'r')
    contenant = fichier1.readlines()    
    fichier1.close()
    
    return contenant
    

def choix_satellite(data):
    '''
    Cette fonction retourne le nom du satellite choisi dans un fichier d'éphéméride'

    Parameters
    ----------
    data : TYPE list
        DESCRIPTION.
    line : TYPE integer
        DESCRIPTION.

    Returns
    -------
    nom : TYPE str
        DESCRIPTION. nom du satellite choisi

    '''
    line = int(input("Satellite numero combien ?"))
    if line == 0:
        print("La numérotation commence à 1.")
        line = int(input("Satellite numéro combien ? "))
        
    nom = ''
    for k in data[line+24-2]:
        if k == ' ':
            break
        else:
            nom += k
    return nom


def coord_satellite(data):
    List_pos_sat = []
    List_ttes_pos_sat_par_heure=[]
    List_ttes_pos_sat = []
    compteur=0
    #les coord commencent à partir de la ligne 23, indicée 22 sous python
    for k in range(22, len(data)):
        if data[k][0]=='P':
            compteur+=1
            #réécriture de la ligne en liste
            List_pos_sat = organiser_ligne(data[k])
            #ajout au dictionnaire des positions
            List_ttes_pos_sat_par_heure.append(List_pos_sat)
            
            if compteur==32:
                List_ttes_pos_sat.append(List_ttes_pos_sat_par_heure)
                List_ttes_pos_sat_par_heure=[]
                compteur=0
     
    #vérification de la correction d'horloge (cf. fonction associée)
    verif_corr_horloge(List_ttes_pos_sat)
    
    return List_ttes_pos_sat



def organiser_ligne(line):
    '''
    Réorganise la donnée de position d'un satellite d'un fichier éphéméride

    Parameters
    ----------
    line : TYPE str
        DESCRIPTION. nom, coord x,y,z et clock d'un satellite à un instant t

    Returns
    -------
    mylist : TYPE list
        DESCRIPTION. mêmes infos mais dans une liste pour y avoir mieux accès

    '''
    
    mylist = line.split(' ')
    for k in range(len(mylist)-1,0,-1):
        if mylist[k] == ''or mylist[k]=='\n':
            mylist.remove(mylist[k])

    return mylist

def date_gregorienne(data):
    info = organiser_ligne(data[22])
    year, month, day = info[1], info[2], info[3]
    
    return day+'/'+month+'/'+year
    
def date_satellite(data):
    info = organiser_ligne(data[1])
    week = info[1]
    return week

def horaire_gregorien(data):
    info = organiser_ligne(data[22])
    hour, minute, second = info[4], info[5], info[6]
    return hour+' H '+minute+' MIN '+second+' S'

def horaire_satellite(data):
    info = organiser_ligne(data[1])
    second_of_week = info[2]
    return second_of_week

def deviation_position(data,data_of_sats):
    '''
    Cette fonction remplace les exposants des déviations de la position par les valeurs de déviations en millimètres.

    Parameters
    ----------
    data : TYPE list of str
        DESCRIPTION. fichier brute d'ephemerides'
    data_of_one_sat : TYPE list of lists
        DESCRIPTION. list des positions, correction horloge, exposants deviations position et horloge d'un satellite'

    Returns
    -------
    new_coord : TYPE
        DESCRIPTION.

    '''
    
    new_coord = copy.deepcopy(data_of_sats)
    #extraction du base floating point number
    lign15 = organiser_ligne(data[14])
    number = float(lign15[1])
    
    #extraction of the two-digit exponents for the X-Y-Z-coordinates in units of millimeters
    for i in range(len(data_of_sats)):
        for k in range(len(data_of_sats[i])):
            if len(data_of_sats[i][k])>=9:  #vérifie si l'exposant est bien présent
                #X-coordinates
                new_coord[i][k][5] = number ** int(data_of_sats[i][k][5])
                #Y-coordinates
                new_coord[i][k][6] = number ** int(data_of_sats[i][k][6])
                #Z-coordinates
                new_coord[i][k][7] = number ** int(data_of_sats[i][k][7])
        
    return new_coord


def verif_corr_horloge(data_of_sats):
    '''
    Cette fonction détecte l'information d'erreur ou d'abscence de données sur la correction d'horloge ie "999999.%"
    et remplace cette valeur par la valeur "0.0"
    pour ainsi éviter une mauvaise interprétation de la correction de l'horloge.

    Parameters
    ----------
    data_of_one_sat : TYPE list of lists
        DESCRIPTION. list des positions, correction horloge, exposants deviations position et horloge d'un satellite'

    Returns
    -------
    '''
    for data_of_one_time in data_of_sats:
        for l in data_of_one_time:
            if '999999.' in l[4] :
                l[4] = '0.0'
    
        

def deviation_horloge(data,data_of_sats):
    '''
    Cette fonction remplace les exposants des déviations de la correction d'horloge par les valeurs de déviations en picosecondes.

    Parameters
    ----------
    data : TYPE list of str
        DESCRIPTION. fichier brute d'ephemerides'
    data_of_one_sat : TYPE list of lists
        DESCRIPTION. list des positions, correction horloge, deviations position et exposant déviation de correction horloge d'un satellite'

    Returns
    -------
    new_coord : TYPE
        DESCRIPTION.

    '''
    
    new_coord = copy.deepcopy(data_of_sats)
    #extraction du base floating point number
    lign15 = organiser_ligne(data[14])
    number = float(lign15[2])
    
    #extraction of the three-digit exponents representing the standard deviation for the clock correction in units of picosecondes
    for i in range(len(data_of_sats)):
        for k in range(len(data_of_sats[i])):
            if len(data_of_sats[i][k])>=9:  #vérifie si l'exposant est bien présent
                new_coord[i][k][8] = number ** int(data_of_sats[i][k][8])
        
    return new_coord



def prise_en_compte(data,data_of_one_sat):
    '''
    Cette fonction actualise les positions avec les déviations et indique les secondes
    de la semaine avec correction et déviation (en prenant en compte les 15min d'écart toutes les mesures)

    Parameters
    ----------
    data : TYPE list of str
        DESCRIPTION. fichier brute d'ephemerides'
    data_of_one_sat : TYPE list of lists
        DESCRIPTION. list des positions, correction horloge, deviations position et horloge d'un satellite'

    Returns
    -------
    new_data : TYPE
        DESCRIPTION.

    '''
    new_data = copy.deepcopy(data_of_one_sat)
    
    for k in range(len(new_data)):
        for i in range(len(new_data[k])):
            if len(new_data[k][i])>=5:
                
                new_data[k][i][4] = float(new_data[k][i][4])*10**(-6)
                new_data[k][i][4] += float(horaire_satellite(data)) #ajout seconde de la semaine
                new_data[k][i][4] += 15*60*k   #ajout de 15min ie 15*60 sec à chaque nouvelle mesure
                
                if 8<=len(new_data[k][i])>5:
                    new_data[k][i][1],new_data[k][i][2],new_data[k][i][3],new_data[k][i][5],new_data[k][i][6],new_data[k][i][7] = float(new_data[k][i][1]),float(new_data[k][i][2]),float(new_data[k][i][3]),float(new_data[k][i][5]),float(new_data[k][i][6]),float(new_data[k][i][7])
                    new_data[k][i][1] += new_data[k][i][5]*10**(-6)    #deviation X-coordinate
                    new_data[k][i][2] += new_data[k][i][6]*10**(-6)   #deviation Y-coordinate
                    new_data[k][i][3] += new_data[k][i][7]*10**(-6)    #deviation Z-coordinate
                    
                if len(new_data[k][i])>8:
                    new_data[k][i][8] = float(new_data[k][i][8])
                    new_data[k][i][4] += new_data[k][i][8]*10**(-12)   #deviation clock correction
    
    return new_data

def choix_horaire(data,horaire):
    """
    permet de choisir la position des satellites sur une plage horaire a partir d'une heure donnée

    Parameters
    ----------
    data : list
        donnée des position satellite.
    horaire : float
        heure donnée en seconde depuis le debu de la semaine GPS.

    Returns
    -------
    liste_heure : list
        coordonnées des satellites pour l'heure donnée.

    """
    liste_heure=[]
    
    heure_origine=345600.0
    interval=15*60
    plage_horaire=int((horaire-heure_origine)/interval)
    liste_heure.append(data[plage_horaire])
    liste_heure.append(data[plage_horaire+1])
    
    
    return liste_heure



def co_sat(heure):
    """
    traite le fichier d'entrée et renvoie les positions des satellites a l'heure demandé

    Parameters
    ----------
    heure : float
        heure donnée en seconde depuis le debu de la semaine GPS.

    Returns
    -------
    liste_heure : list
        coordonnées des satellites pour l'heure donnée.

    """
    
    #Choix du fichier
    
    fichier_ephemeride = choisir_fichier('igs20704.sp3')
    
    #Choix du satellite
    
    # nom_sat = choix_satellite(fichier_ephemeride)
    # print("\nVous avez choisi le satellite : ",nom_sat)
    
    #extraction des coordonnées du satellite choisi avec vérification d la correction d'horloge
    
    print("\nVoici ses coordonnées le "+date_gregorienne(fichier_ephemeride)+"à "+horaire_gregorien(fichier_ephemeride)+" \n")
    print("ou en semaine GPS : "+date_satellite(fichier_ephemeride)+" et secondes de cette semaine : "+horaire_satellite(fichier_ephemeride)+" : \n")
    coordonnees = coord_satellite(fichier_ephemeride)
    #['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','exponent-X-deviation','exponent-Y-deviation','exponent-Z-deviation','exponent-clock-deviation']
    print("Ces données sont contenues dans la variable 'coordonnees'. \n")
    print(coordonnees[0][0])
    
    #prise en compte de la déviation de position
    print("\nPrise en compte de la déviation de position ")
    coord_avec_devia_pos = deviation_position(fichier_ephemeride,coordonnees)
    #['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','X-deviation','Y-deviation','Z-deviation','exponent-clock-deviation']
    print(coord_avec_devia_pos[0][0])
    
    
    #prise en compte de la déviation d'horloge
    print("\nPrise en compte de la deviation de la correction d'horloge ")
    coord_avec_devia_pos_et_clock_corr = deviation_horloge(fichier_ephemeride,coord_avec_devia_pos)
    #['nom','X-coordinate','Y-coordinate','Z-coordinate,'correction-horloge','X-deviation','Y-deviation','Z-deviation','clock-deviation']
    print(coord_avec_devia_pos_et_clock_corr[0][0])
    
    #affichage de la position avec déviation et seconde de la semaine avec correction et déviation horloge
    print("\nPosition avec deviation et seconde de la semaine avec correction et déviation horloge ")
    coord_finales_et_secondeofweek = prise_en_compte(fichier_ephemeride, coord_avec_devia_pos_et_clock_corr)
    #['nom','X-coordinate','Y-coordinate','Z-coordinate,'seconde of week']
    print(coord_finales_et_secondeofweek[0][0])
    
    #choix de l'heure demandée
    liste_heure=choix_horaire(coord_finales_et_secondeofweek,heure)
    return(liste_heure)
    
    