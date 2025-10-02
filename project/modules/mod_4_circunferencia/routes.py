from flask import Blueprint, render_template, request, jsonify
import graphics_logic as lg

circ_bp = Blueprint(
    "mod_4_circunferencia",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/circ/static",
)


@circ_bp.route("/circunferencias")
def circ_page():
    return render_template("circ_index.html")


@circ_bp.route("/api/circ/draw_circle", methods=["POST"])
def api_draw_circle():
    data = request.json
    xc, yc, r = int(data["xc"]), int(data["yc"]), int(data["r"])
    algo = data["algo"]

    # Lógica para escolher qual função de cálculo usar
    if algo == "PontoMedio":
        points = lg.mid_Point_circle(xc, yc, r)
    elif algo == "Explicit":
        points = lg.explicit_circle(xc, yc, r)
    elif algo == "Parametric":
        points = lg.parametric_circle(xc, yc, r)
    else:
        # Padrão para Bresenham se o algoritmo for desconhecido
        points = lg.bresenham_circle(xc, yc, r)

    return jsonify(points)
