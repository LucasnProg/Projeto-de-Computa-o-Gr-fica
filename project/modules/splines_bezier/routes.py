from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

bezier_bp = Blueprint(
    "mod_13_bezier",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/bezier/static",
)

@bezier_bp.route("/bezier-curves")
def bezier_page():
    """ Rota para a página de Curvas de Bézier. """
    return render_template("bezier_index.html")

@bezier_bp.route("/api/bezier/calculate", methods=["POST"])
def api_calculate_bezier():
    data = request.json
    
    p0 = data.get('p0')
    p1 = data.get('p1')
    p2 = data.get('p2')
    p3 = data.get('p3')
    
    if not all([p0, p1, p2, p3]):
        return jsonify({"error": "Todos os 4 pontos de controle são obrigatórios"}), 400

    points = [p0, p1, p2, p3]
    
    curve_points = lg.calculate_bezier_curve(points)
    
    return jsonify({
        "curve_points": curve_points
    })