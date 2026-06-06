from flask import Blueprint, render_template, session, redirect, url_for, request
from bps.attendance_bp.service.attendance_service import process_index_data, query_data
from bps.attendance_bp.service.attendance_service import do_import_service,get_all_classes_service

attendance_bp = Blueprint('attendance_bp', __name__, template_folder='attendance_templates', url_prefix='/attendance')

@attendance_bp.route('/index')
def index():
    if 'username' in session:
        records = process_index_data()
        return render_template('bp/attendance_bp/index.html',records = records, username = session['username'])
    else:
        return redirect(url_for('index_bp.login'))

# 导入页面路由，确保URL无异常
# 这是你显示导入页面的路由（不是do_import接口）
@attendance_bp.route('/import', methods=['GET'])
def import_page():
    if 'username' in session:
        classes = get_all_classes_service()

        if not classes:
            return render_template('bp/attendance_bp/import.html',
                                   msg="错误：系统中没有任何班级数据，请先导入学生名单",
                                   username=session['username'])

        return render_template('bp/attendance_bp/import.html',
                               classes=classes,
                               username=session['username'])
    else:
        return redirect(url_for('index_bp.login'))


@attendance_bp.route('/do_import', methods=['POST'])
@attendance_bp.route('/do_import', methods=['POST'])
def do_import():
    if 'username' in session:
        student_class = request.form.get('student_class')
        if not student_class:
            classes = get_all_classes_service()
            return render_template('bp/attendance_bp/import.html',
                                   msg="错误：请选择班级",
                                   classes=classes,
                                   username=session['username'])

        files = request.files.getlist('file[]')
        msg = do_import_service(files, session['username'], student_class)

        classes = get_all_classes_service()

        return render_template('bp/attendance_bp/import.html',
                               msg=msg,
                               classes=classes,
                               username=session['username'])
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
