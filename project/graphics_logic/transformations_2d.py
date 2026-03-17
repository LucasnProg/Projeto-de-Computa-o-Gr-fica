
import math

def multiply_matrices(m1, m2):
    """Multiplica matriz de transformação (3x3) pela matriz de vértices (3xN)"""
    linhas_m1 = len(m1)      
    colunas_m1 = len(m1[0])  
    colunas_m2 = len(m2[0])  

    result = [[0] * colunas_m2 for _ in range(linhas_m1)]
    
    for i in range(linhas_m1):
        for j in range(colunas_m2): 
            for k in range(colunas_m1):
                result[i][j] += m1[i][k] * m2[k][j]
    return result

def point_to_matrix(points):
    """Converte a lista de dicts para para a matriz transformada 3xN"""
    matrix = []
    lineX = []
    lineY = []
    lineW = []

    for p in points:
        lineX.append(p["x"])
        lineY.append(p["y"])
        lineW.append(1)

    matrix.append(lineX)
    matrix.append(lineY)
    matrix.append(lineW)
    return matrix

def matrix_to_points(matrix):
    """Converte a matriz transformada 3xN de volta para lista de dicts para o Frontend"""
    points = []
    colunas = len(matrix[0])
    
    for j in range(colunas):
        points.append({
            "x": round(matrix[0][j], 2), 
            "y": round(matrix[1][j], 2)  
        })
    return points

def scale_object(points, sx, sy):
    matrix_scale = [
        [sx, 0 , 0],
        [0, sy, 0],
        [0, 0 , 1]
    ]

    figure = point_to_matrix(points)
    new_figure = multiply_matrices(matrix_scale, figure)
    return matrix_to_points(new_figure)

def tralade_object(points, tx, ty):
    matrix_translade = [
        [1, 0 , tx],
        [0, 1, ty],
        [0, 0 , 1]
    ]

    figure = point_to_matrix(points)
    new_figure = multiply_matrices(matrix_translade, figure)
    return matrix_to_points(new_figure)

def rotate_object(points, angle):
    rad = math.radians(angle)
    cos, sen = math.cos(rad), math.sin(rad)

    matrix_rotation = [
        [cos, -sen , 0],
        [sen, cos, 0],
        [0, 0 , 1]
    ]

    figure = point_to_matrix(points)
    new_figure = multiply_matrices(matrix_rotation, figure)
    return matrix_to_points(new_figure)

def reflect_object(points, axis):
    if(axis == "x"):
        matrix_refletion = [
        [1, 0 , 0],
        [0, -1, 0],
        [0, 0 , 1]
        ]
    elif(axis == "y"):
        matrix_refletion = [
        [-1, 0 , 0],
        [0, 1, 0],
        [0, 0 , 1]
        ]
    elif(axis == "xy"):
        matrix_refletion = [
        [-1, 0 , 0],
        [0, -1, 0],
        [0, 0 , 1]
        ]
    

    figure = point_to_matrix(points)
    new_figure = multiply_matrices(matrix_refletion, figure)
    return matrix_to_points(new_figure)

def shear_object(points, shx, shy):
    matrix_shear = [
    [1, shx, 0],
    [shy, 1, 0],
    [0, 0 , 1]
    ]
    

    figure = point_to_matrix(points)
    new_figure = multiply_matrices(matrix_shear, figure)
    return matrix_to_points(new_figure)


