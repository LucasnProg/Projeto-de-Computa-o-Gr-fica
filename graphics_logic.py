import math
import numpy as np

# ===================================================================
# MÓDULO 3: RASTERIZAÇÃO DE RETAS
# Baseado no seu script para DDA e Ponto Médio (Bresenham).
# ===================================================================


def dda_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo DDA (Digital Differential Analyzer).
    Seguindo a implementação do livro texto
    """
    points = []
    length = abs(x2 - x1)
    if abs(y2 - y1) > length:
        length = abs(y2 - y1)

    if length == 0:
        points.append({"x": round(x1), "y": round(y1)})
        return points

    x_inc = (x2 - x1) / length
    y_inc = (y2 - y1) / length

    x, y = x1, y1
    while x <= x2:
        points.append({"x": round(x), "y": round(y)})
        x += x_inc
        y += y_inc
    return points, x_inc, y_inc


def bresenham_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo de Reta de Bresenham (Ponto Médio).
    Seguindo a implementação do livro texto.
    """
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    p = 2 * (dy - dx)

    if x1 > x2:
        x = x2
        y = y2
        x2 = 0
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


# ===================================================================
# MÓDULO 4: RASTERIZAÇÃO DE CIRCUNFERÊNCIAS
# Baseado no seu script com os 3 métodos de desenho de círculo.
# ===================================================================


def mid_Point_circle(xc, yc, r):
    """
    Implementação do algoritmo de Círculo de Bresenham (Ponto Médio).
    Usa aritmética de inteiros e simetria de 8 oitantes conforme o livro texto.
    """
    points = []
    x, y = 0, r
    p = 1 - r

    def circle_points(cx, cy, x, y):
        points.extend(
            [
                {"x": cx + x, "y": cy + y},
                {"x": cx - x, "y": cy + y},
                {"x": cx + x, "y": cy - y},
                {"x": cx - x, "y": cy - y},
                {"x": cx + y, "y": cy + x},
                {"x": cx - y, "y": cy + x},
                {"x": cx + y, "y": cy - x},
                {"x": cx - y, "y": cy - x},
            ]
        )

    circle_points(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        circle_points(xc, yc, x, y)
    return points


def explicit_circle(xc, yc, r):
    """
    Implementação via Equação Explícita (y = sqrt(r² - x²)).
    Simples, mas ineficiente e gera falhas nos pólos verticais.
    """
    points_dict = {}
    for x_offset in range(-r, r + 1):
        x = xc + x_offset
        y_offset_sq = r**2 - x_offset**2
        if y_offset_sq >= 0:
            y_offset = math.sqrt(y_offset_sq)
            y1, y2 = round(yc + y_offset), round(yc - y_offset)
            x_rounded = round(x)
            points_dict[f"{x_rounded},{y1}"] = {"x": x_rounded, "y": y1}
            points_dict[f"{x_rounded},{y2}"] = {"x": x_rounded, "y": y2}
    return list(points_dict.values())


def parametric_circle(xc, yc, r, steps=360):
    """
    Implementação via Equação Paramétrica (Trigonométrica).
    Usa seno e cosseno. Preciso, mas computacionalmente mais custoso.
    """
    points = []

    def circle_points(cx, cy, x, y):
        points.extend(
            [
                {"x": cx + x, "y": cy + y},
                {"x": cx - x, "y": cy + y},
                {"x": cx + x, "y": cy - y},
                {"x": cx - x, "y": cy - y},
                {"x": cx + y, "y": cy + x},
                {"x": cx - y, "y": cy + x},
                {"x": cx + y, "y": cy - x},
                {"x": cx - y, "y": cy - x},
            ]
        )

    for i in range(steps // 8 + 1):
        theta = (math.pi / 4) * i / (steps // 8)
        x = int(round(r * math.cos(theta)))
        y = int(round(r * math.sin(theta)))
        circle_points(xc, yc, x, y)

    return points


def elipse_mid_point(xc, yc, rx, ry):
    """
    Implementação do algoritmo Midpoint para Elipses,
    com a saída formatada como uma lista de dicionários.
    """
    pontos = set()

    def round(a):
        return int(a + 0.5)

    def elipse_points(x, y):
        # Adiciona os 4 pontos simétricos ao conjunto
        pontos.add((xc + x, yc + y))
        pontos.add((xc - x, yc + y))
        pontos.add((xc + x, yc - y))
        pontos.add((xc - x, yc - y))

    # --- Inicialização ---
    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2

    x = 0
    y = ry
    px = 0
    py = two_rx2 * y

    elipse_points(x, y)

    # --- Região 1 ---
    p = round(ry2 - (rx2 * ry) + (0.25 * rx2))

    while px < py:
        x += 1
        px += two_ry2
        if p < 0:
            p += ry2 + px
        else:
            y -= 1
            py -= two_rx2
            p += ry2 + px - py
        elipse_points(x, y)

    # --- Região 2 ---
    p = round(ry2 * (x + 0.5) * (x + 0.5) + rx2 * (y - 1) * (y - 1) - rx2 * ry2)

    while y > 0:
        y -= 1
        py -= two_rx2
        if p > 0:
            p += rx2 - py
        else:
            x += 1
            px += two_ry2
            p += rx2 - py + px
        elipse_points(x, y)

    all_points = [{"x": px, "y": py} for px, py in sorted(list(pontos))]

    return all_points


# ===================================================================
# MÓDULOS 5 e 2: TRANSFORMAÇÕES 2D E SISTEMAS DE COORDENADAS
# Baseado nos seus scripts de transformações e conversões de coordenadas.
# ===================================================================

# --- Lógica de Matrizes ---


def multiply_matrices(m1, m2):
    """Multiplica duas matrizes 3x3."""
    result = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += m1[i][k] * m2[k][j]
    return result


def apply_transform(points, matrix):
    """Aplica uma matriz de transformação a uma lista de pontos."""
    new_points = []
    for p in points:
        px, py = p["x"], p["y"]
        new_x = matrix[0][0] * px + matrix[0][1] * py + matrix[0][2] * 1
        new_y = matrix[1][0] * px + matrix[1][1] * py + matrix[1][2] * 1
        new_points.append({"x": new_x, "y": new_y})
    return new_points


# --- Funções para Criar Matrizes de Transformação ---


def create_translation_matrix(tx, ty):
    """Cria a matriz de Translação."""
    return [[1, 0, tx], [0, 1, ty], [0, 0, 1]]


def create_scale_matrix(sx, sy, cx, cy):
    """Cria a matriz de Escala em torno de um pivô (cx, cy)."""
    # Sequência: Translada para a origem, aplica a escala, translada de volta.
    t1 = create_translation_matrix(-cx, -cy)
    s = [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]
    t2 = create_translation_matrix(cx, cy)
    return multiply_matrices(t2, multiply_matrices(s, t1))


def create_rotation_matrix(angle_degrees, cx, cy):
    """Cria a matriz de Rotação em torno de um pivô (cx, cy)."""
    rad = math.radians(angle_degrees)
    cos_a, sin_a = math.cos(rad), math.sin(rad)
    # Sequência: Translada para a origem, aplica a rotação, translada de volta.
    t1 = create_translation_matrix(-cx, -cy)
    r = [[cos_a, -sin_a, 0], [sin_a, cos_a, 0], [0, 0, 1]]
    t2 = create_translation_matrix(cx, cy)
    return multiply_matrices(t2, multiply_matrices(r, t1))


def create_reflection_matrix(reflect_x, reflect_y):
    """Cria a matriz de Reflexão.
    - reflect_x=True reflete em torno do eixo Y (inverte X).
    - reflect_y=True reflete em torno do eixo X (inverte Y).
    """
    sx = -1 if reflect_y else 1  # Reflexão em Y inverte o sinal de X
    sy = -1 if reflect_x else 1  # Reflexão em X inverte o sinal de Y
    return [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]


def create_shear_matrix(shx, shy):
    """Cria a matriz de Cisalhamento."""
    return [[1, shx, 0], [shy, 1, 0], [0, 0, 1]]


# --- Funções de Conversão de Coordenadas ---
# Baseado nas fórmulas do seu script 'Sistemas de Coordenadas'


def dc_to_ndc(x_dc, y_dc, width, height):
    """Converte Coordenadas de Dispositivo (DC) para NDC (0 a 1)."""
    ndc_x = x_dc / float(width)
    ndc_y = y_dc / float(height)
    return ndc_x, ndc_y


def ndc_to_wc(ndc_x, ndc_y, x_max, x_min, y_max, y_min):
    """Converte Coordenadas NDC (0 a 1) para Coordenadas de Mundo (WC)."""
    wc_x = ndc_x * (x_max - x_min) + x_min
    wc_y = ndc_y * (y_max - y_min) + y_min
    return wc_x, wc_y


def wc_to_ndc(wc_x, wc_y, x_max, x_min, y_max, y_min):
    """Converte Coordenadas de Mundo (WC) de volta para NDC (0 a 1)."""
    ndc_x = (wc_x - x_min) / (x_max - x_min)
    ndc_y = (wc_y - y_min) / (y_max - y_min)
    return ndc_x, ndc_y


# ===================================================================
# MÓDULO 7: RECORTE DE LINHA 2D (COHEN-SUTHERLAND)
# ===================================================================

# Bit 4: Esquerda
# Bit 3: Direita
# Bit 2: Abaixo
# Bit 1: Acima
_INSIDE = 0b0000
_LEFT = 0b0001
_RIGHT = 0b0010
_BOTTOM = 0b0100
_TOP = 0b1000


def _compute_outcode(x, y, xmin, ymin, xmax, ymax):
    """Calcula o auto-código (outcode) de 4 bits para um ponto (x,y)[cite: 258]."""
    code = _INSIDE
    if x < xmin:
        code |= _LEFT
    elif x > xmax:
        code |= _RIGHT
    if y < ymin:
        code |= _BOTTOM
    elif y > ymax:
        code |= _TOP
    return code


def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    """
    Recorta uma linha (x1,y1)-(x2,y2) contra uma janela de recorte retangular.
    Implementa o algoritmo de Cohen-Sutherland [cite: 280-290].
    """
    code1 = _compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    code2 = _compute_outcode(x2, y2, xmin, ymin, xmax, ymax)
    accepted = False

    while True:
        if (code1 | code2) == 0:
            accepted = True
            break

        elif (code1 & code2) != 0:
            break

        else:
            code_out = code1 if code1 != 0 else code2

            x, y = 0.0, 0.0
            if code_out & _TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif code_out & _BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif code_out & _RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif code_out & _LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if code_out == code1:
                x1, y1 = x, y
                code1 = _compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                code2 = _compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

    if accepted:
        return [round(x1), round(y1), round(x2), round(y2)]
    else:
        return None


# ... (todo o seu código existente, incluindo cohen_sutherland_clip) ...

# ===================================================================
# MÓDULO 8: RECORTE DE POLÍGONO (SUTHERLAND-HODGMAN)
# Implementação baseada no Capítulo 7 de "Computer Graphics with OpenGL"
# (1).pdf]
# ===================================================================

# Constantes para as bordas da janela
_CLIP_LEFT = 0
_CLIP_RIGHT = 1
_CLIP_BOTTOM = 2
_CLIP_TOP = 3


def _intersect(p1, p2, edge_type, clip_value):
    """
    Calcula o ponto de interseção de uma aresta (p1, p2) com uma
    linha de recorte infinita (baseado na equação paramétrica da reta).
    """
    dx = p2["x"] - p1["x"]
    dy = p2["y"] - p1["y"]

    # Interseção com bordas verticais (Esquerda ou Direita)
    if edge_type == _CLIP_LEFT or edge_type == _CLIP_RIGHT:
        # Evita divisão por zero se a linha for vertical
        if dx == 0:
            return {"x": clip_value, "y": p1["y"]}  # Retorna um ponto na borda

        m = dy / dx  # Coeficiente angular
        x = clip_value
        y = p1["y"] + m * (x - p1["x"])
        return {"x": x, "y": y}

    # Interseção com bordas horizontais (Topo ou Fundo)
    elif edge_type == _CLIP_TOP or edge_type == _CLIP_BOTTOM:
        # Evita divisão por zero se a linha for horizontal
        if dy == 0:
            return {"x": p1["x"], "y": clip_value}  # Retorna um ponto na borda

        m_inv = dx / dy  # Inverso do coeficiente angular
        y = clip_value
        x = p1["x"] + m_inv * (y - p1["y"])
        return {"x": x, "y": y}


def _is_inside(p, edge_type, clip_window):
    """
    Verifica se um ponto 'p' está "dentro" de uma borda de recorte específica.
    """
    xmin, ymin = clip_window["xmin"], clip_window["ymin"]
    xmax, ymax = clip_window["xmax"], clip_window["ymax"]

    if edge_type == _CLIP_LEFT:
        return p["x"] >= xmin
    elif edge_type == _CLIP_RIGHT:
        return p["x"] <= xmax
    elif edge_type == _CLIP_BOTTOM:
        return p["y"] >= ymin
    elif edge_type == _CLIP_TOP:
        return p["y"] <= ymax
    return False


def sutherland_hodgman_clip(subject_polygon, clip_window):
    """
    Recorta um polígono (subject_polygon) contra uma janela de recorte
    retangular convexa (clip_window) usando o algoritmo de Sutherland-Hodgman.

    Args:
        subject_polygon (list): Lista de dicionários [{'x': x, 'y': y}, ...]
        clip_window (dict): Dicionário {'xmin': x, 'ymin': y, 'xmax': x, 'ymax': y}

    Returns:
        list: A lista de vértices do novo polígono recortado.
    """

    # (1).pdf]
    # O algoritmo processa o polígono contra cada uma das 4 bordas
    # da janela de recorte sequencialmente.

    clip_boundaries = [
        (_CLIP_LEFT, clip_window["xmin"]),
        (_CLIP_RIGHT, clip_window["xmax"]),
        (_CLIP_BOTTOM, clip_window["ymin"]),
        (_CLIP_TOP, clip_window["ymax"]),
    ]

    output_list = list(subject_polygon)  # Começa com o polígono original

    # Itera sobre cada uma das 4 bordas de recorte (esquerda, direita, fundo, topo)
    for edge_type, clip_value in clip_boundaries:

        input_list = list(output_list)  # Saída da etapa anterior é a entrada desta
        output_list.clear()

        if not input_list:
            break

        # Itera sobre cada aresta (p1 -> p2) do polígono de entrada
        for i in range(len(input_list)):
            p1 = input_list[i]
            p2 = input_list[
                (i + 1) % len(input_list)
            ]  # Próximo ponto (com wrap-around)

            p1_inside = _is_inside(p1, edge_type, clip_window)
            p2_inside = _is_inside(p2, edge_type, clip_window)

            # Caso 1: Ambos os pontos estão dentro. Adiciona p2.
            if p1_inside and p2_inside:
                output_list.append(p2)

            # Caso 2: Ponto p1 dentro, p2 fora. Adiciona a interseção.
            elif p1_inside and not p2_inside:
                intersection = _intersect(p1, p2, edge_type, clip_value)
                if intersection:
                    output_list.append(intersection)

            # Caso 3: Ponto p1 fora, p2 dentro. Adiciona interseção e p2.
            elif not p1_inside and p2_inside:
                intersection = _intersect(p1, p2, edge_type, clip_value)
                if intersection:
                    output_list.append(intersection)
                output_list.append(p2)

            # Caso 4: Ambos os pontos estão fora. Não adiciona nada.
            elif not p1_inside and not p2_inside:
                pass

    return output_list


# ===================================================================
# MÓDULO 9: RECORTE DE POLÍGONO (WEILER-ATHERTON)
# Implementação completa baseada no Capítulo 7 de
# "Computer Graphics with OpenGL"
# (1).pdf]
# ===================================================================
import sys

# Constante pequena para lidar com erros de ponto flutuante
_EPSILON = 1e-9  # Usar um valor um pouco maior que o epsilon da máquina

# --- Classes de Ajuda para Weiler-Atherton ---


class _Point:
    """Classe simples para representar um ponto."""

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __eq__(self, other):
        """Verifica se dois pontos são 'quase' iguais."""
        if not isinstance(other, _Point):
            return False
        return abs(self.x - other.x) < _EPSILON and abs(self.y - other.y) < _EPSILON

    def __repr__(self):
        return f"P({self.x:.1f}, {self.y:.1f})"

    def to_dict(self):
        """Converte de volta para o formato de dicionário do seu projeto."""
        return {"x": self.x, "y": self.y}


class _IntersectionPoint(_Point):
    """Classe especial para um ponto que é uma interseção."""

    def __init__(self, x, y, t_subject, t_clip, subject_edge_idx, clip_edge_idx):
        super().__init__(x, y)
        self.is_intersection = True
        self.is_entering = False  # Será definido na fase de classificação
        self.visited = False  # Atributo que faltava no _Point
        self.t_subject = t_subject  # Distância paramétrica na aresta do "subject"
        self.t_clip = t_clip  # Distância paramétrica na aresta do "clip"
        self.subject_edge_index = subject_edge_idx  # Índice da aresta do "subject"
        self.clip_edge_index = clip_edge_idx  # Índice da aresta do "clip"
        self.subject_link = None  # Link para o nó correspondente na lista do "clip"
        self.clip_link = None  # Link para o nó correspondente na lista do "subject"

    def __repr__(self):
        status = "Entering" if self.is_entering else "Leaving"
        return f"I({self.x:.1f}, {self.y:.1f} - {status})"


# --- Funções Auxiliares de Geometria (Sem alteração) ---


def _get_line_intersection(s1, s2, c1, c2):
    """
    Encontra a interseção entre duas arestas de linha (S1-S2) e (C1-C2).
    Retorna (t_subject, t_clip, x, y) ou None.
    """
    denom = (c2.y - c1.y) * (s2.x - s1.x) - (c2.x - c1.x) * (s2.y - s1.y)

    if abs(denom) < _EPSILON:
        return None

    ua_num = (c2.x - c1.x) * (s1.y - c1.y) - (c2.y - c1.y) * (s1.x - c1.x)
    ub_num = (s2.x - s1.x) * (s1.y - c1.y) - (s2.y - s1.y) * (s1.x - c1.x)

    t_subject = ua_num / denom
    t_clip = ub_num / denom

    if (
        t_subject > -_EPSILON
        and t_subject < 1 + _EPSILON
        and t_clip > -_EPSILON
        and t_clip < 1 + _EPSILON
    ):

        x = s1.x + t_subject * (s2.x - s1.x)
        y = s1.y + t_subject * (s2.y - s1.y)

        return t_subject, t_clip, x, y

    return None


def _is_point_inside_polygon(point, polygon):
    """
    Verifica se um ponto está dentro de um polígono (Ray Casting).
    """
    x, y = point.x, point.y
    inside = False

    p1 = polygon[-1]
    for i in range(len(polygon)):
        p2 = polygon[i]

        if (p1.y > y) != (p2.y > y):
            intersect_x = (p2.x - p1.x) * (y - p1.y) / (p2.y - p1.y) + p1.x
            if x < intersect_x:
                inside = not inside

        p1 = p2

    return inside


# --- Implementação Principal do Weiler-Atherton (Corrigida) ---


def weiler_atherton_clip(subject_polygon_dict, clip_polygon_dict):
    """
    Implementação completa do algoritmo Weiler-Atherton.
    Recorta um polígono "subject" contra um polígono "clip".

    (1).pdf]
    """

    # --- 1. Conversão e Validação ---
    if (
        not subject_polygon_dict
        or len(subject_polygon_dict) < 3
        or not clip_polygon_dict
        or len(clip_polygon_dict) < 3
    ):
        return []

    subject_polygon = [_Point(v["x"], v["y"]) for v in subject_polygon_dict]
    clip_polygon = [_Point(v["x"], v["y"]) for v in clip_polygon_dict]

    # --- 2. Fase 1: Encontrar TODAS as Interseções ---
    all_intersections = []

    for i in range(len(subject_polygon)):
        s1 = subject_polygon[i]
        s2 = subject_polygon[(i + 1) % len(subject_polygon)]

        for j in range(len(clip_polygon)):
            c1 = clip_polygon[j]
            c2 = clip_polygon[(j + 1) % len(clip_polygon)]

            intersection_data = _get_line_intersection(s1, s2, c1, c2)

            if intersection_data:
                t_subject, t_clip, x, y = intersection_data

                new_point = _IntersectionPoint(x, y, t_subject, t_clip, i, j)
                if new_point not in all_intersections:
                    all_intersections.append(new_point)

    if not all_intersections:
        # --- Caso Especial: Sem Interseções ---
        if _is_point_inside_polygon(subject_polygon[0], clip_polygon):
            return [subject_polygon_dict]  # Subject está dentro
        elif _is_point_inside_polygon(clip_polygon[0], subject_polygon):
            return [clip_polygon_dict]  # Clip está dentro (interseção)
        else:
            return []  # Polígonos disjuntos

    # --- 3. Fase 2: Construir as Listas Completas ---

    def build_full_list(polygon, edge_prop, t_prop):
        full_list = []
        for i in range(len(polygon)):
            full_list.append(polygon[i])

            intersections_on_this_edge = [
                p for p in all_intersections if getattr(p, edge_prop) == i
            ]

            intersections_on_this_edge.sort(key=lambda p: getattr(p, t_prop))
            full_list.extend(intersections_on_this_edge)
        return full_list

    subject_list = build_full_list(subject_polygon, "subject_edge_index", "t_subject")
    clip_list = build_full_list(clip_polygon, "clip_edge_index", "t_clip")

    # --- 4. Fase 3: Classificar Interseções (Entering / Leaving) ---
    is_subject_inside = _is_point_inside_polygon(subject_polygon[0], clip_polygon)

    for point in subject_list:
        if isinstance(point, _IntersectionPoint):
            point.is_entering = not is_subject_inside
            is_subject_inside = not is_subject_inside

    # --- 5. Fase 4: Linkar Interseções ---
    for s_point in subject_list:
        if isinstance(s_point, _IntersectionPoint):
            for c_point in clip_list:
                if s_point is c_point:  # 'is' verifica a identidade do objeto
                    s_point.clip_link = c_point
                    c_point.subject_link = s_point
                    break

    # --- 6. Fase 5: Traçar os Polígonos Resultantes (LÓGICA CORRIGIDA) ---
    output_polygons = []

    entering_points = [p for p in all_intersections if p.is_entering]

    for start_point in entering_points:

        # A verificação 'visited' só se aplica a pontos de interseção
        if start_point.visited:
            continue

        current_polygon = []
        current_list = subject_list
        current_point = start_point

        while True:  # Loop até voltarmos ao início

            # --- INÍCIO DA CORREÇÃO DO BUG ---
            # Apenas pontos de INTERSEÇÃO são marcados/verificados como 'visited'
            if isinstance(current_point, _IntersectionPoint):
                if current_point.visited:
                    # Se voltamos a um ponto de interseção visitado,
                    # só pode ser o ponto inicial.
                    if current_point == start_point:
                        break  # Fechamos o polígono
                    else:
                        # Erro: entramos em um ciclo já visitado
                        # print("Erro: Ciclo visitado detectado.")
                        break
                current_point.visited = True

            current_polygon.append(current_point.to_dict())
            # --- FIM DA CORREÇÃO DO BUG ---

            # Encontra o próximo ponto na lista atual
            try:
                idx = current_list.index(current_point)
            except ValueError:
                print(f"Erro fatal: Ponto {current_point} não encontrado na lista.")
                break

            next_point = current_list[(idx + 1) % len(current_list)]

            # Se o próximo ponto for uma interseção, trocamos de lista
            while isinstance(next_point, _IntersectionPoint):
                current_point = next_point

                # Verificamos ANTES de adicionar
                if current_point.visited:
                    if current_point == start_point:
                        break  # Fechamos o polígono
                    else:
                        # print("Erro: Ciclo interno detectado.")
                        break

                current_point.visited = True
                current_polygon.append(current_point.to_dict())

                # Troca de lista
                if current_list is subject_list:
                    current_list = clip_list
                    current_point = (
                        current_point.clip_link
                    )  # Pula para a lista do "clip"
                else:
                    current_list = subject_list
                    current_point = (
                        current_point.subject_link
                    )  # Pula para a lista do "subject"

                if current_point is None:
                    # O bug anterior (links nulos) causaria isso
                    print("Erro fatal: Link nulo encontrado!")
                    break

                idx = current_list.index(current_point)
                next_point = current_list[(idx + 1) % len(current_list)]

            if current_point is None:
                break

            # Se chegamos aqui, 'next_point' é um _Point normal
            current_point = next_point

            # Se voltamos ao início, fechamos o polígono
            if current_point == start_point:
                break

        if current_polygon:
            output_polygons.append(current_polygon)

    return output_polygons


# ===================================================================
# MÓDULO 10 & 11: LÓGICA DE VISUALIZAÇÃO 3D E PIPELINE 2D
# Baseado nos Capítulos 7, 8, e 9 de "Computer Graphics with OpenGL"
# (1).pdf]
# ===================================================================


def map_window_to_viewport(xw, yw, window, viewport):
    """
    Mapeia um ponto (xw, yw) da Janela do Mundo (Window) para a
    Porta de Visão (Viewport).
    """
    # (1).pdf]
    # Extrai os limites da Janela (World)
    xw_min, yw_min = window["xmin"], window["ymin"]
    xw_max, yw_max = window["xmax"], window["ymax"]

    # Extrai os limites da Viewport (Device/Screen)
    xv_min, yv_min = viewport["vx_min"], viewport["vy_min"]
    xv_max, yv_max = viewport["vx_max"], viewport["vy_max"]

    # Calcula os fatores de escala
    sx = (xv_max - xv_min) / (xw_max - xw_min)
    sy = (yv_max - yv_min) / (yw_max - yw_min)

    # Calcula as coordenadas finais da Viewport
    xv = xv_min + (xw - xw_min) * sx
    yv = yv_min + (yw - yw_min) * sy

    return {"x": xv, "y": yv}


# --- Lógica de Matriz 4x4 (Cap. 8) ---


def create_identity_4x4():
    """Cria uma matriz identidade 4x4."""
    return np.identity(4)


def multiply_matrices_4x4(m1, m2):
    """Multiplica duas matrizes 4x4 (M2 * M1)."""
    return np.dot(m2, m1)


def create_composite_matrix_4x4(transforms):
    """
    Cria uma matriz de transformação 4x4 composta a partir de uma lista
    de transformações (ex: ['T(10,5,0)', 'Rx(45)', ...]).
    """
    matrix = create_identity_4x4()

    # (1).pdf]
    # Composição de matrizes (M_nova * M_antiga)
    for t in transforms:
        op = t.split("(")[0]
        params_str = t[len(op) + 1 : -1]  # Pega o conteúdo entre parênteses

        m_new = create_identity_4x4()

        try:
            params = [float(p) for p in params_str.split(",")] if params_str else []
        except ValueError:
            print(f"Aviso: Parâmetros inválidos para {t}")
            continue

        if op == "T" and len(params) == 3:
            m_new = create_translation_matrix_3d(*params)
        elif op == "S" and len(params) == 3:
            m_new = create_scale_matrix_3d(*params)
        elif op == "Rx" and len(params) == 1:
            m_new = create_rotation_matrix_3d_x(*params)
        elif op == "Ry" and len(params) == 1:
            m_new = create_rotation_matrix_3d_y(*params)
        elif op == "Rz" and len(params) == 1:
            m_new = create_rotation_matrix_3d_z(*params)

        # --- NOVAS TRANSFORMAÇÕES ---
        elif op == "Sh_xy" and len(params) == 2:
            m_new = create_shear_matrix_3d_xy(*params)
        elif op == "Sh_xz" and len(params) == 2:
            m_new = create_shear_matrix_3d_xz(*params)
        elif op == "Sh_yz" and len(params) == 2:
            m_new = create_shear_matrix_3d_yz(*params)
        elif op == "Rf_xy" and len(params) == 0:
            m_new = create_reflection_matrix_3d_xy()
        elif op == "Rf_xz" and len(params) == 0:
            m_new = create_reflection_matrix_3d_xz()
        elif op == "Rf_yz" and len(params) == 0:
            m_new = create_reflection_matrix_3d_yz()
        # --- FIM DAS NOVAS TRANSFORMAÇÕES ---

        matrix = multiply_matrices_4x4(matrix, m_new)

    return matrix


# --- Funções de Transformação 3D (Cap. 8) ---


def create_translation_matrix_3d(tx, ty, tz):
    """Cria a matriz de Translação 3D."""
    return np.array([[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]])


def create_scale_matrix_3d(sx, sy, sz):
    """Cria a matriz de Escala 3D."""
    return np.array([[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]])


def create_rotation_matrix_3d_x(angle_degrees):
    """Cria a matriz de Rotação 3D em torno do eixo X."""
    rad = math.radians(angle_degrees)
    c, s = math.cos(rad), math.sin(rad)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0], [0, s, c, 0], [0, 0, 0, 1]])


def create_rotation_matrix_3d_y(angle_degrees):
    """Cria a matriz de Rotação 3D em torno do eixo Y."""
    rad = math.radians(angle_degrees)
    c, s = math.cos(rad), math.sin(rad)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0], [-s, 0, c, 0], [0, 0, 0, 1]])


def create_rotation_matrix_3d_z(angle_degrees):
    """Cria a matriz de Rotação 3D em torno do eixo Z."""
    rad = math.radians(angle_degrees)
    c, s = math.cos(rad), math.sin(rad)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


# --- Funções de Projeção 3D (Cap. 9) ---


def create_shear_matrix_3d_xy(shx, shy):
    """Matriz de Cisalhamento no plano XY (em relação a Z)"""
    # (1).pdf]
    return np.array([[1, 0, shx, 0], [0, 1, shy, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def create_shear_matrix_3d_xz(shx, shz):
    """Matriz de Cisalhamento no plano XZ (em relação a Y)"""
    # (1).pdf]
    return np.array([[1, shx, 0, 0], [0, 1, 0, 0], [0, shz, 1, 0], [0, 0, 0, 1]])


def create_shear_matrix_3d_yz(shy, shz):
    """Matriz de Cisalhamento no plano YZ (em relação a X)"""
    # (1).pdf]
    return np.array([[1, 0, 0, 0], [shy, 1, 0, 0], [shz, 0, 1, 0], [0, 0, 0, 1]])


def create_reflection_matrix_3d_xy():
    """Matriz de Reflexão sobre o plano XY (inverte Z)"""
    # (1).pdf]
    return np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])


def create_reflection_matrix_3d_xz():
    """Matriz de Reflexão sobre o plano XZ (inverte Y)"""
    # (1).pdf]
    return np.array([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def create_reflection_matrix_3d_yz():
    """Matriz de Reflexão sobre o plano YZ (inverte X)"""
    # (1).pdf]
    return np.array([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])


def create_isometric_projection_matrix():
    """
    Cria uma matriz de projeção paralela isométrica.
    Isso é feito compondo duas rotações (em Y, depois em X)
    seguidas de uma projeção ortográfica simples (descartando Z).
    """
    # (1).pdf]
    # Rotação em Y de 45 graus
    angle_y = 45
    rad_y = math.radians(angle_y)
    cos_y, sin_y = math.cos(rad_y), math.sin(rad_y)
    M_rot_y = np.array(
        [[cos_y, 0, sin_y, 0], [0, 1, 0, 0], [-sin_y, 0, cos_y, 0], [0, 0, 0, 1]]
    )

    # Rotação em X de 35.264 graus
    angle_x = 35.264
    rad_x = math.radians(angle_x)
    cos_x, sin_x = math.cos(rad_x), math.sin(rad_x)
    M_rot_x = np.array(
        [[1, 0, 0, 0], [0, cos_x, -sin_x, 0], [0, sin_x, cos_x, 0], [0, 0, 0, 1]]
    )

    # Matriz de projeção ortográfica (simplesmente descarta Z)
    M_ortho = np.array(
        [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]  # Z é zerado
    )

    # A matriz isométrica é M_ortho * M_rot_x * M_rot_y
    M_iso = multiply_matrices_4x4(M_rot_y, M_rot_x)
    M_iso = multiply_matrices_4x4(M_iso, M_ortho)
    return M_iso


# --- Função Principal de Renderização 3D ---


def apply_3d_transform_and_project(vertices, transforms):
    """
    Aplica uma lista de transformações 3D a uma lista de vértices
    e, em seguida, aplica a projeção isométrica.

    Retorna uma lista de pontos 2D projetados.
    """
    # 1. Cria a matriz de transformação composta (Model-View)
    M_model = create_composite_matrix_4x4(transforms)

    # 2. Cria a matriz de projeção
    M_proj = create_isometric_projection_matrix()

    # 3. Cria a matriz final (M_proj * M_model)
    M_final = multiply_matrices_4x4(M_model, M_proj)

    projected_points = []

    for v in vertices:
        # Converte o vértice para coordenada homogênea 4D
        v_hom = np.array([v["x"], v["y"], v["z"], 1.0])

        # Aplica a transformação e projeção
        v_proj_hom = np.dot(M_final, v_hom)

        # Converte de volta de homogêneo (embora seja projeção paralela,
        # 'w' deve ser 1, mas é uma boa prática)
        if v_proj_hom[3] != 0 and v_proj_hom[3] != 1:
            x = v_proj_hom[0] / v_proj_hom[3]
            y = v_proj_hom[1] / v_proj_hom[3]
        else:
            x = v_proj_hom[0]
            y = v_proj_hom[1]

        projected_points.append({"x": x, "y": y})

    return projected_points


# ===================================================================
# MÓDULO 13: CURVAS DE BÉZIER CÚBICAS
# Baseado no Capítulo 13, Seção 8 de "Computer Graphics with OpenGL"
# (1).pdf]
# ===================================================================

def _bezier_blending_0(u):
    """ Função de Mistura (Bernstein) BEZ_0,3(u) = (1-u)^3 """
    # (1).pdf]
    return (1 - u) ** 3

def _bezier_blending_1(u):
    """ Função de Mistura (Bernstein) BEZ_1,3(u) = 3u(1-u)^2 """
    # (1).pdf]
    return 3 * u * ((1 - u) ** 2)

def _bezier_blending_2(u):
    """ Função de Mistura (Bernstein) BEZ_2,3(u) = 3u^2(1-u) """
    # (1).pdf]
    return 3 * (u ** 2) * (1 - u)

def _bezier_blending_3(u):
    """ Função de Mistura (Bernstein) BEZ_3,3(u) = u^3 """
    # (1).pdf]
    return u ** 3

def calculate_bezier_cubic(p0, p1, p2, p3, steps=100):
    """
    Calcula os pontos de uma curva de Bézier cúbica usando 4 pontos de controle.
    
    Implementa a equação paramétrica:
    P(u) = (1-u)^3*P0 + 3u(1-u)^2*P1 + 3u^2(1-u)*P2 + u^3*P3
    
    (1).pdf]
    
    Args:
        p0, p1, p2, p3 (dict): Dicionários {'x': ..., 'y': ...}
        steps (int): Número de segmentos para aproximar a curva.
        
    Returns:
        list: Uma lista de pontos {'x': ..., 'y': ...} que formam a curva.
    """
    points = []
    
    for i in range(steps + 1):
        # u é o parâmetro que vai de 0.0 a 1.0
        u = i / float(steps)
        
        # Obtém os pesos (funções de mistura de Bernstein)
        bez0 = _bezier_blending_0(u)
        bez1 = _bezier_blending_1(u)
        bez2 = _bezier_blending_2(u)
        bez3 = _bezier_blending_3(u)
        
        # Calcula o ponto (x, y) na curva para o 'u' atual
        # Pondera as coordenadas de cada ponto de controle
        x = bez0 * p0['x'] + bez1 * p1['x'] + bez2 * p2['x'] + bez3 * p3['x']
        y = bez0 * p0['y'] + bez1 * p1['y'] + bez2 * p2['y'] + bez3 * p3['y']
        
        points.append({'x': x, 'y': y})
        
    return points