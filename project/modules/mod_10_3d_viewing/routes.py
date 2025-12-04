from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg
import re

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
    """
    Processar vértices e lista de comandos de transformação.
    Esperado JSON: { "vertices": [...], "transforms": ["T(10,0,0)", "Rx(90)", ...] }
    """
    data = request.json
    vertices = data.get('vertices', [])
    transforms_list = data.get('transforms', [])

    # 1. Iniciar com Matriz Identidade
    final_matrix = lg.projection.get_identity_4x4()

    # 2. Processar cada string de comando vinda do JS
    # O JS envia strings como: "T(100,50,0)", "Rx(45)", "Sh_xy(0.2,0.2)"
    for cmd in transforms_list:
        mat = lg.projection.get_identity_4x4()
        
        # Parse usando Regex para extrair números
        # Ex: "T(100, 50, 0)" -> nums = [100.0, 50.0, 0.0]
        nums = [float(x) for x in re.findall(r"-?\d+\.?\d*", cmd)]
        
        if cmd.startswith('T(') and len(nums) >= 3:
            mat = lg.projection.create_translation_3d(nums[0], nums[1], nums[2])
            
        elif cmd.startswith('S(') and len(nums) >= 3:
            mat = lg.projection.create_scale_3d(nums[0], nums[1], nums[2])
            
        elif cmd.startswith('Rx(') and len(nums) >= 1:
            mat = lg.projection.create_rotation_x(nums[0])
            
        elif cmd.startswith('Ry(') and len(nums) >= 1:
            mat = lg.projection.create_rotation_y(nums[0])
            
        elif cmd.startswith('Rz(') and len(nums) >= 1:
            mat = lg.projection.create_rotation_z(nums[0])
            
        elif cmd.startswith('Sh_') and len(nums) >= 2:
            plane = cmd.split('(')[0] # Pega "Sh_xy", "Sh_xz", etc
            mat = lg.projection.create_shear_3d(plane, nums[0], nums[1])
            
        elif cmd.startswith('Rf_'):
            plane = cmd.split('(')[0] # Pega "Rf_xy", etc
            mat = lg.projection.create_reflection_3d(plane)

        # Multiplicação cumulativa: M_final = M_nova * M_acumulada
        # (A ordem de multiplicação depende da convenção, aqui assumimos pré-multiplicação 
        # para aplicar a transformação mais recente sobre o resultado das anteriores)
        final_matrix = lg.projection.multiply_matrix_4x4(mat, final_matrix)

    # 3. Aplicar a matriz final aos vértices
    transformed_vertices = lg.projection.apply_matrix_to_points(vertices, final_matrix)

    # 4. Projetar para 2D (Perspectiva fixa para visualização)
    # d=500 é uma distância de câmera razoável para ver o objeto
    projected_2d = lg.projection.project_points_perspective(transformed_vertices, d=500)

    return jsonify({"projected_points": projected_2d})