from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

twod_bp = Blueprint(
    'mod_5_twod',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/twod/static'
)

@twod_bp.route('/twod')
def twod_page():
    return render_template('twod_index.html')

@twod_bp.route('/api/twod/transform', methods=['POST'])
def api_transform():
    data = request.json
    trans_type = data.get('type')
    points = data.get('points') 
    params = data.get('params')

    matrix = []

    # 1. TRANSLAÇÃO
    if trans_type == 'translate':
        tx = float(params['tx'])
        ty = float(params['ty'])
        matrix = lg.create_translation_matrix(tx, ty)

    # 2. ESCALA 
    elif trans_type == 'scale':
        sx = float(params['sx'])
        sy = float(params['sy'])
        # Pega o centro enviado pelo JS 
        cx = float(params.get('cx', 0))
        cy = float(params.get('cy', 0))
        matrix = lg.create_scale_matrix(sx, sy, cx, cy)

    # 3. ROTAÇÃO 
    elif trans_type == 'rotate':
        angle = float(params['angle'])
        # Pega o centro enviado pelo JS. 
        cx = float(params.get('cx', 0))
        cy = float(params.get('cy', 0))
        matrix = lg.create_rotation_matrix(angle, cx, cy)

    # 4. REFLEXÃO
    elif trans_type == 'reflection':
        reflect_x = params['reflect_x']
        reflect_y = params['reflect_y']
        matrix = lg.create_reflection_matrix(reflect_x, reflect_y)

    # 5. CISALHAMENTO
    elif trans_type == 'shear':
        shx = float(params['shx'])
        shy = float(params['shy'])
        matrix = lg.create_shear_matrix(shx, shy)

    # Aplica a transformação usando a lógica modularizada
    new_points = lg.apply_transform(points, matrix)
    
    return jsonify(new_points)