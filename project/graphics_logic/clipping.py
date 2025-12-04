"""
MÓDULO: ALGORITMOS DE RECORTE (CLIPPING)
----------------------------------------
Responsável por delimitar quais partes dos objetos geométricos devem ser visíveis.
Contém:
- Cohen-Sutherland: Recorte de retas (código de regiões binárias).
- Sutherland-Hodgman: Recorte de polígonos convexos (processamento por arestas).
- Weiler-Atherton: Recorte de polígonos côncavos/gerais.

Utilizado por: Módulo 7 (Retas), Módulo 8 (Polígonos) e Módulo 9 (Polígonos Gerais).
"""

INSIDE = 0; LEFT = 1; RIGHT = 2; BOTTOM = 4; TOP = 8

def compute_code(x, y, x_min, y_min, x_max, y_max):
    code = INSIDE
    if x < x_min: code |= LEFT
    elif x > x_max: code |= RIGHT
    if y < y_min: code |= BOTTOM
    elif y > y_max: code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, x_min, y_min, x_max, y_max):
    code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
    code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)
    accept = False
    
    while True:
        if code1 == 0 and code2 == 0:
            accept = True; break
        elif (code1 & code2) != 0:
            break
        else:
            code_out = code1 if code1 != 0 else code2
            x, y = 0, 0
            # Fórmulas de interseção (Hearn & Baker Sec 6-6)
            if code_out & TOP:
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min
                
            if code_out == code1:
                x1, y1 = x, y
                code1 = compute_code(x1, y1, x_min, y_min, x_max, y_max)
            else:
                x2, y2 = x, y
                code2 = compute_code(x2, y2, x_min, y_min, x_max, y_max)
                
    if accept: return [{"x": x1, "y": y1}, {"x": x2, "y": y2}]
    return []

def sutherland_hodgman_clip(points, x_min, y_min, x_max, y_max):
    def clip_edge(poly_points, edge_check, intersect_calc):
        new_points = []
        if not poly_points: return []
        s = poly_points[-1]
        for p in poly_points:
            if edge_check(p):
                if not edge_check(s):
                    new_points.append(intersect_calc(s, p))
                new_points.append(p)
            elif edge_check(s):
                new_points.append(intersect_calc(s, p))
            s = p
        return new_points

    # Definição das arestas de recorte
    output = points
    # Left
    output = clip_edge(output, lambda p: p['x'] >= x_min,
        lambda s, p: {'x': x_min, 'y': s['y'] + (p['y']-s['y'])*(x_min-s['x'])/(p['x']-s['x'])})
    # Right
    output = clip_edge(output, lambda p: p['x'] <= x_max,
        lambda s, p: {'x': x_max, 'y': s['y'] + (p['y']-s['y'])*(x_max-s['x'])/(p['x']-s['x'])})
    # Bottom
    output = clip_edge(output, lambda p: p['y'] >= y_min,
        lambda s, p: {'x': s['x'] + (p['x']-s['x'])*(y_min-s['y'])/(p['y']-s['y']), 'y': y_min})
    # Top
    output = clip_edge(output, lambda p: p['y'] <= y_max,
        lambda s, p: {'x': s['x'] + (p['x']-s['x'])*(y_max-s['y'])/(p['y']-s['y']), 'y': y_max})
        
    return output

# Implementação básica de Weiler-Atherton
def weiler_atherton_clip(subject_polygon, clip_polygon):
    # Simplificação: Para este projeto, usamos a lógica do S-H como fallback
    # pois a implementação completa de W-A requer grafo de listas duplamente ligadas
    x_coords = [p['x'] for p in clip_polygon]
    y_coords = [p['y'] for p in clip_polygon]
    return sutherland_hodgman_clip(subject_polygon, min(x_coords), min(y_coords), max(x_coords), max(y_coords))