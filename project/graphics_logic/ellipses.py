"""
MÓDULO: RASTERIZAÇÃO DE ELIPSES
-------------------------------
Responsável por desenhar elipses dividindo a curva em duas regiões baseadas na inclinação.
Contém:
- Ponto Médio para Elipses: Algoritmo incremental que trata as regiões 1 e 2 separadamente.

Utilizado por: Módulo 6 (Elipses).
"""

def elipse_mid_point(xc, yc, rx, ry):
    points = set()
    def plot(x, y):
        points.add((xc+x, yc+y)); points.add((xc-x, yc+y))
        points.add((xc+x, yc-y)); points.add((xc-x, yc-y))
    
    rx2, ry2 = rx*rx, ry*ry
    two_rx2, two_ry2 = 2*rx2, 2*ry2
    x, y = 0, ry
    px, py = 0, two_rx2 * y
    plot(x, y)
    
    # Região 1
    p = round(ry2 - (rx2*ry) + (0.25*rx2))
    while px < py:
        x += 1
        px += two_ry2
        if p < 0: p += ry2 + px
        else:
            y -= 1
            py -= two_rx2
            p += ry2 + px - py
        plot(x, y)
        
    # Região 2
    p = round(ry2*(x+0.5)**2 + rx2*(y-1)**2 - rx2*ry2)
    while y > 0:
        y -= 1
        py -= two_rx2
        if p > 0: p += rx2 - py
        else:
            x += 1
            px += two_ry2
            p += rx2 - py + px
        plot(x, y)
        
    return [{"x": px, "y": py} for px, py in sorted(list(points))]