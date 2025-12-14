#R TREE VERSION
import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
import numpy as np
import math
from operator import itemgetter
from rtree import index


doc = ezdxf.readfile("/content/drive/MyDrive/Drawing1.dxf")
spc = doc.modelspace()
lines_ini = []
zero = Vec2(0,0)
latime_max_zid = 12.8


for e in spc.query("LINE"):
  p1 = Vec2(e.dxf.start.x, e.dxf.start.y)
  p2 = Vec2(e.dxf.end.x, e.dxf.end.y)
  m =  Vec2((e.dxf.start.x + e.dxf.end.x)/2 , (e.dxf.start.y + e.dxf.end.y)/2)
  v = (p1 - p2)/math.dist(p1,p2)

  n = Vec2(-v[1],v[0])
  lines_ini.append({
                "p1":p1,
                "p2":p2,
                "m":  m,
                "len":math.dist(p1,p2),
                "dir":v,
                "norm":n
                })

lines = sorted(lines_ini, key = itemgetter('len'), reverse = True)


Copac = index.Index()

#R Tree este creat
def adaugiri(count,pom):
  punct1 = lines[count]['p1']
  punct2 = lines[count]['p2']

  minx = min(punct1[0],punct2[0])
  maxx = max(punct1[0],punct2[0])
  miny = min(punct1[1],punct2[1])
  maxy = max(punct1[1],punct2[1])

  #return minx, maxx, miny,maxy

  pom.insert(count, (minx,miny,maxx,maxy))

for i in range(len(lines)):
  adaugiri(i,Copac)


#Se efectueaza cautarea celei mai potrivite linii pt perete
def cautare(count, pom, latime = latime_max_zid):
  a = []

  punct1 = lines[count]['p1']
  punct2 = lines[count]['p2']


  minx = min(punct1[0],punct2[0]) - latime
  maxx = max(punct1[0],punct2[0]) + latime
  miny = min(punct1[1],punct2[1]) - latime
  maxy = max(punct1[1],punct2[1]) + latime

  lol = pom.intersection((minx,miny,maxx,maxy), objects = True)

  for j in lol:
    #print(f"Debug Initial {j.id}")
    punct1 = lines[j.id]['p1']
    punct2 = lines[j.id]['p2']

    minxj = min(punct1[0],punct2[0])
    maxxj = max(punct1[0],punct2[0])
    minyj = min(punct1[1],punct2[1])
    maxyj = max(punct1[1],punct2[1])

    if count != j.id and minxj >= minx and maxxj <= maxx and minyj >= miny and maxyj <= maxy  :
      #print(f"Debug Final: OK {j.id}")
      a.append(j.id)

  return a


'''
def iter3():
  for i in range(len(lines)):
    rez = cautare(i,Copac)


    for j in  rez:
      print(j.id)
      if verif_grp2(i,j.id) and j.id != i:
        print("OK")
      else:
        print("NOT OK")
'''


#def test_nou(indx):
#  rez = cautare(indx,Copac)
#  for j in  rez:
#    print(j.id)
#    punct1 = lines[j.id]['p1']
#    punct2 = lines[j.id]['p2']
#
#    minx = min(punct1[0],punct2[0])
#    maxx = max(punct1[0],punct2[0])
#    miny = min(punct1[1],punct2[1])
#    maxy = max(punct1[1],punct2[1])
#
#    if



#Functie pentru gasirea numarului unei linii din DXF
def numerotare():
  for i in range(len(lines)):
    print(i)
    print(lines[i]['p1'])
    print(lines[i]['p2'])
    print(lines[i]['len'])


#Leaga liniile raw care formeaza un perete, apoi scoate punctele din ele, le sorteaza dupa modul, si le baga intr-un R-Tree
def imperechere(count, pom):
  peret = []
  puncte = []
  puncte_tree = index.Index()

  peret.append(lines[count])

  rez = cautare(count, pom)
  #Rez da o lista cu indexul liniei
  for i in range(len(rez)):
    peret.append(lines[rez[i]])


  for j in range(len(peret)):

      puncte.append({
          "p":peret[j]['p1'],
          "modul":abs(peret[j]['p1'])
          })

      puncte.append({
          "p":peret[j]['p2'],
          "modul":abs(peret[j]['p2'])
          })

  puncte_srt = sorted(puncte, key = itemgetter('modul'), reverse = "True")

  for l in range(len(puncte_srt)):
      minx = puncte_srt[l]['p'][0]
      maxx = puncte_srt[l]['p'][0]
      miny = puncte_srt[l]['p'][1]
      maxy = puncte_srt[l]['p'][1]

      puncte_tree.insert(l, (minx,miny,maxx,maxy))


  return peret, puncte_srt, puncte_tree

#def polig(count, pom):
#  peretp = []
#  lengts = []
#  rez = imperechere(count,Copac)
#  for k in range(len(rez)):
#    np.linalg.norm(rez[k]['p1'])
#    np.linalg.norm(rez[k]['p2'])
#


#Gruparea pe poligoane
def iter3():
  indx = set()
  ziduri = []


  for i in range (len(lines)):
    if i in indx:
      continue
    else:
      indx.add(i)
      peret,n,m = imperechere(i,Copac)
      rez = cautare(i,Copac)
      ziduri.append({
          "puncte":n,
          "tree":m
      })
      for k in range (len(rez)):
        indx.add(rez[k])


  #return indx
  return  ziduri


#print(iter3())


#b = cautare(16,Copac)
#
#print(b)
#
#cautare(16,Copac)

def desenat(count,pom = Copac):
  puncte_list,puncte_tree = iter3()[count]['puncte'], iter3()[count]['tree']
  minmaxmic = (
        puncte_list[0]['p'][0] - latime_max_zid,
        puncte_list[0]['p'][1] - latime_max_zid,
        puncte_list[0]['p'][0] + latime_max_zid,
        puncte_list[0]['p'][1] + latime_max_zid
  )

  minmaxmare = [
       puncte_list[-1]['p'][0] - latime_max_zid,
       puncte_list[-1]['p'][1] - latime_max_zid,
       puncte_list[-1]['p'][0] + latime_max_zid,
       puncte_list[-1]['p'][1] + latime_max_zid
  ]

  lmaomic = puncte_tree.intersection(minmaxmic, objects = True,)
  lmare = puncte_tree.intersection(minmaxmare, objects = True)

  return puncte_list





#desenat(2)
#iter3()[2]
#for i in range (len(iter3())):
#  #print(desenat(i))
#  spc.add_line(desenat(i)[0], desenat(i)[1], dxfattribs = {'color': 4})
#  #print(i)

#doc.saveas("/content/drive/MyDrive/proiect04.dxf")



desenat(2)









  
