from shapely import validation
import math
from operator import itemgetter
from collections import defaultdict

import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
from ezdxf.math import Vec3

import shapely
from shapely import STRtree
from shapely.validation import explain_validity
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, mapping


doc = ezdxf.readfile("/content/drive/MyDrive/dxf/MLP_Birou.dxf")
doc.layers.add(name='MLP_modificat', color = 11)
doc.layers.add(name = 'MLP_expand', color = 3)
doc.layers.add(name = 'triunghiuri')
doc.layers.add(name = 'poligon')
doc.layers.add(name = 'contur', color = 1)
spc = doc.modelspace()



#segmente = list()
sgm_norm = list()

for e in spc.query('LINE'):
  p1 = Point(round(e.dxf.start.x,4) , round(e.dxf.start.y,4))
  p2 = Point(round(e.dxf.end.x,  4) , round(e.dxf.end.y,  4))

  p1nrm = (round(e.dxf.start.x,4) , round(e.dxf.start.y,4))
  p2nrm = (round(e.dxf.end.x,4) , round(e.dxf.end.y,4))

#  p1nrm = (e.dxf.start.x,   e.dxf.start.y)
#  p2nrm = (  e.dxf.end.x ,    e.dxf.end.y)


  sgm_norm.append((p1nrm,p2nrm))
  #segmente.append(LineString((p1,p2)))




###Triangulari n shi
ini = MultiLineString(sgm_norm)

#Transform segmentele in Shapely

v = ini.buffer(150, quad_segs = 0, cap_style = 'square', join_style='mitre')
#Buffer initial, pentru a abstractiza structura interna a peretilor si pentru
#a pastra doar granita externa

#v1 = MultiPolygon(
#                  (
#                    Polygon(mapping(v)['coordinates'][i][0]) for i in range(len(v.geoms))
#                  )
#              )


#Se pastreaza doar poligonul extern fara gauri ramase de la buffer

b = v.buffer(-150, quad_segs = 0, cap_style = 'square', join_style = 'mitre')
#Buffer negativ cu aceiasi valoare, boundary b are coordonatele utile pt proces


###Desen dupa buffer###




#for l in mapping(skeletron.ridges())['coordinates']:
#  spc.add_line(l[0],l[1])



triunghiuri = shapely.constrained_delaunay_triangles(b)
for n in triunghiuri.geoms:
  spc.add_lwpolyline(n.boundary.coords, dxfattribs={'layer':'triunghiuri'})
#Triangulare a poligoanelor bufferite (b)

skeletons = []


segmente = set()
def creare_Segmente():
  seg = set()
  for polig in b.geoms:
    #skeletron = StraightSkeleton(polig)
    #skeletons.append(skeletron)

    #m = [mapping(polig)['coordinates'][i] for i in range(len(mapping(polig)['coordinates']))]
    mapping_ext = mapping(polig)['coordinates'][0]
    gauri = []
    if len(mapping(polig)['coordinates']) > 1:
      for c in range(1, len(mapping(polig)['coordinates'])):
        gauri = mapping(polig)['coordinates'][c]
    else:
      pass

    #spc.add_lwpolyline(m, dxfattribs={'layer':'poligon'})
    seg = seg | {(mapping_ext[i], mapping_ext[i+1]) for i in range(len(mapping_ext) - 1)} #aveam nevoie de segmente, nu de puncte
    seg = seg | {(gauri[i], gauri[i+1]) for i in range(len(gauri) - 1)}

  return seg

segmente = creare_Segmente()

###
#Selectare triunghiuri bune, adica veriga: triunghi care are o singura latura din poligon
###

#lista_triunghiuri <polilinii inchise, 4 vertexuri>



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



def familii_segmente_paralele():

  unitar   = []
  reg      = []

  unghi = lambda s: math.degrees(math.atan2(abs(s[1][1] - s[0][1]), abs(s[1][0] - s[0][0])))
  lungime = lambda s: math.dist(s[0],s[1])

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




def grupare_unire():
  sgm_formare = []
  sgm_noi     = []


  def test_coliniar(linie1, linie2, unghi_curent):
    if linie1[0] == linie2[1]:
      ungh = math.degrees(
          math.atan2(
              abs(linie1[0][1] - linie2[0][1]),
              abs(linie1[0][0] - linie2[0][0])
              )
          )
    elif linie1[0] != linie2[1]:
      ungh = math.degrees(
          math.atan2(
              abs(linie1[0][1] - linie2[1][1]),
              abs(linie1[0][0] - linie2[1][0])
              )
          )

    if unghi_curent == ungh and linie1 != linie2:
      return linie2
    else:
      pass


  def grupare(index):
    unghi_curent = registrum[index]['unghi']
    lst =          registrum[index]['coord_lng']
    gasite = set()


    for i in range(len(lst)):
      sgm = []
      if lst[i][0] not in gasite:
        gasite.add(lst[i][0])
        sgm.append(lst[i][0])
      else:
        pass

      for j in range(len(lst)):
        if i != j and test_coliniar(lst[i][0], lst[j][0], unghi_curent) and lst[j][0] not in gasite:
          gasite.add(lst[j][0])
          sgm.append(lst[j][0])

      if len(sgm) > 1:
        sgm_formare.append(sgm)


  for nr in range(len(registrum)):
    grupare(nr)


  def unire_segmente(index): #adauga segmente in sgm noi, trebuie bagate in R tree
    nr = 1
    gasite = set()
    cell = [LineString(i) for i in sgm_formare[index]]
    tree = STRtree(cell)


    print(f' {nr} atinge {tree.query(cell[nr], 'touches')}')
    print(f'nr = {cell[nr]}')
    print(f'apropiat = {cell[tree.query(cell[nr])[0]]}')

  return unire_segmente(7) #7 caz ciudat

  #Desen pzis
  #for i in range(len(sgm_noi)):
  #  spc.add_line(sgm_noi[i][0], sgm_noi[i][1], dxfattribs={'layer':'contur'})

  #return sgm_formare

segmente_de_fillet = grupare_unire()
#segmente_fill_shp = [LineString(i) for i in segmente_de_fillet]
#segmente_fill_shp = MultiLineString(segmente_de_fillet)



trafo = lambda x: (Vec2(x[0]),Vec2(x[1]))



segmente_de_fillet

#doc.saveas("/content/drive/MyDrive/dxf/mlp_linii_3.dxf")
