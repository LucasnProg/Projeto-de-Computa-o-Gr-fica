from flask import Blueprint, render_template, request, jsonify
import graphics_logic as lg

view3d_bp = Blueprint(
    "mod_10_3d_viewing",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/view3d/static",
)

@view3d_bp.route("/3d-viewing")
def view3d_page():
    return render_template("view3d_index.html")

@view3d_bp.route("/api/3d/render", methods=["POST"])
def api_render_3d():
    """
    API que recebe vértices de um objeto 3D e uma lista de transformações.
    Retorna os pontos 2D projetados.
    """
    data = request.json
    vertices = data["vertices"]       # Vértices 3D originais
    transforms = data["transforms"]   # Lista de strings de transformação

    # Aplica transformações e projeção isométrica
    projected_2d_points = lg.apply_3d_transform_and_project(vertices, transforms)
    
    return jsonify({"projected_points": projected_2d_points})