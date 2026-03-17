from flask import Flask


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    from .modules.mod_1_main.routes import main_bp
    from .modules.retas.routes import retas_bp
    from .modules.circunferencia.routes import circ_bp
    from .modules.transformacoes_2D.routes import twod_bp
    from .modules.viewport_2D.routes import vp_twod_bp
    from .modules.viewport_3D.routes import vp_threed_bp
    from .modules.elipse.routes import elipse_bp
    from .modules.recorte_suterland.routes import clipping_bp
    from .modules.recorte_poligonos.routes import sh_bp
    from .modules.transformacoes_3D.routes import view3d_bp
    from .modules.splines_bezier.routes import bezier_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(retas_bp)
    app.register_blueprint(circ_bp)
    app.register_blueprint(twod_bp)
    app.register_blueprint(elipse_bp)
    app.register_blueprint(clipping_bp)
    app.register_blueprint(sh_bp)
    app.register_blueprint(view3d_bp)
    app.register_blueprint(bezier_bp)
    app.register_blueprint(vp_twod_bp)
    app.register_blueprint(vp_threed_bp)
    
    return app
