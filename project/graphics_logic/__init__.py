#Este arquivo reúne todas as funções para que o resto do projeto não quebre.
from .lines import dda_line, bresenham_line
from .circles import mid_Point_circle, explicit_circle, parametric_circle
from .ellipses import elipse_mid_point
from .transformations_2d import *
from .transformations_3d import *
from .recorte_suterland import (
    cohen_sutherland
)
from .recorte_poligono import (
    polygonClipSuthHodg
)
from .bezier import *

from .opengl_viewer import *