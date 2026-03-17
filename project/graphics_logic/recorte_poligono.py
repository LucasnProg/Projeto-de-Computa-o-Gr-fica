LEFT, RIGHT, BOTTOM, TOP = 0, 1, 2, 3

def inside(p, b, wMin, wMax):
    """Verifica se o ponto p está do lado de 'dentro' da borda b."""
    if b == LEFT: return p['x'] >= wMin['x']
    if b == RIGHT: return p['x'] <= wMax['x']
    if b == BOTTOM: return p['y'] >= wMin['y']
    if b == TOP: return p['y'] <= wMax['y']
    return True

def cross(p1, p2, winEdge, wMin, wMax):
    """Verifica se a aresta p1-p2 cruza a borda winEdge."""
    return inside(p1, winEdge, wMin, wMax) != inside(p2, winEdge, wMin, wMax)

def intersect(p1, p2, winEdge, wMin, wMax):
    """Calcula a interseção da aresta p1-p2 com a borda winEdge."""
    iPt = {"x": 0.0, "y": 0.0}
    m = 0.0
    
    if p1['x'] != p2['x']:
        m = (p1['y'] - p2['y']) / (p1['x'] - p2['x'])

    if winEdge == LEFT:
        iPt['x'] = wMin['x']
        iPt['y'] = p2['y'] + (wMin['x'] - p2['x']) * m
    elif winEdge == RIGHT:
        iPt['x'] = wMax['x']
        iPt['y'] = p2['y'] + (wMax['x'] - p2['x']) * m
    elif winEdge == BOTTOM:
        iPt['y'] = wMin['y']
        if p1['x'] != p2['x']:
            iPt['x'] = p2['x'] + (wMin['y'] - p2['y']) / m
        else:
            iPt['x'] = p2['x']
    elif winEdge == TOP:
        iPt['y'] = wMax['y']
        if p1['x'] != p2['x']:
            iPt['x'] = p2['x'] + (wMax['y'] - p2['y']) / m
        else:
            iPt['x'] = p2['x']
            
    iPt['x'], iPt['y'] = round(iPt['x']), round(iPt['y'])
    return iPt

def clipPoint(p, winEdge, wMin, wMax, pOut, first, s):
    """Pipeline recursivo: processa um ponto contra uma borda e repassa para a próxima."""
    if first[winEdge] is None:
        first[winEdge] = p
    else:
        if cross(p, s[winEdge], winEdge, wMin, wMax):
            iPt = intersect(p, s[winEdge], winEdge, wMin, wMax)
            if winEdge < TOP:
                clipPoint(iPt, winEdge + 1, wMin, wMax, pOut, first, s)
            else:
                pOut.append(iPt)

    s[winEdge] = p

    if inside(p, winEdge, wMin, wMax):
        if winEdge < TOP:
            clipPoint(p, winEdge + 1, wMin, wMax, pOut, first, s)
        else:
            pOut.append(p)

def closeClip(wMin, wMax, pOut, first, s):
    """Fecha o polígono testando o último ponto ('s') contra o 'first' de cada borda."""
    for winEdge in range(LEFT, TOP + 1):
        if s[winEdge] is not None and first[winEdge] is not None:
            if cross(s[winEdge], first[winEdge], winEdge, wMin, wMax):
                pt = intersect(s[winEdge], first[winEdge], winEdge, wMin, wMax)
                if winEdge < TOP:
                    clipPoint(pt, winEdge + 1, wMin, wMax, pOut, first, s)
                else:
                    pOut.append(pt)

def polygonClipSuthHodg(pIn, xmin, ymin, xmax, ymax):
    """
    Função Principal do Algoritmo de Sutherland-Hodgman.
    Recebe uma lista de vértices pIn e as coordenadas da janela.
    """

    wMin = {"x": xmin, "y": ymin}
    wMax = {"x": xmax, "y": ymax}
    
    pOut = []
    
    first = [None] * 4
    s = [None] * 4

    for p in pIn:
        clipPoint(p, LEFT, wMin, wMax, pOut, first, s)

    closeClip(wMin, wMax, pOut, first, s)
    
    return pOut