
import math

def projecao_paralela_isometrica(points):
    """
    Recebe os pontos 3D e aplica a projeção para desenho na tela.
    """
    cos_T_y = math.sqrt(2)/math.sqrt(3)
    cos_T_x = math.sqrt(2)/2

    sen_T_y = math.sqrt(1)/math.sqrt(3)
    sen_T_x = math.sqrt(2)/2

    matrix_projection = [
        [cos_T_y, (sen_T_y*sen_T_x), (sen_T_y*cos_T_x), 0],
        [0, cos_T_x, -sen_T_x, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 1]
    ]

    figure = point_to_matrix_3d(points)
    new_figure = multiply_matrices_3d(matrix_projection, figure)
    
    projected_points = []
    colunas = len(new_figure[0])
    for j in range(colunas):
        projected_points.append({
            "x": round(new_figure[0][j], 2), 
            "y": round(new_figure[1][j], 2)
        })
    return projected_points

def multiply_matrices_3d(m1, m2):
    """Multiplica matriz de transformação (4x4) pela matriz de vértices (4xN)"""
    linhas_m1 = len(m1)      
    colunas_m1 = len(m1[0])  
    colunas_m2 = len(m2[0])  

    result = [[0] * colunas_m2 for _ in range(linhas_m1)]
    
    for i in range(linhas_m1):
        for j in range(colunas_m2): 
            for k in range(colunas_m1):
                result[i][j] += m1[i][k] * m2[k][j]
    return result


def point_to_matrix_3d(points):
    """Converte lista de dicts em matriz de vértices 4xN (X, Y, Z, W)"""
    matrix = []
    lineX = []
    lineY = []
    lineZ = []
    lineW = []

    for p in points:
        lineX.append(p["x"])
        lineY.append(p["y"])
        lineZ.append(p["z"]) 
        lineW.append(1)

    matrix.append(lineX)
    matrix.append(lineY)
    matrix.append(lineZ)
    matrix.append(lineW)
    return matrix


def matrix_to_points_3d(matrix):
    """Converte a matriz transformada 4xN de volta para lista de dicts (3D)"""
    points = []
    colunas = len(matrix[0])
    
    for j in range(colunas):
        w = matrix[3][j]
        if w == 0: 
            w = 1 
            
        points.append({
            "x": round(matrix[0][j] / w, 2), 
            "y": round(matrix[1][j] / w, 2),
            "z": round(matrix[2][j] / w, 2)
        })
    return points

def scale_object_3d(points, sx, sy, sz):
    matrix_scale = [
        [sx, 0 , 0, 0],
        [0, sy, 0, 0],
        [0, 0 , sz, 0],
        [0, 0 , 0, 1]
    ]

    figure = point_to_matrix_3d(points)
    new_figure = multiply_matrices_3d(matrix_scale, figure)
    return matrix_to_points_3d(new_figure)

def tralade_object_3d(points, tx, ty, tz):
    matrix_translade = [
        [1, 0 , 0, tx],
        [0, 1, 0, ty],
        [0, 0 , 1, tz],
        [0, 0 , 0, 1]
    ]

    figure = point_to_matrix_3d(points)
    new_figure = multiply_matrices_3d(matrix_translade, figure)
    return matrix_to_points_3d(new_figure)

def rotate_object_3d(points, angle, axis):
    rad = math.radians(angle)
    cos, sen = math.cos(rad), math.sin(rad)

    if(axis == "x"):
        rotation_matrix = [
        [1, 0 , 0, 0],
        [0, cos, -sen, 0],
        [0, sen , cos, 0],
        [0, 0 , 0, 1]
        ]
    elif(axis == "z"):
        rotation_matrix = [
        [cos, -sen , 0, 0],
        [sen, cos, 0, 0],
        [0, 0 , 1, 0],
        [0, 0 , 0, 1]
        ]
    elif(axis == "y"):
        rotation_matrix = [
        [cos, 0 , sen, 0],
        [0, 1, 0, 0],
        [-sen, 0 , cos, 0],
        [0, 0 , 0, 1]
        ]
    

    figure = point_to_matrix_3d(points)
    new_figure = multiply_matrices_3d(rotation_matrix, figure)
    return matrix_to_points_3d(new_figure)

def reflect_object_3d(points, axis):

    
    if(axis == "xy"):
        reflection_matrix = [
        [1, 0 , 0, 0],
        [0, 1, 0, 0],
        [0, 0 , -1, 0],
        [0, 0 , 0, 1]
        ]
    elif(axis == "yz"):
        reflection_matrix = [
        [-1, 0 , 0, 0],
        [0, 1, 0, 0],
        [0, 0 , 1, 0],
        [0, 0 , 0, 1]
        ]
    elif(axis == "xz"):
        reflection_matrix = [
        [1, 0 , 0, 0],
        [0, -1, 0, 0],
        [0, 0 , 1, 0],
        [0, 0 , 0, 1]
        ]
    

    figure = point_to_matrix_3d(points)
    new_figure = multiply_matrices_3d(reflection_matrix, figure)
    return matrix_to_points_3d(new_figure)

def shear_object_3d(points, axis, sh1, sh2):
    a,b,c,d,e,f = 0,0,0,0,0,0
    
    if(axis == "x"):
        a = sh1
        b = sh2
    elif(axis == "y"):
        c = sh1
        d = sh2
    elif(axis == "z"):
        e = sh1
        f = sh2

    shear_matrix = [
        [1, c , e, 0],
        [a, 1, f, 0],
        [b, d , 1, 0],
        [0, 0 , 0, 1]
        ]
    

    figure = point_to_matrix_3d(points)
    new_figure = multiply_matrices_3d(shear_matrix, figure)

    return matrix_to_points_3d(new_figure)


