from flask import Blueprint, render_template, session, redirect, url_for

attendance_bp = Blueprint('attendance_bp', __name__, template_folder='attendance_templates', static_folder='attendance_static', url_prefix='/attendance')

@attendance_bp.route('/index')
def index():
    if 'username' in session:
        return render_template('attendance/index.html', username = session['username'])
    else:
        return redirect(url_for('index_bp.login'))