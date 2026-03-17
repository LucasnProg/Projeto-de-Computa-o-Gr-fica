from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

vp_twod_bp = Blueprint(
    'vp_2d',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/vp_twod/static'
)

@vp_twod_bp.route('/vp_twod')
def vp_twod_page():
    return render_template('vp_twod_index.html')

@vp_twod_bp.route('/api/vp_twod/transform', methods=['POST'])
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

@vp_twod_bp.route('/api/vp_twod/window_to_vp', methods=['POST'])
def api_windows_to_vp():
    data = request.json
    points = data.get('points')
    
    umin, umax = 30, 150
    vmin, vmax = 20, 200


    w_xmin, w_xmax = 0, 300
    w_ymin, w_ymax = 0, 300

    sx = (umax - umin) / (w_xmax - w_xmin)
    sy = (vmax - vmin) / (w_ymax - w_ymin)

    passo_a = lg.tralade_object(points, -w_xmin, -w_ymin)
    
    passo_b = lg.scale_object(passo_a, sx, sy)
    
    pontos_finais_vp = lg.tralade_object(passo_b, umin, vmin)

    pontos_recortados = lg.polygonClipSuthHodg(pontos_finais_vp, umin, vmin, umax, vmax)
    
    return jsonify({
        "unclipped": pontos_finais_vp,
        "clipped": pontos_recortados
    })