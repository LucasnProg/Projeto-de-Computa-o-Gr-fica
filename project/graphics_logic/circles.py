"""
MÓDULO: RASTERIZAÇÃO DE CIRCUNFERÊNCIAS
---------------------------------------
Responsável por desenhar círculos utilizando simetria de 8 pontos.
Contém:
- Ponto Médio (Bresenham): Algoritmo otimizado com inteiros.
- Equação Explícita e Paramétrica: Métodos alternativos para comparação didática.

Utilizado por: Módulo 4 (Circunferências).
"""

import math

def mid_Point_circle(xc, yc, r):
    points = []
    x, y = 0, r
    p = 1 - r
    def plot(cx, cy, x, y):
        points.extend([
            {"x": cx+x, "y": cy+y}, {"x": cx-x, "y": cy+y},
            {"x": cx+x, "y": cy-y}, {"x": cx-x, "y": cy-y},
            {"x": cx+y, "y": cy+x}, {"x": cx-y, "y": cy+x},
            {"x": cx+y, "y": cy-x}, {"x": cx-y, "y": cy-x}
        ])
    plot(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0: p += 2*x + 1
        else:
            y -= 1
            p += 2*(x-y) + 1
        plot(xc, yc, x, y)
    return points

def explicit_circle(xc, yc, r):
    points = []
    for x_off in range(-r, r+1):
        y_sq = r**2 - x_off**2
        if y_sq >= 0:
            y_off = math.sqrt(y_sq)
            points.append({"x": xc+x_off, "y": round(yc+y_off)})
            points.append({"x": xc+x_off, "y": round(yc-y_off)})
    return points

def parametric_circle(xc, yc, r, steps=360):
    points = []
    for i in range(steps+1):
        theta = math.radians(i * 360/steps)
        points.append({
            "x": round(xc + r*math.cos(theta)),
            "y": round(yc + r*math.sin(theta))
        })
    return points