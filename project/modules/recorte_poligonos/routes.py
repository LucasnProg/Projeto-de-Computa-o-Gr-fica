from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

sh_bp = Blueprint(
    "mod_8_sutherland_hodgman",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/sh/static",
)

@sh_bp.route("/sutherland-hodgman")
def sh_page():
    return render_template("sh_index.html")

@sh_bp.route("/api/sh/clip", methods=["POST"])
def api_clip_sh():
    data = request.json
    subject = data.get("subjectPolygon", [])
    window = data.get("clipWindow", {})

    x_min = float(window.get("xmin", -100))
    y_min = float(window.get("ymin", -100))
    x_max = float(window.get("xmax", 100))
    y_max = float(window.get("ymax", 100))

    clipped_polygon = lg.polygonClipSuthHodg(subject, x_min, y_min, x_max, y_max)

    return jsonify({"clippedPolygon": clipped_polygon})