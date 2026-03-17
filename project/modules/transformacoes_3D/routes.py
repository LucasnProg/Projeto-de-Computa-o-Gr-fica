from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg
import threading

view3d_bp = Blueprint(
    'mod_10_3d_viewing',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/view3d/static'
)

@view3d_bp.route('/view3d')
def view3d_page():
    return render_template('view3d_index.html')

@view3d_bp.route('/api/3d/render', methods=['POST'])
def api_render():
    data = request.json
    vertices = data.get('vertices', [])
    transforms_list = data.get('transforms', [])

    if not vertices:
        return jsonify({"projected_points": []})

    current_points = vertices
 

    for cmd in transforms_list:
        cmd_type = cmd.get('type')
        
        if cmd_type == 'translate':
            current_points = lg.tralade_object_3d(current_points, cmd['tx'], cmd['ty'], cmd['tz'])
            
        elif cmd_type in ['scale', 'rotate', 'shear', 'reflect']:
            
            x_0 = current_points[0]['x'] 
            y_0 = current_points[0]['y'] 
            z_0 = current_points[0]['z']

            current_points = lg.tralade_object_3d(current_points, -x_0, -y_0, -z_0)
            
            if cmd_type == 'scale':
                current_points = lg.scale_object_3d(current_points, cmd['sx'], cmd['sy'], cmd['sz'])
                
            elif cmd_type == 'rotate':
                current_points = lg.rotate_object_3d(current_points, cmd['angle'], cmd['axis'])
                
            elif cmd_type == 'shear':
                current_points = lg.shear_object_3d(current_points, cmd['axis'], cmd['sh1'], cmd['sh2'])
                
            elif cmd_type == 'reflect':
                current_points = lg.reflect_object_3d(current_points, cmd['axis'])
            
            current_points = lg.tralade_object_3d(current_points, x_0, y_0, z_0)

    return jsonify({"new_object": current_points})

@view3d_bp.route('/api/3d/project_object', methods=['POST'])
def project_object():
    data = request.json
    current_points = data.get('vertices', [])
    current_edges = data.get('edges', [])

    if current_edges:
        lg.opengl_viewer.update_live_object(current_points, current_edges)

    projected_2d = lg.projecao_paralela_isometrica(current_points)

    return jsonify({"projected_points": projected_2d})

@view3d_bp.route('/api/3d/opengl_view', methods=['POST'])
def opengl_view():
    data = request.json
    vertices = data.get('vertices', [])
    edges = data.get('edges', [])

    lg.opengl_viewer.update_live_object(vertices, edges)

    if not lg.opengl_viewer.window_initialized:
        threading.Thread(target=lg.opengl_viewer.open_3d_window, daemon=True).start()

    return jsonify({"status": "Visualizador 3D aberto/atualizado com sucesso!"})