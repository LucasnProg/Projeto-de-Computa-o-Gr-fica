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


    new_points = points

    if trans_type == 'translate':
        tx = float(params['tx'])
        ty = float(params['ty'])
        new_points = lg.tralade_object(points, tx, ty)

    elif trans_type == 'scale':
        sx = float(params['sx'])
        sy = float(params['sy'])
        
        cx = points[0]['x']
        cy = points[0]['y']
        
        pts_origem = lg.tralade_object(points, -cx, -cy)
        pts_escalados = lg.scale_object(pts_origem, sx, sy)
        new_points = lg.tralade_object(pts_escalados, cx, cy)

    elif trans_type == 'rotate':
        angle = float(params['angle'])
        
        cx = points[0]['x']
        cy = points[0]['y']
        
        pts_origem = lg.tralade_object(points, -cx, -cy)
        pts_rotacionados = lg.rotate_object(pts_origem, angle)
        new_points = lg.tralade_object(pts_rotacionados, cx, cy)

    elif trans_type == 'reflection':
        reflect_x = params.get('reflect_x', False)
        reflect_y = params.get('reflect_y', False)
        
        axis = ""
        if reflect_x and reflect_y:
            axis = "xy"
        elif reflect_x:
            axis = "x"
        elif reflect_y:
            axis = "y"
            
        if axis:
            cx = points[0]['x']
            cy = points[0]['y']
        
        
            new_points = lg.reflect_object(points, axis)

    elif trans_type == 'shear':
        shx = float(params['shx'])
        shy = float(params['shy'])
        new_points = lg.shear_object(points, shx, shy)

    return jsonify(new_points)