"""
MÓDULO: TRANSFORMAÇÕES GEOMÉTRICAS 2D
-------------------------------------
Responsável pela manipulação matricial de objetos 2D.
Contém:
- Criação de matrizes 3x3 (Coordenadas Homogêneas): Translação, Escala, Rotação, Reflexão e Cisalhamento.
- Aplicação de transformações compostas (ex: Rotação em torno de pivô arbitrário).

Utilizado por: Módulo 5 (Transformações 2D) e Módulo 11 (Pipeline).
"""

import math

def multiply_matrices(m1, m2):
    result = [[0]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def apply_transform(points, matrix):
    new_points = []
    for p in points:
        px, py = p["x"], p["y"]
        nx = matrix[0][0]*px + matrix[0][1]*py + matrix[0][2]
        ny = matrix[1][0]*px + matrix[1][1]*py + matrix[1][2]
        new_points.append({"x": nx, "y": ny})
    return new_points

def create_translation_matrix(tx, ty):
    return [[1, 0, tx], [0, 1, ty], [0, 0, 1]]

def create_scale_matrix(sx, sy, cx=0, cy=0):
    t1 = create_translation_matrix(-cx, -cy)
    s = [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]
    t2 = create_translation_matrix(cx, cy)
    return multiply_matrices(t2, multiply_matrices(s, t1))

def create_rotation_matrix(angle, cx=0, cy=0):
    rad = math.radians(angle)
    c, s = math.cos(rad), math.sin(rad)
    t1 = create_translation_matrix(-cx, -cy)
    r = [[c, -s, 0], [s, c, 0], [0, 0, 1]]
    t2 = create_translation_matrix(cx, cy)
    return multiply_matrices(t2, multiply_matrices(r, t1))

def create_reflection_matrix(rx, ry):
    sx = -1 if ry else 1
    sy = -1 if rx else 1
    return [[sx, 0, 0], [0, sy, 0], [0, 0, 1]]

def create_shear_matrix(shx, shy):
    return [[1, shx, 0], [shy, 1, 0], [0, 0, 1]]