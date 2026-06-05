from flask import Blueprint, render_template, session, redirect, url_for, request
from bps.attendance_bp.service.attendance_service import process_index_data, query_data
from bps.attendance_bp.service.attendance_service import do_import as do_import_service

attendance_bp = Blueprint('attendance_bp', __name__, template_folder='attendance_templates', url_prefix='/attendance')

@attendance_bp.route('/index')
def index():
    if 'username' in session:
        records = process_index_data()
        return render_template('bp/attendance_bp/index.html',records = records, username = session['username'])
    else:
        return redirect(url_for('index_bp.login'))

# 导入页面路由，确保URL无异常
@attendance_bp.route('/import')
def import_page():
    if 'username' in session:
        return render_template('bp/attendance_bp/import.html', username = session['username'])
    else:
        return redirect(url_for('index_bp.login'))


@attendance_bp.route('/do_import', methods=['POST'])
def do_import():
    if 'username' in session:
        msg = do_import_service(request, session['username'])
        return render_template('bp/attendance_bp/import.html',msg = msg, username = session['username'])
    else:
        return redirect(url_for('index_bp.login'))

# 查询页面路由，保持URL规范
@attendance_bp.route('/query', methods=['GET', 'POST'])
def query():
    if 'username' in session:
        data = query_data(request)
        return render_template('bp/attendance_bp/query.html',**data, username = session['username'])
    else:
        return redirect(url_for('index_bp.login'))
