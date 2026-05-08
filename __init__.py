# from shapely import validation
import math
from operator import itemgetter
from collections import defaultdict

import ezdxf
from ezdxf import math as mth
from ezdxf.math import Vec2
from ezdxf.math import Vec3

import shapely
from shapely import STRtree
# from shapely.validation import explain_validity
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, mapping


