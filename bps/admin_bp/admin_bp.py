from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import bcrypt
import secrets
import string
from datetime import datetime
from config import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
def dashboard():
    return render_template('admin/dashboard.html',
           username='xqy',
           user_count=100,
           key_count=200,
           log_count=300,
           recent_logs=123)

@admin_bp.route('users')
def users():
       pass

@admin_bp.route('keys')
def keys():
       pass

@admin_bp.route('users')
def users():
       pass

@admin_bp.route('login_logs')
def login_logs():
       pass

@admin_bp.route('logout')
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


def login_required(f):
    """登录验证装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_user_id' not in session:
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)

    return decorated_function


def generate_api_key(length=32):
    """生成随机API密钥"""
    chars = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>?'
    return ''.join(secrets.choice(chars) for _ in range(length))
#
#
# # ==================== 登录页面 ====================
# @admin_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         conn = db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id, username, password FROM user WHERE username = %s", (username,))
#         user = cursor.fetchone()
#         cursor.close()
#
#         if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
#             # 记录登录日志
#             cursor = conn.cursor()
#             cursor.execute("""
#                            INSERT INTO login_log (user_id, username, ip_address, device_info, login_time)
#                            VALUES (%s, %s, %s, %s, %s)
#                            """, (user['id'], user['username'], get_client_ip(), get_device_info(), datetime.now()))
#             conn.commit()
#             cursor.close()
#
#             session['admin_user_id'] = user['id']
#             session['admin_username'] = user['username']
#             session.permanent = True
#
#             return redirect(url_for('admin_bp.dashboard'))
#         else:
#             flash('用户名或密码错误', 'error')
#
#     # return render_template('login.html')
#
#
# @admin_bp.route('/logout')
# def logout():
#     session.clear()
#     return redirect(url_for('admin.login'))
#
#
# # ==================== 仪表盘 ====================
# @admin_bp.route('/dashboard')
# @login_required
# def dashboard():
#     conn = db()
#     cursor = conn.cursor()
#
#     # 统计数据
#     cursor.execute("SELECT COUNT(*) as count FROM user")
#     user_count = cursor.fetchone()['count']
#
#     cursor.execute("SELECT COUNT(*) as count FROM api_key WHERE status = '1'")
#     key_count = cursor.fetchone()['count']
#
#     cursor.execute("SELECT COUNT(*) as count FROM login_log")
#     log_count = cursor.fetchone()['count']
#
#     # 最近登录日志
#     cursor.execute("""
#                    SELECT *
#                    FROM login_log
#                    ORDER BY login_time DESC LIMIT 10
#                    """)
#     recent_logs = cursor.fetchall()
#     cursor.close()
#
#     return render_template('dashboard.html',
#                            username=session.get('admin_username'),
#                            user_count=user_count,
#                            key_count=key_count,
#                            log_count=log_count,
#                            recent_logs=recent_logs)
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