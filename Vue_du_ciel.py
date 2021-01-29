# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

fait par Thomas de Beaumont
"""

#importation des bibliothèques
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 


#ouverture des fichiers
MNS=plt.imread('MNS\MNE_18_fusionné.TIF')
WF_non_traite = open ("MNS\MNE_18_fusionné.TFW",'r')

trace_Stereopolis = open ("trajet_stereo.txt",'r')
"""
field 1 : date (s)
field 2 : X
field 3 : Y
field 4 : Z
field 5 : useless for the study
field 6 : useless for the study
field 7 : useless for the study
field 8 : useless for the study
"""


#definition des fonctions
def traitement_trace(trace):
    """
    traite le fichier en entrée pour pouvoir exploiter les données

    Parameters
    ----------
    trace : text file
        fichier text avec des informations pour chaque point 

    Returns
    -------
    None.

    """
    listpoints=[]
    points=trace.readlines()
    for p in points:
        psplit=p.split()
        
        psplit[0]=(float(psplit[0]))
        psplit[1]=(float(psplit[1]))
        psplit[2]=(float(psplit[2]))
        psplit[3]=(float(psplit[3]))
        
        listpoints.append(psplit)
        
    return(listpoints)
    
        
def PixelProche(X,Y,WF):
    """
    determine le pixel le plus proche des coordonées données en entré
    Parameters
    ----------
    X : float
        coordonée Est du point.
    Y : float
        coordonée Nord du point.
    WF : list
        informations du fichier de conversion du MNS.

    Returns
    -------
    Tuple
        coordonées I et J du pixel dans la matrice.

    """
    (Xp,Yp)=CartoToImg(X, Y, WF)
    return (int(Xp),int(Yp))
           
    

def CartoToImg(X,Y,WF):
    """
        met les coordonnées dans la projection cartographique en coordonnées des pixels 
    
        Parameters
        ----------
        X : integer
            coordonnée x du pixel dans la pojection
        Y : integer
            coordonnée y du pixel dans la projection
        WF : File
            fichier world contenant les parametre de transformation pour passer de l'image à la projection'
    
        Returns
        -------
        les coordonnées du pixel dans l'image
    
    """
    lignes= WF
        
    A=lignes[0]
    #B=lignes[2]
    C=lignes[4]
    #D=lignes[1]
    E=lignes[3]
    F=lignes[5]
        
    "A modifier si B et D != 0"
        
    Xp=(X-C)/A
    Yp=(Y-F)/E        
        
    return((Xp,Yp))



def ImgToCarto(X,Y,WF):
    """
    met les coordonnées des pixels en coordonnées dans la projection cartographique 

    Parameters
    ----------
    X : integer
        coordonnée x du pixel dans l'image
    Y : integer
        coordonnée y du pixel dans l'image
    WF : File
        fichier world contenant les parametre de transformation pour passer de l'image a la projection'

    Returns
    -------
    les coordonnées du pixel dans la projection carto

    """
    lignes=WF
    
    Xcarto= X*float(lignes[0]) + Y*float(lignes[2]) + float(lignes[4])
    Ycarto= X*float(lignes[1]) + Y*float(lignes[3]) + float(lignes[5])
        
    return((Xcarto,Ycarto))

def ListeTheta(n0):
    """
    calcul un nombre N0 d'angles égalements espacés entre -pi/2 et pi/2

    Parameters
    ----------
    n0 : integer
        Nombre d'angle contenus dans la discrétisation

    Returns
    -------
    une liste d'angles

    """
    list_centre=[-np.pi/2]
    
    for i in range(n0):
        
        thetai=-(np.pi/2)+((i*np.pi)/n0)
        thetaiplusun=-(np.pi/2)+(((i+1)*np.pi)/n0)
        
        list_centre.append((thetai+thetaiplusun)/2)
        
    return(list_centre)


def Vue_du_ciel(TS,MNS,WF):
    """
    calcul la surface de vue du ciel pour chaque points de la trace GNSS

    Parameters
    ----------
    T : List
        trace GNSS
    MNS : list
        Image en niveaux de gris de l'evolution du sol
    WF : list
        fichier world contenant les parametre de transformation pour passer de l'image a la projection'

    Returns
    -------
    None.

    """
    #création de la discrétisation des angles
    listheta=ListeTheta(100)

    
    #pour chaques points GNSS de la trace d véhicule stéréopolis
    for k in range(len(TS)):  #len(TS)
        
        #listes des résultats du calcul
        points_finaux_p=[]
        points_finaux_n=[]
        
        #recupération des coordonnées du point
        Xcentre=TS[k][1]
        Ycentre=TS[k][2]
        
        #le point central est placé en premier dans la liste des resultats
        pointsf=[(Xcentre,Ycentre,TS[k][3])]
        
        #detection du pixel le plus proche du centre
        (jcentre,icentre)=PixelProche(Xcentre,Ycentre,WF)
        
        #on calcule la hauteur du point d'origine
        Hc=max(MNS[icentre][jcentre][0],TS[k][3])  #on décide de choisir la hauteur donnée par la trace GNSS sauf si celle ci est plus basse que la hauteur du pixel centrale
        
        # print('Hc via MNS: ',MNS[icentre][jcentre][0])
        # print('HC via trace GPS: ',TS[k][3])
        
        
        #on parcourt tout les directions a partir du centre
        for theta in listheta:
            """
            pour chaque vecteur de direction (unitaire) on a un facteur d'agrandissement mu
            et on choisit le pixel le plus proche du point d'origine auquel on ajoute le vecteur :
            mu*Vdir
            on fait varier mu pour parcourir tout l'axe
            """
            
            Vdir=[np.cos(theta),np.sin(theta)]
            
            #initialisation des angles calculés
            Angle_max_p=0
            Angle_max_n=0
            
            #on parcourt la droite grace a un facteur d'agrandissement du vecteur unitaire
            for mu in range(100):
                
               #dans les positifs
                 icalcp=int(icentre+mu*Vdir[0])
                 jcalcp=int(jcentre+mu*Vdir[1])
                
                
                 #on verifie que l'on reste dans l'image
                 if (icalcp>=0 and icalcp<taille[0]) and (jcalcp>=0 and jcalcp<taille[1]):
                    
                     #on calcule la hauteur du point calculé
                     Hp=MNS[icalcp][jcalcp][0]
                     
                     #on calcul l'angle d'elevation
                     angle_calc_p=np.arctan((Hp-Hc)/(mu*taille_pixel))
                    
                     #on garde l'angle d'élévation maximum
                     if (angle_calc_p>=Angle_max_p)and(Hp>=Hc):
                        
                         Angle_max_p=angle_calc_p #l'angle max deviens celui qui viens d'être calculé
                         
                         #on enregistre les coordonées du point correspondant
                         point_angle_max_p=(ImgToCarto(jcalcp,icalcp,WF)[0],ImgToCarto(jcalcp,icalcp,WF)[1],Hp)
                
                
                #dans les negatifs
                 icalcn=int(icentre-mu*Vdir[0])
                 jcalcn=int(jcentre-mu*Vdir[1])
        
                  #on verifie que l'on reste dans l'image
                 if (icalcn>=0 and icalcn<taille[0]) and (jcalcn>=0 and jcalcn<taille[1]):
        
                    Hn=MNS[icalcn][jcalcn][0]
                      #on calcul l'angle d'elevation
                    angle_calc_n=np.arctan((Hn-Hc)/(mu*taille_pixel))
                                         
                      #on garde l'angle d'élévation maximum
                    if (angle_calc_n>=Angle_max_n)and(Hn>=Hc):
                        
                          Angle_max_n=angle_calc_n #l'angle max deviens celui qui viens d'être calculé
                          
                          #on enregistre les coordonées du point correspondant
                          point_angle_max_n=(ImgToCarto(jcalcn,icalcn,WF)[0],ImgToCarto(jcalcn,icalcn,WF)[1],Hn)
            
            
            #après avoir parcouru toute la droite, on enregistre le point qui a l'angle le plus élevé
            points_finaux_n.append(point_angle_max_n)
            points_finaux_p.append(point_angle_max_p)

        #on ajoute tous les points dans la liste finale
        pointsf+=points_finaux_p+points_finaux_n
        
        #enregistrement du résultat dans un fichier que l'on repère avec l'heure de mesure
        df = pd.DataFrame(pointsf) 
        df.to_csv('Resultat\Limite_vue_du_ciel_'+str(TS[k][0])+'.csv', index=False) 
        
    # #on retourne les points pour un affichage dans python (valable que si on lance le calcul avec un seul point)
    # return pointsf
        
        



if __name__ == "__main__":
    # execute only if run as a script
    
    #initialisation et prétraitement du fichier world associé au MNS
    lignesSDL= WF_non_traite.readlines()
    WF=[]
    for ligne in lignesSDL:
        WF.append(float(ligne.strip()))
        
        
    #variables globale
    taille_pixel=WF[0]
    taille_X = len(MNS)
    taille_Y = len(MNS[0])
    taille=(taille_X,taille_Y)
    TS=traitement_trace(trace_Stereopolis) #Traitement de la trace GNSS du véhicule stéréopolis
  
    #fermeture des fichiers
    WF_non_traite.close()
    trace_Stereopolis.close()
    
    # print("taille: ",taille)
    # print("WF" , WF)
    
    
    
    MNS_array=np.array(MNS)
    #plt.imshow(MNS)
    
    #on lance le calcul
    Vue_point_1=Vue_du_ciel(TS,MNS,WF)
    
    
    # #affichage du résultat avec python pour le premier point
    # #utile en phase de test
    # X=[]
    # Y=[]
    
    # for point in Vue_point_1:
    #     X.append(point[0])
    #     Y.append(point[1])
        
    # print("X=",TS[0][1])
    # print("Y=",TS[0][2])
    
    # print(Vue_point_1)
    # df = pd.DataFrame(Vue_point_1) 
    # df.to_csv('list_1.csv', index=False) 

    # plt.figure(1)

    # plt.scatter(X,Y,color='b')
    # plt.scatter(TS[0][1],TS[0][2],color='r')
    # plt.xlim(min(X)-1,max(X)+1)
    # plt.ylim(min(Y)-1,max(Y)+1)
    
    



