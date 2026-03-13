from flask import Blueprint, render_template, request, jsonify
from project import graphics_logic as lg

wa_bp = Blueprint(
    "mod_9_weiler_atherton",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/wa/static",
)

@wa_bp.route("/weiler-atherton")
def wa_page():
    return render_template("wa_index.html")

@wa_bp.route("/api/wa/clip", methods=["POST"])
def api_clip_wa():
    data = request.json
    subject = data.get("subjectPolygon", [])
    clip = data.get("clipPolygon", [])

    # A função lógica retorna UM polígono (lista de pontos)
    result_points = lg.weiler_atherton_clip(subject, clip)

    response = {"clippedPolygons": [result_points]}

    return jsonify(response)