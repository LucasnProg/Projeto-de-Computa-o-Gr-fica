from flask import Blueprint, render_template, request, jsonify
import graphics_logic as lg

twod_bp = Blueprint(
    "mod_5_twod",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/twod/static",
)


@twod_bp.route("/2d")
def twod_page():
    return render_template("twod_index.html")


@twod_bp.route("/api/twod/transform", methods=["POST"])
def api_transform():
    data = request.json
    points = data["points"]
    params = data["params"]
    t_type = data["type"]

    if t_type == "translate":
        matrix = lg.create_translation_matrix(params["tx"], params["ty"])
    elif t_type == "scale":
        matrix = lg.create_scale_matrix(
            params["sx"], params["sy"], params["cx"], params["cy"]
        )
    elif t_type == "rotate":
        matrix = lg.create_rotation_matrix(params["angle"],
                                           params["cx"], params["cy"])
    elif t_type == "reflection":  # <-- ADICIONADO
        matrix = lg.create_reflection_matrix(params["reflect_x"],
                                             params["reflect_y"])
    elif t_type == "shear":  # <-- ADICIONADO
        matrix = lg.create_shear_matrix(params["shx"], params["shy"])
    else:
        return jsonify({"error": "Unknown transform type"}), 400

    new_points = lg.apply_transform(points, matrix)
    return jsonify(new_points)
