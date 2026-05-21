from flask import render_template, Blueprint


sfs_bp = Blueprint('sfs_bp', __name__, template_folder='sfs_templates', static_folder='sfs_static', url_prefix='/sfs')

import os

# 自动获取当前蓝图所在目录（跨系统通用）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
bp_static_path = os.path.join(BASE_DIR, "static")

@sfs_bp.route('/')
def a():
    return render_template('sfs_index.html')