from flask import Blueprint, render_template

pdi_bp = Blueprint(
    "mod_12_pdi_transform",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/pdi/static",
)


@pdi_bp.route("/pdi-transform")
def pdi_page():
    """Rota para a página de Transformação Geométrica de Imagens (PDI)."""
    return render_template("pdi_index.html")
