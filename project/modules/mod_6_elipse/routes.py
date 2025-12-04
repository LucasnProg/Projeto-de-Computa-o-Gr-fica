from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

elipse_bp = Blueprint(
    "mod_6_elipse",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/elipse/static",
)


@elipse_bp.route("/elipse")
def elipse_page():
    return render_template("elipse_index.html")


@elipse_bp.route("/api/elipse/draw_elipse", methods=["POST"])
def api_draw_elipse():
    data = request.json
    xc, yc, = int(data["xc"]), int(data["yc"])
    rx, ry = int(data["rx"]), int(data["ry"])
    points = lg.elipse_mid_point(xc, yc, rx, ry)

    return jsonify(points)
