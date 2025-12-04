"""
MÓDULO: CURVAS PARAMÉTRICAS
---------------------------
Responsável pela geração de curvas suaves baseadas em pontos de controle.
Contém:
- Curvas de Bézier: Implementação utilizando polinômios de Bernstein.

Utilizado por: Módulo 13 (Curvas de Bézier).
"""

import math

def binomial_coeff(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

def bernstein_poly(n, i, t):
    return binomial_coeff(n, i) * (t ** i) * ((1 - t) ** (n - i))

def bezier_curve(control_points, num_points=100):
    n = len(control_points) - 1
    curve_points = []
    for i in range(num_points + 1):
        t = i / num_points
        x, y = 0, 0
        for k, p in enumerate(control_points):
            b = bernstein_poly(n, k, t)
            x += b * p["x"]
            y += b * p["y"]
        curve_points.append({"x": x, "y": y})
    return curve_points