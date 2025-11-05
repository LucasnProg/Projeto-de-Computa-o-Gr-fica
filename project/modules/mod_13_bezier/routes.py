from flask import Blueprint, render_template, request, jsonify
import graphics_logic as lg

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
    """
    API para calcular uma curva de Bézier cúbica.
    Recebe 4 pontos de controle (p0, p1, p2, p3).
    """
    data = request.json
    try:
        p0 = data["p0"]
        p1 = data["p1"]
        p2 = data["p2"]
        p3 = data["p3"]
        
        # Chama a lógica que implementa a fórmula de Bézier Cúbica
        # (1).pdf]
        curve_points = lg.calculate_bezier_cubic(p0, p1, p2, p3, steps=100)
        
        return jsonify({"curve_points": curve_points})
    
    except KeyError:
        return jsonify({"error": "Dados incompletos. São necessários 4 pontos de controle."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500