from flask import Blueprint, render_template
main_bp = Blueprint('mod_1_main', __name__, template_folder='templates')


@main_bp.route('/')
def index():
    return render_template('main_index.html')
