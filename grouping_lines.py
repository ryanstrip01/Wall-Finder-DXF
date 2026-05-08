import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
from ezdxf.math import Vec3

# import shapely
# from shapely import STRtree
# from shapely.validation import explain_validity
# from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, mapping


from broken_lines import segmente_centru
from utils import UnitVector2D, TestColiniar



def familii_segmente_paralele():

    unitar  = []
    reg     = []

    unghi   = lambda s: UnitVector2D(s).unghi
    lungime = lambda s: UnitVector2D(s).magn

    unghi_curent = None


    for i in segmente_centru:
        unitar.append ((unghi(i), i , lungime(i)))


    unitar.sort(key = lambda x: (x[0],x[2]), reverse = True)

    lungimi = sorted([unitar[i][2] for i in range(len(unitar))])

    for u in range(len(unitar)):

        if unitar[u][0] != unghi_curent:
          unghi_curent = unitar[u][0]

          coor_lng = []
          coor_lng.append(unitar[u][1:])
          reg.append({
              'unghi':unghi_curent,
              'coord_lng': coor_lng
          })


        elif unitar[u][0] == unghi_curent:
            coor_lng.append(unitar[u][1:])

    return reg
   

registrum = familii_segmente_paralele()
# print(registrum)


def grupare():
    sgm_formare = []
    
    for index in range(len(registrum)):
        ungh_cur     = registrum[index]['unghi']
        lst          = registrum[index]['coord_lng']
        gasite = set()

        for i in range(len(lst)):
            sgm = []
            if lst[i][0] not in gasite:
                gasite.add(lst[i][0])
                sgm.append(lst[i][0])
            else:
                pass

            for j in range(len(lst)):
                if i != j and TestColiniar().test_coliniar(lst[i][0], lst[j][0], ungh_cur) and lst[j][0] not in gasite: 
                    gasite.add(lst[j][0])
                    sgm.append(lst[j][0])
                    
              
            sgm_formare.append(sgm)
            
    return sgm_formare
        

grupuri = grupare()

