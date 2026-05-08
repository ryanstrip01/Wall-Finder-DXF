#Program care inveleste numele in linii 
import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
from ezdxf.math import Vec3


doc = ezdxf.readfile(r'C:\Proiect_Automatizare\chestii_cad\wrapper\name_wrapping1.dxf')
spc = doc.modelspace()


for e in spc.query('TEXT'):
    print(e.get_placement()[1])