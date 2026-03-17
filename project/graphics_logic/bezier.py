# u --> Parâmetro da Curva, variando de 0 a 1. 
# COEFS --> Coeficientes binomiais, representa o polinômio de Bernstein calculando

import math

N_POINTS = 1000

def calc_coeficiente_binomial(n):
    """
    Calcula os coeficientes binomiais COEFS(n, k) = n! / (k! * (n - k)!)
    """
    COEFS = []
    for k in range(n + 1):
        COEFS.append(math.comb(n, k)) 
    return COEFS

def compute_bez_pt(u, points, COEFS):
    """
    Calcula um único ponto (x, y) na curva de Bézier para um dado 'u' (entre 0 e 1).
    """
    n_points = len(points)
    n = n_points - 1
    
    x, y = 0.0, 0.0
    
    for k in range(n_points):
        bez_blend_fcn = COEFS[k] * math.pow(u, k) * math.pow(1.0 - u, n - k)
        x += points[k]['x'] * bez_blend_fcn
        y += points[k]['y'] * bez_blend_fcn
        
    return {'x': x, 'y': y}

def calculate_bezier_curve(points):
    """
    Gera a lista completa de pontos da curva.
    """
    n_points = len(points)
    COEFS = calc_coeficiente_binomial(n_points - 1) 
    
    curve_points = []
    
    for k in range(N_POINTS + 1):
        u = float(k) / float(N_POINTS)
        pt = compute_bez_pt(u, points, COEFS)
        curve_points.append(pt)
        
    return curve_points