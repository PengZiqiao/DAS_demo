from flask import render_template
from flask_login import login_required
from . import bp


@bp.route('/')
def index():
    return render_template('main/index.html')
