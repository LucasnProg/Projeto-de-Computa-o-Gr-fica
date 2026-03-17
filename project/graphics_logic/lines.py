

def dda_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo DDA.
    """

    def custom_round(a):
        return int(a + 0.5)
    
    points = []

    dx = x2-x1
    dy = y2-y1

    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)

    if steps == 0:
        return 0.0, 0.0, [{"x": x1, "y": y1}]

    x_inc = dx / float(steps)
    y_inc = dy / float(steps)

    x = x1
    y = y1

    points.append({"x": custom_round(x), "y": custom_round(y)})

    for i in range(int(steps)):
        x += x_inc
        y += y_inc
        points.append({"x": custom_round(x), "y": custom_round(y)})
        
    return points, x_inc, y_inc


def bresenham_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo de Reta de Bresenham (Ponto Médio).
    Generalizado para todos os 8 octantes (múltiplas inclinações).
    """
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    points = []
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)

    # Calculo da direção de avanço para X e Y (+1 ou -1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    is_steep = dy > dx # Define a inclinação para ver onde incrementar a cada passo 

    if is_steep:
        dx, dy = dy, dx

    d_start = 2 * dy - dx
    inc_e = 2 * dy
    inc_ne = 2 * (dy - dx)
    
    x = x1
    y = y1
    d = d_start

    while (x != x2 or y != y2):
        points.append({"x": x, "y": y, "d": d})
        
        if d < 0:
            d += inc_e
            if is_steep:
                y += sy
            else:
                x += sx
        else:
            d += inc_ne
            x += sx
            y += sy

    points.append({"x": x, "y": y, "d": d})

    return points