import ezdxf

doc = ezdxf.readfile(r'C:\Proiect_Automatizare\chestii_cad\MLP_Birou.dxf')
doc.layers.add(name = 'MLP_modificat', color = 11)
doc.layers.add(name = 'MLP_expand', color = 3)
doc.layers.add(name = 'triunghiuri')
doc.layers.add(name = 'poligon')
doc.layers.add(name = 'contur', color = 1)
doc.layers.add(name = 'segm_unire', color = 60)
spc = doc.modelspace()



