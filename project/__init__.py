from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    from .modules.mod_1_main.routes import main_bp
    from .modules.mod_2_coordenadas.routes import sc_bp
    from .modules.mod_3_retas.routes import retas_bp
    from .modules.mod_4_circunferencia.routes import circ_bp
    from .modules.mod_5_twod.routes import twod_bp
    from .modules.mod_6_elipse.routes import elipse_bp
    from .modules.mod_7_clipping.routes import clipping_bp
    from .modules.mod_8_sutherland_hodgman.routes import sh_bp
    from .modules.mod_9_weiler_atherton.routes import wa_bp
    from .modules.mod_10_3d_viewing.routes import view3d_bp
    from .modules.mod_11_2d_pipeline.routes import pipeline_bp
    from .modules.mod_12_pdi_transform.routes import pdi_bp
    from .modules.mod_13_bezier.routes import bezier_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(sc_bp)
    app.register_blueprint(retas_bp)
    app.register_blueprint(circ_bp)
    app.register_blueprint(twod_bp)
    app.register_blueprint(elipse_bp)
    app.register_blueprint(clipping_bp)
    app.register_blueprint(sh_bp)
    app.register_blueprint(wa_bp)
    app.register_blueprint(view3d_bp)
    app.register_blueprint(pipeline_bp)
    app.register_blueprint(pdi_bp)
    app.register_blueprint(bezier_bp)
    
    return app
