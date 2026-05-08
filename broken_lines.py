import math
from operator import itemgetter
from collections import defaultdict

import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
from ezdxf.math import Vec3


from triangulation import triunghiuri, segmente
from init_ezdxf import *
# from utils import unit_vector_2d


def selectare_triunghiuri(index): #(index, lista_triunghiuri <polilinii inchise, 4 vertexuri>)
  counter = 0
  verts = list(triunghiuri.geoms[index].boundary.coords)
  edges = [(verts[i],verts[i+1]) for i in range(len(verts) - 1)]
  #print(edges)

  e_pereti = []
  for e in edges:
    if e in segmente:
      counter += 1
      e_pereti.append(e)

#  if counter == 2:
#    #print('Triunghi Ureche')
#    #print(edges)
#    pass
#
#  if counter == 0:
#    #print('Triunghi Jonctiune')
#    #print(edges)
#    pass

  if counter == 1:
    #print("Triunghi Veriga")
    return edges, e_pereti[0]
  else:
    pass

triunghiuri_veriga = []
for t in range(len(triunghiuri.geoms)):
  if selectare_triunghiuri(t) is not None:
    triunghiuri_veriga.append(selectare_triunghiuri(t))



segmente_centru = []
def desen_linie_triunghi(index): #Deseneaza linia paralela cu segmentul
                                 #Referinta directa la triunghiuri_veriga
  trig, seg = triunghiuri_veriga[index]
  seg_mj = [m for m in trig if m != seg]

  mj = lambda x: ((x[0][0] + x[1][0])/2, (x[0][1] + x[1][1])/2)
  
  linie = (mj(seg_mj[0]),
           mj(seg_mj[1]))

  spc.add_line(linie[0], linie[1], dxfattribs={'layer':'contur'})
  return linie

for i in range(len(triunghiuri_veriga)):
  segmente_centru.append(desen_linie_triunghi(i))
  
  
  
  
  # print(desen_linie_triunghi(i))
  
#Adaugare xline
# print(segmente_centru[0])
# unit = unit_vector_2d(segmente_centru[0])
# spc.add_xline(segmente_centru[0][0], unit)
# print(unit)


  
# doc.saveas(r'C:\Proiect_Automatizare\chestii_cad\xline_test.dxf') 
