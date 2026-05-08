import math
import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
from ezdxf.math import Vec3

from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, mapping



# v = ((80.0002, 605.0), (80.0002, 4197.5))



class TestColiniar:
    
    def __init__(self):
        pass
        
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
          return True
        else:
          return False


class AbsDistance:

    def __init__(self):
        pass
       
    def absdistance(points: list):
        dists = []
        for elm in points:
            dist = math.sqrt(elm[0]*elm[0] + elm[1]*elm[1])
            dists.append(dist)
        
        return dists
        
        
class Line:
    
    def __init__(self, tup):
        self.self    = tup
        self.p1 = tup[0]
        self.p2 = tup[1]
        self.p1vec2 = Vec2(tup[0])
        self.p2vec2 = Vec2(tup[1])
        self.selfvec2 = (self.p1vec2, self.p2vec2)
        self.shapelyline = LineString(self.self)
        
        self.__dx = self.p2vec2.x - self.p1vec2.x
        self.__dy = self.p2vec2.y - self.p1vec2.y
        self.__length = math.sqrt(self.__dx*self.__dx + self.__dy*self.__dy)
        self.dirvec = (self.__dx/self.__length, self.__dy/self.__length)
        self.angle = math.degrees(math.atan2(abs(self.dirvec[1]), abs(self.dirvec[0])))
        

# print(AbsDistance.absdistance(
                        # [(3328.7502, 1660.0)]
                                 # )
                                    # )
                                    
                                    
# print(Line(
            # ((7797.5002, 6007.5), (7797.5002, 2305.0)) 
             # ).dirvec
             # )