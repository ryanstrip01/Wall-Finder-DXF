import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
from ezdxf.math import Vec3

import shapely
from shapely import STRtree
# from shapely.validation import explain_validity
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, mapping

from init_ezdxf import *
from utils import Line

sgm_norm = list()

for e in spc.query('LINE'):
  p1 = Point(round(e.dxf.start.x,4) , round(e.dxf.start.y,4))
  p2 = Point(round(e.dxf.end.x,  4) , round(e.dxf.end.y,  4))

  p1nrm = (round(e.dxf.start.x,4) , round(e.dxf.start.y,4))
  p2nrm = (round(e.dxf.end.x,4)   , round(e.dxf.end.y,4))

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


triunghiuri = shapely.constrained_delaunay_triangles(b)
for n in triunghiuri.geoms:
  spc.add_lwpolyline(n.boundary.coords, dxfattribs={'layer':'triunghiuri'})
#Triangulare a poligoanelor bufferite (b)



def creare_Segmente(): 
#Segmentele pe granita externa a peretilor 
#care trebuie sa coincida cu triunghiurile pentru a gasi triunghi veriga
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
# print(segmente)
