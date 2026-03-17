
INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def check_outcode(x, y, xmin, ymin, xmax, ymax):
    """
    Calcula o código binário de cada ponto (x, y).
    Funcionamento:
    Compara as coordenadas do ponto com as fronteiras da janela (xmin, xmax, ymin, ymax).
    """
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code

def cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    """
    Implementação do Algoritmo de Cohen-Sutherland.
    """
    code1 = check_outcode(x1, y1, xmin, ymin, xmax, ymax)
    code2 = check_outcode(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        if code1 == 0 and code2 == 0: # Aceitação Trivial.
            accept = True
            break
        elif (code1 & code2) != 0: # Rejeição Trivial.
            break
        else: # Recorte
            x, y = 0.0, 0.0
            code_out = code1 if code1 != 0 else code2

            if code_out & TOP: # Interseção com o topo
                t = (ymax - y1)/(y2-y1)
                x = x1 + (t*(x2 - x1))
                y = ymax
            elif code_out & BOTTOM: # Interseção com o bottom
                t = (ymin - y1)/(y2-y1)
                x = x1 + (t*(x2 - x1)) 
                y = ymin
            elif code_out & RIGHT: # Interseção com a direita
                t = (xmax - x1) / (x2 - x1)
                y = y1 + (t * (y2 - y1))
                x = xmax
            elif code_out & LEFT: # Interseção com a esquerda
                t = (xmin - x1) / (x2 - x1)
                y = y1 + (t * (y2 - y1))
                x = xmin

            if code_out == code1:
                x1, y1 = round(x), round(y)
                code1 = check_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = round(x), round(y)
                code2 = check_outcode(x2, y2, xmin, ymin, xmax, ymax)

    if accept:
        return {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
    else:
        return None
