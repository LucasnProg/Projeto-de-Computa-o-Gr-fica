from flask import Blueprint, render_template, request, jsonify
import graphics_logic as lg

pipeline_bp = Blueprint(
    "mod_11_2d_pipeline",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/pipeline/static",
)


@pipeline_bp.route("/2d-pipeline")
def pipeline_page():
    return render_template("pipeline_index.html")


@pipeline_bp.route("/api/2d/pipeline_process", methods=["POST"])
def api_process_pipeline():
    """
    API que implementa o pipeline 2D:
    1. Recebe um polígono (World Coords)
    2. Recebe uma Janela (World Coords)
    3. Recebe uma Viewport (Device Coords)
    4. Recorta o polígono contra a Janela (World Coords)
    5. Mapeia o polígono recortado para a Viewport (Device Coords)
    """
    data = request.json
    subject_polygon = data["subjectPolygon"]
    window = data["window"]
    viewport = data["viewport"]

    # 1. Recorte (Clipping)
    # (1).pdf]
    # Usamos o algoritmo Sutherland-Hodgman do Módulo 8
    clipped_polygon_world = lg.sutherland_hodgman_clip(subject_polygon, window)

    if not clipped_polygon_world:
        return jsonify({"viewport_polygon": []})  # Polígono totalmente recortado

    # 2. Mapeamento (Window-to-Viewport)
    # (1).pdf]
    viewport_polygon = []
    for vertex in clipped_polygon_world:
        xw = vertex["x"]
        yw = vertex["y"]
        # Mapeia da Janela do Mundo para a Viewport
        viewport_point = lg.map_window_to_viewport(xw, yw, window, viewport)
        viewport_polygon.append(viewport_point)

    return jsonify({"viewport_polygon": viewport_polygon})
