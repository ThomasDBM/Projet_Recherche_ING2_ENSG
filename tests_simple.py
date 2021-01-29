# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 09:44:03 2021

Test de la fonction Vue_du_ciel présente dans le script du même nom sur un cas simple

@author: thomas de Beaumont
"""



import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from mpl_toolkits.mplot3d import Axes3D

# #Script de création du petit MNS
# MNS=[[50,50,50,50,50,50,50,110,110,50,50],
#       [50,50,50,50,10,50,51,120,100,50,50],
#       [50,50,50,50,50,50,50,50,50,50,50],
#       [50,50,50,100,50,50,50,50,75,100,100],
#       [50,50,50,50,50,50,50,50,75,75,100],
#       [50,50,50,50,50,50,50,50,75,100,100],
#       [50,100,100,50,50,50,50,50,50,50,50],
#       [50,100,100,50,50,50,55,50,50,50,50],
#       [50,100,100,50,50,50,50,50,110,75,100],
#       [50,50,50,50,100,100,50,50,75,100,100],
#       [50,50,50,50,100,100,50,50,100,100,100]]

# MNSa=np.array(MNS)
# #plt.imshow(MNSa)

# image=img.fromarray(MNSa)

# image.save('mini_MNS.tiff')


MNS=plt.imread('mini_MNS.tiff')
taille_X = len(MNS)
taille_Y = len(MNS[0])
taille=(taille_X,taille_Y)
taille_pixel=1

#plt.imshow(MNS)


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


def Vue_du_ciel(MNS):
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
    listheta=ListeTheta(10)
    # print('listheta=',listheta)
    
    

    points_finaux_p=[]
    points_finaux_n=[]
        

        
    #detection du pixel le plus proche
    (icentre,jcentre)=(5,5)
        
    #on calcule la hauteur du point d'origine
    Hc=MNS[icentre][jcentre][0]
    # Hc=TS[k][3]
        
    # print('Hc via MNS: ',MNS[icentre][jcentre][0])

        
    #on parcourt tout les directions a partir du centre
    for theta in listheta:
            
        Vdir=[np.cos(theta),np.sin(theta)]
        Angle_max_p=0
        Angle_max_n=0
            
        #on parcourt la droite grace a un facteur d'agrandissement du vecteur unitaire
        for mu in range(1,11):
                
            #dans les positifs
            icalcp=int(icentre+mu*Vdir[0])
            jcalcp=int(jcentre+mu*Vdir[1])
            # print('----------------------\nmu=',mu)
            # print('thetha=',theta)
            # print('\nip,jp =',icalcp,',',jcalcp)
                
                
            #on verifie que l'on reste dans l'image
            if (icalcp>=0 and icalcp<taille[0]) and (jcalcp>=0 and jcalcp<taille[1]):
                    
                     #on calcule la hauteur du point calculé
                     Hp=MNS[icalcp][jcalcp][0]
                     # print('hp=',Hp)
                     
                     #on calcul l'angle d'elevation
                     angle_calc_p=np.arctan((Hp-Hc)/(mu*taille_pixel))
                     # print('angle p=',angle_calc_p*(360/np.pi))
                    
                     #on garde l'angle d'élévation maximum
                     if (angle_calc_p>=Angle_max_p) and (Hp>=Hc):
                        
                         Angle_max_p=angle_calc_p
                         # print('anglepfin=',Angle_max_p*(360/np.pi))
                         point_angle_max_p=(icalcp,jcalcp,Hp)
                    
                
                
            #dans les negatifs
            icalcn=int(icentre-mu*Vdir[0])
            jcalcn=int(jcentre-mu*Vdir[1])
            # print('\nin,jn =',icalcn,',',jcalcn)
        
                  #on verifie que l'on reste dans l'image
            if (icalcn>=0 and icalcn<taille[0]) and (jcalcn>=0 and jcalcn<taille[1]):
        
                    Hn=MNS[icalcn][jcalcn][0]
                    # print('hn=',Hn)
                      #on calcul l'angle d'elevation
                    angle_calc_n=np.arctan((Hn-Hc)/(mu*taille_pixel))
                    # print('angle n=',angle_calc_n*(360/np.pi))
                                         
                      #on garde l'angle d'élévation maximum
                    if (angle_calc_n>=Angle_max_n) and (Hn>=Hc):
                        
                          Angle_max_n=angle_calc_n
                          # print('anglenfin=',Angle_max_n*(360/np.pi))
                          point_angle_max_n=(icalcn,jcalcn,Hn)
            
            
          
        points_finaux_n.append(point_angle_max_n)
        points_finaux_p.append(point_angle_max_p)

    return(points_finaux_p+points_finaux_n)



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
        triangles.append((centre,points[i],points[i+1]))
    triangles.append((centre,points[-1],points[0]))
    return(triangles)
    
#calculs des points limitant la vue
Vue_point_1=Vue_du_ciel(MNS)
# print('\n',Vue_point_1)

#création des triangles
triangles=creation_triangles(Vue_point_1, (3,5,50))
# print(triangles)


#affichage graphique du résultat
X=[]
Y=[]
Z=[]    

for point in Vue_point_1:
    X.append(point[0])
    Y.append(point[1])
    Z.append(point[2])

fig1=plt.figure(1)
plt.imshow(MNS)
plt.scatter(5,3)
# plt.scatter(Y,X,color='r')

fig2=plt.figure(2)
ax = Axes3D(fig2)
ax.set_xlim(0,11)
ax.set_ylim(0,11)
ax.set_zlim(0, 150)
ax.view_init(0,45)

ax.scatter3D(3,5,50, c='r')
for triangle in triangles:
    trace = Poly3DCollection([triangle], alpha=0.5)
    ax.add_collection3d(trace)

ax.scatter3D(X,Y,Z, c='b')
    





