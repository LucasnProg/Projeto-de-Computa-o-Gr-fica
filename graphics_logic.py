import math

# ===================================================================
# MÓDULO 3: RASTERIZAÇÃO DE RETAS
# Baseado no seu script para DDA e Ponto Médio (Bresenham).
# ===================================================================


def dda_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo DDA (Digital Differential Analyzer).
    Usa aritmética de ponto flutuante para calcular os incrementos.
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
    while (x <= x2):
        points.append({"x": round(x), "y": round(y)})
        x += x_inc
        y += y_inc
    return points, x_inc, y_inc


def bresenham_line(x1, y1, x2, y2):
    """
    Implementação do algoritmo de Reta de Bresenham (Ponto Médio).
    Usa apenas aritmética de inteiros, sendo altamente eficiente.
    """
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    points = []
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        points.append({"x": x1, "y": y1})
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    return points


# ===================================================================
# MÓDULO 4: RASTERIZAÇÃO DE CIRCUNFERÊNCIAS
# Baseado no seu script com os 3 métodos de desenho de círculo.
# ===================================================================


def bresenham_circle(xc, yc, r):
    """
    Implementação do algoritmo de Círculo de Bresenham (Ponto Médio).
    Usa aritmética de inteiros e simetria de 8 oitantes para máxima eficiência.
    """
    points = []
    x, y = 0, r
    p = 1 - r

    def plot_circle_points(cx, cy, x, y):
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

    plot_circle_points(xc, yc, x, y)
    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(xc, yc, x, y)
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


def parametric_circle(xc, yc, r):
    """
    Implementação via Equação Paramétrica (Trigonométrica).
    Usa seno e cosseno. Preciso, mas computacionalmente mais custoso.
    """
    points_dict = {}
    step = 0.1
    theta = 0
    while theta < 2 * math.pi:
        x = round(xc + r * math.cos(theta))
        y = round(yc + r * math.sin(theta))
        points_dict[f"{x},{y}"] = {"x": x, "y": y}
        theta += step
    return list(points_dict.values())


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
