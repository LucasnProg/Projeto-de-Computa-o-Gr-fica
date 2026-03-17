from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg
import threading

vp_threed_bp = Blueprint(
    'vp_3d',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/vp_threed/static'
)

@vp_threed_bp.route('/vp_threed')
def vp_threed_page():
    return render_template('vp_threed_index.html')

@vp_threed_bp.route('/api/vp_threed/transform', methods=['POST'])
def api_transform():
    data = request.json
    trans_type = data.get('type')
    points = data.get('points') 
    params = data.get('params')

    new_points = points

    x_0 = points[0]['x'] 
    y_0 = points[0]['y'] 
    z_0 = points[0]['z']

    if trans_type == 'translate':
        tx = float(params['tx'])
        ty = float(params['ty'])
        tz = float(params['tz'])
        new_points = lg.tralade_object_3d(points, tx, ty, tz)

    elif trans_type in ['scale', 'rotate', 'reflection', 'shear']:
        
        pts_origem = lg.tralade_object_3d(points, -x_0, -y_0, -z_0)

        if trans_type == 'scale':
            sx = float(params['sx'])
            sy = float(params['sy'])
            sz = float(params['sz'])
            pts_transformados = lg.scale_object_3d(pts_origem, sx, sy, sz)

        elif trans_type == 'rotate':
            angle = float(params['angle'])
            axis = params['axis']
            pts_transformados = lg.rotate_object_3d(pts_origem, angle, axis)

        elif trans_type == 'reflection':
            axis = params['axis'] 
            pts_transformados = lg.reflect_object_3d(pts_origem, axis)

        elif trans_type == 'shear':
            axis = params['axis']
            sh1 = float(params['sh1'])
            sh2 = float(params['sh2'])
            pts_transformados = lg.shear_object_3d(pts_origem, axis, sh1, sh2)

        new_points = lg.tralade_object_3d(pts_transformados, x_0, y_0, z_0)

    return jsonify(new_points)

@vp_threed_bp.route('/api/vp_threed/window_to_vp', methods=['POST'])
def api_windows_to_vp():
    data = request.json
    points_3d = data.get('points')
    edges = data.get('edges', [])
    
    if edges:
        lg.opengl_viewer.update_live_object(points_3d, edges)
    projected_points_2d = lg.projecao_paralela_isometrica(points_3d)
    
    umin, umax = 30, 150
    vmin, vmax = 20, 200

    w_xmin, w_xmax = 0, 300
    w_ymin, w_ymax = 0, 300

    sx = (umax - umin) / (w_xmax - w_xmin)
    sy = (vmax - vmin) / (w_ymax - w_ymin)

    translacao_1 = lg.tralade_object(projected_points_2d, -w_xmin, -w_ymin)
    escala = lg.scale_object(translacao_1, sx, sy)
    pontos_finais_vp = lg.tralade_object(escala, umin, vmin)

    clipped_edges = []
    for edge in edges:
        p1 = pontos_finais_vp[edge[0]]
        p2 = pontos_finais_vp[edge[1]]
        
        resultado = lg.cohen_sutherland(
            p1['x'], p1['y'], p2['x'], p2['y'], 
            umin, vmin, umax, vmax
        )
        
        if resultado:
            if isinstance(resultado, dict):
                clipped_edges.append({
                    'x1': round(resultado.get('x1', resultado.get('x', p1['x'])), 2), 
                    'y1': round(resultado.get('y1', resultado.get('y', p1['y'])), 2), 
                    'x2': round(resultado.get('x2', p2['x']), 2), 
                    'y2': round(resultado.get('y2', p2['y']), 2)
                })
            else:
                clipped_edges.append({
                    'x1': round(resultado[0], 2), 'y1': round(resultado[1], 2), 
                    'x2': round(resultado[2], 2), 'y2': round(resultado[3], 2)
                })
    
    return jsonify({
        "unclipped": pontos_finais_vp,
        "clipped_edges": clipped_edges 
    })


@vp_threed_bp.route('/api/vp_threed/opengl_view', methods=['POST'])
def api_opengl_view():
    data = request.json
    points = data.get('points', [])
    edges = data.get('edges', [])

    if edges:
        lg.opengl_viewer.update_live_object(points, edges)

    if not lg.opengl_viewer.window_initialized:
        threading.Thread(target=lg.opengl_viewer.open_3d_window, daemon=True).start()

    return jsonify({"status": "Visualizador 3D aberto com sucesso"})