from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

retas_bp = Blueprint(
    "mod_3_retas",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/retas/static",
)


@retas_bp.route("/retas")
def retas_page():
    return render_template("retas_index.html")


@retas_bp.route("/api/retas/draw_line", methods=["POST"])
def api_draw_line():
    data = request.json
    p = [float(data["x1"]), float(data["y1"]),
         float(data["x2"]), float(data["y2"])]
    if data["algo"] == "DDA":
        points, x_inc, y_inc = lg.dda_line(*p)
        reponse = {"points": points, "x_inc": x_inc, "y_inc": y_inc}
        return jsonify(reponse)
    else:
        points = lg.bresenham_line(*p)
        reponse = {"points": points}
        return jsonify(reponse)
