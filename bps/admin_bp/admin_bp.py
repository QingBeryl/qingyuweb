from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from config import db
from bps.index_bp.service.user_service import get_user
from bps.admin_bp.service.login_log_service import get_user_count_service, get_user_secret_count_service, get_login_log_count_service, get_logs_service

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/users')
def users():
       pass

@admin_bp.route('/keys')
def keys():
       pass

@admin_bp.route('/login_logs')
def login_logs():
       pass

@admin_bp.route('/logout')
def logout():
       pass
# ==================== 工具函数 ====================
def get_client_ip():
    """获取客户端真实IP"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr


def get_device_info():
    """获取设备信息"""
    return request.user_agent.string[:500]


# @admin_bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('admin.login'))
#
#
# ==================== 仪表盘 ====================
@admin_bp.route('/')
def dashboard():
    if 'username' in session:
        user = get_user(session['username'])
        return render_template('bp/admin/dashboard.html',
               username=session['username'],
               user_count=get_user_count_service(),
               key_count=get_user_secret_count_service(),
               log_count=get_login_log_count_service(),
               recent_logs=get_logs_service())
    else:
        return redirect(url_for('index_bp.login'))


    conn = db()
    cursor = conn.cursor()



    # 最近登录日志
    cursor.execute("""
                   SELECT *
                   FROM login_log
                   ORDER BY login_time DESC LIMIT 10
                   """)
    recent_logs = cursor.fetchall()
    cursor.close()

    return render_template('dashboard.html',
                           username=session.get('admin_username'),
                           user_count=user_count,
                           key_count=key_count,
                           log_count=log_count,
                           recent_logs=recent_logs)
#
#
# # ==================== 用户管理 ====================
# @admin_bp.route('/users')
# @login_required
# def users():
#     conn = db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id, username, signature FROM user")
#     users = cursor.fetchall()
#     cursor.close()
#
#     return render_template('users.html',
#                            username=session.get('admin_username'),
#                            users=users)
#
#
# @admin_bp.route('/user/edit/<int:user_id>', methods=['POST'])
# @login_required
# def edit_user(user_id):
#     username = request.form.get('username')
#     signature = request.form.get('signature')
#     new_password = request.form.get('password')
#
#     conn = db()
#     cursor = conn.cursor()
#
#     if new_password:
#         hashed_pw = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
#         cursor.execute("""
#                        UPDATE user
#                        SET username  = %s,
#                            signature = %s,
#                            password  = %s
#                        WHERE id = %s
#                        """, (username, signature, hashed_pw, user_id))
#     else:
#         cursor.execute("""
#                        UPDATE user
#                        SET username  = %s,
#                            signature = %s
#                        WHERE id = %s
#                        """, (username, signature, user_id))
#
#     conn.commit()
#     cursor.close()
#     flash('用户信息更新成功', 'success')
#     return redirect(url_for('admin.users'))
#
#
# # ==================== 密钥管理 ====================
# @admin_bp.route('/keys')
# @login_required
# def keys():
#     conn = db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM api_key ORDER BY id DESC")
#     keys = cursor.fetchall()
#     cursor.close()
#
#     return render_template('keys.html',
#                            username=session.get('admin_username'),
#                            keys=keys)
#
#
# @admin_bp.route('/key/generate', methods=['POST'])
# @login_required
# def generate_key():
#     new_key = generate_api_key()
#     conn = db()
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO api_key (`key`, status) VALUES (%s, '1')", (new_key,))
#     conn.commit()
#     cursor.close()
#     flash('新密钥生成成功', 'success')
#     return redirect(url_for('admin.keys'))
#
#
# @admin_bp.route('/key/toggle/<int:key_id>')
# @login_required
# def toggle_key(key_id):
#     conn = db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT status FROM api_key WHERE id = %s", (key_id,))
#     key = cursor.fetchone()
#     new_status = '0' if key['status'] == '1' else '1'
#     cursor.execute("UPDATE api_key SET status = %s WHERE id = %s", (new_status, key_id))
#     conn.commit()
#     cursor.close()
#     return redirect(url_for('admin.keys'))
#
#
# @admin_bp.route('/key/delete/<int:key_id>')
# @login_required
# def delete_key(key_id):
#     conn = db()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM api_key WHERE id = %s", (key_id,))
#     conn.commit()
#     cursor.close()
#     flash('密钥删除成功', 'success')
#     return redirect(url_for('admin.keys'))
#
#
# # ==================== 登录日志 ====================
# @admin_bp.route('/login-logs')
# @login_required
# def login_logs():
#     conn = db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM login_log ORDER BY login_time DESC")
#     logs = cursor.fetchall()
#     cursor.close()
#
#     return render_template('login_logs.html',
#                            username=session.get('admin_username'),
#                            logs=logs)