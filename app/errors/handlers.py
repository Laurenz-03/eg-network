from flask import Blueprint, render_template
from flask_login import login_required

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
@login_required
def error_404(error):
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
@login_required
def error_403(error):
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
@login_required
def error_500(error):
    return render_template('errors/500.html'), 500