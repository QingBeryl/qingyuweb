from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from bps.admin_bp.service.dashboard_service import get_user_count_service, get_user_secret_count_service, get_login_log_count_service, get_recent_logs_service
from bps.admin_bp.service.users_service import get_all_users_service, get_user_by_id, updata_user_by_id_service
from bps.index_bp.utils.bcrypt_util import bcrypt_verify, bcrypt_hash
from bps.admin_bp.service.key_service import get_all_keys_service, add_key_service
from bps.admin_bp.service.login_logs_service import get_login_logs
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


# @admin_bp.route('/users')
# def users():
#        pass

# @admin_bp.route('/keys')
# def keys():
#        pass

# @admin_bp.route('/login_logs')
# def login_logs():
#        pass

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username:
            if password:
                if username == 'admin':
                    if bcrypt_verify(password, '$2b$13$kcznma3s/yxmOKSpZdgvneh8OPTiwlcni0EsIOlZX.hLtO2rThRaK'):
                        session['username'] = username
                        flash('登录成功！ 相逢于此，万事顺遂', 'success')
                        return redirect(url_for('admin.dashboard'))
                    else:
                        flash('心意未达，下次再见 用户名或密码错误！', 'error')
                        return redirect(url_for('admin.login'))
                else:
                    flash('用户不存在！', 'error')
            else:
                flash('密码不能为空！', 'error')
        else:
            flash('用户名不能为空！', 'error')
        return redirect(url_for('admin.login'))
    else:
        return render_template('bp/admin/login.html')

# ==================== 仪表盘 ====================
@admin_bp.route('/')
def dashboard():
    if 'username' in session:
        if session['username'] == 'admin':
            return render_template('bp/admin/dashboard.html',
                   username=session['username'],
                   user_count=get_user_count_service(),
                   key_count=get_user_secret_count_service(),
                   log_count=get_login_log_count_service(),
                   recent_logs=get_recent_logs_service())
        else:
            return redirect(url_for('admin.login'))
    else:
        return redirect(url_for('admin.login'))

# ==================== 用户管理 ====================
@admin_bp.route('/users')
def users():
    if 'username' in session:
        if session['username'] == 'admin':
            users = get_all_users_service()
            return render_template('bp/admin/users.html',
                   username=session['username'],
                   users=users)
        else:
            return redirect(url_for('admin.login'))
    else:
        return redirect(url_for('admin.login'))

@admin_bp.route('/user/edit/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    # 管理员权限校验
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('admin.login'))

    # 获取表单数据
    username = request.form.get('username')
    signature = request.form.get('signature')
    new_password = request.form.get('password')

    # 空值校验
    if not username:
        flash('用户名不能为空！', 'error')
        return redirect(url_for('admin.users'))

    # 标记是否需要更新
    need_update_name = False
    need_update_pwd = False
    need_update_sig = False
    user = get_user_by_id(user_id)

    # 校验更改内容
    if username != user['username']:
        need_update_name = True
        new_name = username
        print(username, user['username'], new_name)
    else:
        new_name = username

    if signature:
        need_update_sig = True
        new_sig = signature
    else:
        new_sig = '他看起来很懒，什么也没有留下'

    if new_password:
        if bcrypt_hash(new_password) != user['password']:
            need_update_pwd = True
            new_pwd = bcrypt_hash(new_password)
    else:
        new_pwd = user['password']

    # 执行更改操作
    if need_update_name or need_update_pwd or need_update_sig:
        updata_user_by_id_service(user_id, new_name, new_sig, new_pwd)
        flash('修改成功！', 'success')
        return redirect(url_for('admin.users'))
    else:
        flash('修改成功！', 'success')
        return redirect(url_for('admin.users'))
















    # if 'username' in session:
    #     if session['username'] == 'admin':
    #         username = request.form.get('username')
    #         signature = request.form.get('signature')
    #         new_password = request.form.get('password')
    #         user = get_user_by_id_dao(user_id)
    #         if username:
    #             if username ==  user['username']:
    #                 if new_password:
    #                     if signature:
    #                         if signature != user['signature']:
    #                             if bcrypt_hash(new_password) != user['password']:
    #                                 updata_signature_service(username, signature)
    #                                 update_password_service(username, new_password)
    #                                 return render_template(url_for('admin.users'))
    #                             else:
    #                                 flash('新密码与旧密码不能相同！', 'error')
    #                                 return render_template(url_for('admin.users'))
    #                         else:
    #                             flash('新签名与旧签名不能相同！', 'error')
    #                             return render_template(url_for('admin.users'))
    #                     else:
    #                         if bcrypt_verify(new_password) != user['password']:
    #                             updata_signature_service(username, '他看起来很懒，什么也没有留下')
    #                             update_password_service(username, new_password)
    #                             return render_template(url_for('admin.users'))
    #                         else:
    #                             flash('新密码与旧密码不能相同！', 'error')
    #                             return render_template(url_for('admin.users'))
    #                 else:
    #                     if signature:
    #                         if signature != user['signature']:
    #                             updata_signature_service(username, signature)
    #                             return render_template(url_for('admin.users'))
    #                         else:
    #                             flash('新签名与旧签名不能相同！', 'error')
    #                             return render_template(url_for('admin.users'))
    #                     else:
    #                         updata_signature_service(username, '他看起来很懒，什么也没有留下')
    #                         return render_template(url_for('admin.users'))
    #             else:
    #                 if new_password:
    #                     if signature:
    #                         if signature != user['signature']:
    #                             if bcrypt_hash(new_password) != user['password']:
    #                                 updata_signature_service(user['username'], signature)
    #                                 update_password_service(username, new_password)
    #                                 update_username_service(user['username'], username)
    #                                 return render_template(url_for('admin.users'))
    #                             else:
    #                                 flash('新密码与旧密码不能相同！', 'error')
    #                                 return render_template(url_for('admin.users'))
    #                         else:
    #                             flash('新签名与旧签名不能相同！', 'error')
    #                             return render_template(url_for('admin.users'))
    #                     else:
    #                         if bcrypt_verify(new_password) != user['password']:
    #                             updata_signature_service(username, '他看起来很懒，什么也没有留下')
    #                             update_password_service(username, new_password)
    #                             update_username_service(user['username'], username)
    #                             return render_template(url_for('admin.users'))
    #                         else:
    #                             flash('新密码与旧密码不能相同！', 'error')
    #                             return render_template(url_for('admin.users'))
    #                 else:
    #                     if signature:
    #                         if signature != user['signature']:
    #                             updata_signature_service(username, signature)
    #                             return render_template(url_for('admin.users'))
    #                         else:
    #                             flash('新签名与旧签名不能相同！', 'error')
    #                             return render_template(url_for('admin.users'))
    #                     else:
    #                         updata_signature_service(username, '他看起来很懒，什么也没有留下')
    #                         return render_template(url_for('admin.users'))
    #         else:
    #             flash('用户名不能为空！', 'error')
    #             return render_template(url_for('admin.users'))
    #     else:
    #         return redirect(url_for('admin.login'))
    # else:
    #     return redirect(url_for('admin.login'))






# def a():
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
# ==================== 密钥管理 ====================
@admin_bp.route('/keys')
def keys():
    # 管理员权限校验
    if 'username' not in session or session['username'] != 'admin':
        return redirect(url_for('admin.login'))
    keys = get_all_keys_service()

    return render_template('bp/admin/keys.html',
                           username=session['username'],
                           keys=keys)
#
#
@admin_bp.route('/key/generate', methods=['POST'])
def generate_key():
    add_key_service()
    return redirect(url_for('admin.keys'))

# @admin_bp.route('/key/toggle/<int:key_id>')
# def toggle_key(key_id):
#     pass
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
# def delete_key(key_id):
#     pass
#     conn = db()
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM api_key WHERE id = %s", (key_id,))
#     conn.commit()
#     cursor.close()
#     flash('密钥删除成功', 'success')
#     return redirect(url_for('admin.keys'))
#
#
#==================== 登录日志 ====================
@admin_bp.route('/login-logs')
def login_logs():
    logs = get_login_logs()
    return render_template('bp/admin/login_logs.html',
                           username=session['username'],
                           logs=logs)