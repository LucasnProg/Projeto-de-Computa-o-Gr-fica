"""
MÓDULO: RASTERIZAÇÃO DE RETAS
-----------------------------
Responsável por converter definições matemáticas de retas em pixels discretos.
Contém:
- DDA (Digital Differential Analyzer): Algoritmo incremental usando float.
- Bresenham Generalizado: Algoritmo otimizado com inteiros para todos os octantes.

Utilizado por: Módulo 3 (Retas).
"""

def dda_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo DDA (Digital Differential Analyzer).
    """
    points = []
    
    # Determina o comprimento pelo maior delta
    length = abs(x2 - x1)
    if abs(y2 - y1) > length:
        length = abs(y2 - y1)

    if length == 0:
        points.append({"x": round(x1), "y": round(y1)})
        return points

    x_inc = (x2 - x1) / length
    y_inc = (y2 - y1) / length

    x, y = x1, y1
    
    # Gera os pontos incrementando passos
    # O loop roda 'length' vezes, convertendo float para inteiro
    i = 0
    while i <= length:
        points.append({"x": round(x), "y": round(y)})
        x += x_inc
        y += y_inc
        i += 1
        
    return points, x_inc, y_inc


def bresenham_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo de Reta de Bresenham (Ponto Médio).
    Versão original para o primeiro octante (|m| < 1).
    """
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    points = []
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    p = 2 * (dy - dx)

    # Se a reta for desenhada da direita para a esquerda, inverte os pontos
    if x1 > x2:
        x = x2
        y = y2
        x2 = x1
    else:
        x = x1
        y = y1

    while x <= x2:
        points.append({"x": x, "y": y})
        x += 1
        if p < 0:
            p += 2 * dy
        else:
            y += 1
            p += 2 * (dy - dx)

    return points