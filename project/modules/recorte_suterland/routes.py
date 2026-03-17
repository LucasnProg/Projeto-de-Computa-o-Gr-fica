from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

clipping_bp = Blueprint(
    "mod_7_clipping",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/clipping/static",
)


@clipping_bp.route("/clipping")
def clipping_page():
    """Rota para a página de Recorte de Linha."""
    return render_template("clipping_index.html")


@clipping_bp.route("/api/clipping/clip_line", methods=["POST"])
def api_clip_line():
    """
    API para receber uma linha e uma janela,
    e retornar a linha recortada.
    """
    data = request.json

    x1, y1 = float(data["x1"]), float(data["y1"])
    x2, y2 = float(data["x2"]), float(data["y2"])

    xmin, ymin = float(data["xmin"]), float(data["ymin"])
    xmax, ymax = float(data["xmax"]), float(data["ymax"])

    clipped_coords = lg.cohen_sutherland(x1, y1, x2, y2, xmin, ymin, xmax, ymax)

    if clipped_coords:
        response = {"accepted": True, "coords": clipped_coords}
    else:
        response = {"accepted": False}

    return jsonify(response)
