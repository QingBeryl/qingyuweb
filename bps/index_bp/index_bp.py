from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash
from bps.index_bp.service.user_service import get_user
from bps.index_bp.utils.bcrypt_util import bcrypt_hash, bcrypt_verify
from bps.index_bp.service.user_service import secret_key, update_status, add_user, updata_signature_service, update_username_service, update_password_service
import os
index_bp = Blueprint('index_bp', __name__)


# 自动获取当前蓝图所在目录（跨系统通用）
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# bp_static_path = os.path.join(BASE_DIR, "index_static")


@index_bp.route('/')
def index():
    if 'username' in session:
        return render_template('bp/index_bp/index.html', username = session['username'])
    else:
        return render_template('bp/index_bp/index.html')
@index_bp.route('/project')
def project():
    if 'username' in session:
        return render_template('bp/index_bp/project.html', username = session['username'])
    else:
        return redirect(url_for('index_bp.login'))

@index_bp.route('/down')
def down():
    if 'username' in session:
        return render_template('bp/index_bp/down.html', username=session['username'])
    else:
        return redirect(url_for('index_bp.login'))

@index_bp.route('/about')
def about():
    if 'username' in session:
        return render_template('bp/index_bp/about.html', username=session['username'])
    else:
        return redirect(url_for('index_bp.login'))

@index_bp.route('/mine')
def mine():
    if 'username' in session:
        user = get_user(session['username'])
        return render_template('bp/index_bp/mine.html', username=session['username'], user=user)
    else:
        return redirect(url_for('index_bp.login'))
@index_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user(username)
        if username:
            if password:
                if user:
                    if bcrypt_verify(password, user['password']):
                        session['username'] = username
                        flash('登录成功！ 相逢于此，万事顺遂', 'success')
                        return redirect(url_for('index_bp.index'))
                    else:
                        flash('心意未达，下次再见 用户名或密码错误！', 'error')
                        return redirect(url_for('index_bp.login'))
                else:
                    flash('用户不存在！', 'error')
            else:
                flash('密码不能为空！', 'error')
        else:
            flash('用户名不能为空！', 'error')
        return redirect(url_for('index_bp.login'))
    else:
        return render_template('bp/index_bp/login.html')

@index_bp.route('/logout')
def logout():
    session.clear()
    flash('暂别此间，下次再会', 'success')
    return redirect(url_for('index_bp.index'))

@index_bp.route('/register', methods=['POST'])
def register_user():
    # 从请求中获取表单信息
    username = request.form['username']
    password1 = request.form['password1']
    password2 = request.form['password2']
    passkey = request.form['passkey']
    # 判断用户名是否为空
    if username:
        # 判断密码是否为空
        if password1:
            if password2:
                # 判断密钥是否为空
                if passkey:
                    # 判断两次输入的密码是否一样
                    if password1 == password2:
                        # 获取可以密钥列表
                        key = secret_key()
                        # 判断密钥是否相等
                        if passkey in key:
                            # 更新密钥状态
                            update_status(passkey)
                            add_user(username, bcrypt_hash(password1))
                            flash('注册成功！', 'success')
                        else:
                            flash('请输入正确的密钥！如没有请与开发者联系', 'error')
                    else:
                        flash('两次密码不相等！', 'error')
                else:
                    flash('密钥不能为空！', 'error')
            else:
                flash('密码不能为空！', 'error')
        else:
            flash('密码不能为空！', 'error')
    else:
        flash('用户名不能为空！', 'error')
    return redirect(url_for('index_bp.login'))

@index_bp.route('/update-signature', methods=['POST'])
def update_signature():
    if 'username' in session:
        new_signature = request.form['signature']
        if len(new_signature) > 255:
            flash('签名长度不能超过255个字符！', 'error')
            return redirect(url_for('index_bp.mine'))
        else:
            updata_signature_service(session['username'], new_signature)
            flash('修改成功，请刷新！', 'success')
            return redirect(url_for('index_bp.mine'))
    else:
        return redirect(url_for('index_bp.login'))

@index_bp.route('/update-username', methods=['POST'])
def update_username():
    if 'username' in session:
        new_username = request.form['username']
        if new_username:
            if len(new_username) > 255:
                flash('用户名长度不能超过255个字符！', 'error')
                return redirect(url_for('index_bp.mine'))
            else:
                update_username_service(session['username'], new_username)
                flash('修改成功，请重新登录！', 'success')
                return redirect(url_for('index_bp.logout'))
        else:
            flash('用户名不能为空！', 'error')
    else:
        return redirect(url_for('index_bp.login'))

@index_bp.route('/update-password', methods=['POST'])
def update_password():
    if 'username' in session:
        raw_password = request.form['raw_password']
        new_password1 = request.form['new_password1']
        new_password2 = request.form['new_password2']
        user = get_user(session['username'])
        if raw_password:
            if new_password1:
                if new_password2:
                    if bcrypt_verify(raw_password, user['password']):
                        if new_password1 != raw_password:
                            if len(new_password1) <= 20 and len(new_password2) <= 20:
                                if new_password1 == new_password2:
                                    print(session['username'])
                                    print(bcrypt_hash(new_password1))
                                    update_password_service(session['username'], bcrypt_hash(new_password1))
                                    flash('修改成功，请重新登录！', 'success')
                                    return redirect(url_for('index_bp.logout'))
                                else:
                                    flash('两次密码不相等，请重新输入！', 'error')
                                    return redirect(url_for('index_bp.mine'))
                            else:
                                flash('新密码长度不能超过20个字符，请重新输入！', 'error')
                                return redirect(url_for('index_bp.mine'))
                        else:
                            flash('新密码与旧密码重复，请重新输入！', 'error')
                            return redirect(url_for('index_bp.mine'))
                    else:
                        flash('旧密码错误，请重新输入！', 'error')
                        return redirect(url_for('index_bp.mine'))
                else:
                    flash('密码不能为空，请重新输入！', 'error')
                    return redirect(url_for('index_bp.mine'))
            else:
                flash('密码不能为空，请重新输入！', 'error')
                return redirect(url_for('index_bp.mine'))
        else:
            flash('密码不能为空，请重新输入！', 'error')
            return redirect(url_for('index_bp.mine'))
    else:
        return redirect(url_for('index_bp.login'))




