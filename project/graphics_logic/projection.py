"""
MÓDULO: VISUALIZAÇÃO E TRANSFORMAÇÕES 3D
----------------------------------------
Objetivo: Gerenciar operações matriciais 4x4 e projeções de objetos tridimensionais.
Baseado em Computer Graphics with OpenGL (Hearn & Baker).
"""
import math

def get_identity_4x4():
    """Retornar uma matriz identidade 4x4."""
    return [
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

def multiply_matrix_4x4(m1, m2):
    """Multiplicar duas matrizes 4x4 (m1 x m2)."""
    result = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def create_translation_3d(tx, ty, tz):
    """Criar matriz de Translação 3D."""
    mat = get_identity_4x4()
    mat[0][3] = tx
    mat[1][3] = ty
    mat[2][3] = tz
    return mat

def create_scale_3d(sx, sy, sz):
    """Criar matriz de Escala 3D."""
    mat = get_identity_4x4()
    mat[0][0] = sx
    mat[1][1] = sy
    mat[2][2] = sz
    return mat

def create_rotation_x(angle_deg):
    """Criar matriz de Rotação em torno do eixo X."""
    rad = math.radians(angle_deg)
    c, s = math.cos(rad), math.sin(rad)
    mat = get_identity_4x4()
    mat[1][1] = c
    mat[1][2] = -s
    mat[2][1] = s
    mat[2][2] = c
    return mat

def create_rotation_y(angle_deg):
    """Criar matriz de Rotação em torno do eixo Y."""
    rad = math.radians(angle_deg)
    c, s = math.cos(rad), math.sin(rad)
    mat = get_identity_4x4()
    mat[0][0] = c
    mat[0][2] = s
    mat[2][0] = -s
    mat[2][2] = c
    return mat

def create_rotation_z(angle_deg):
    """Criar matriz de Rotação em torno do eixo Z."""
    rad = math.radians(angle_deg)
    c, s = math.cos(rad), math.sin(rad)
    mat = get_identity_4x4()
    mat[0][0] = c
    mat[0][1] = -s
    mat[1][0] = s
    mat[1][1] = c
    return mat

def create_shear_3d(plane, a, b):
    """
    Criar matriz de Cisalhamento 3D.
    plane: 'Sh_xy' (z cisalhado por x,y), 'Sh_xz', 'Sh_yz'.
    """
    mat = get_identity_4x4()
    if plane == 'Sh_xy': # Z varia com X e Y (Shear Z)
        mat[0][2] = a 
        mat[1][2] = b
    elif plane == 'Sh_xz': # Y varia com X e Z (Shear Y)
        mat[0][1] = a 
        mat[2][1] = b
    elif plane == 'Sh_yz': # X varia com Y e Z (Shear X)
        mat[1][0] = a
        mat[2][0] = b
    return mat

def create_reflection_3d(plane):
    """Criar matriz de Reflexão 3D."""
    mat = get_identity_4x4()
    if plane == 'Rf_xy': # Espelha Z (inverte Z)
        mat[2][2] = -1
    elif plane == 'Rf_xz': # Espelha Y (inverte Y)
        mat[1][1] = -1
    elif plane == 'Rf_yz': # Espelha X (inverte X)
        mat[0][0] = -1
    return mat

def apply_matrix_to_points(points, matrix):
    """Aplicar matriz 4x4 a uma lista de vértices 3D."""
    new_points = []
    for p in points:
        x, y, z = p['x'], p['y'], p['z']
        # Multiplicação Matriz x Vetor Coluna [x, y, z, 1]
        nx = matrix[0][0]*x + matrix[0][1]*y + matrix[0][2]*z + matrix[0][3]*1
        ny = matrix[1][0]*x + matrix[1][1]*y + matrix[1][2]*z + matrix[1][3]*1
        nz = matrix[2][0]*x + matrix[2][1]*y + matrix[2][2]*z + matrix[2][3]*1
        # w seria calculado aqui se fosse projeção perspectiva completa, 
        # mas para transformações afins w=1.
        new_points.append({'x': nx, 'y': ny, 'z': nz})
    return new_points

def project_points_perspective(points, d=500):
    """
    Projetar pontos 3D para 2D usando perspectiva simples.
    Plano de projeção em z=0. Centro de projeção em (0,0,d).
    Fórmulas: xp = x * (d / (z+d)), yp = y * (d / (z+d))
    """
    projected = []
    for p in points:
        x, y, z = p['x'], p['y'], p['z']
        
        # Evitar divisão por zero se o ponto estiver no olho do observador
        if abs(z + d) < 1e-5: 
            factor = 1
        else:
            factor = d / (z + d)
        
        px = x * factor
        py = y * factor
        projected.append({'x': px, 'y': py})
    return projected