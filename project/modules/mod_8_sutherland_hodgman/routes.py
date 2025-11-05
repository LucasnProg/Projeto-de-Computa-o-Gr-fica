from flask import Blueprint, render_template, request, jsonify
import graphics_logic as lg

sh_bp = Blueprint(
    "mod_8_sutherland_hodgman",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/sh/static",
)


@sh_bp.route("/sutherland-hodgman")
def sh_page():
    """Rota para a página de Recorte Sutherland-Hodgman."""
    return render_template("sh_index.html")


@sh_bp.route("/api/sh/clip", methods=["POST"])
def api_clip_sh():
    """
    API para recortar um polígono contra uma JANELA RETANGULAR.
    """
    data = request.json

    subject_polygon = data["subjectPolygon"]
    clip_window = data["clipWindow"]

    clipped_polygon = lg.sutherland_hodgman_clip(subject_polygon, clip_window)

    response = {"clippedPolygon": clipped_polygon}

    return jsonify(response)
