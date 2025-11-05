from flask import Blueprint, render_template, request, jsonify
import graphics_logic as lg

wa_bp = Blueprint(
    "mod_9_weiler_atherton",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/wa/static",
)


@wa_bp.route("/weiler-atherton")
def wa_page():
    """Rota para a página de Recorte Weiler-Atherton."""
    return render_template("wa_index.html")


@wa_bp.route("/api/wa/clip", methods=["POST"])
def api_clip_wa():
    """
    API para recortar um polígono contra OUTRO POLÍGONO.
    """
    data = request.json

    subject_polygon = data["subjectPolygon"]
    clip_polygon = data["clipPolygon"]

    # ATENÇÃO: Esta função em graphics_logic.py é um STUB.
    # Ela retornará o polígono original até que a lógica
    # complexa do Weiler-Atherton seja implementada.
    clipped_polygon_list = lg.weiler_atherton_clip(subject_polygon, clip_polygon)

    response = {"clippedPolygons": clipped_polygon_list}

    return jsonify(response)
