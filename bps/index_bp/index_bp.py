import urllib

from flask import Blueprint, render_template, request, redirect, url_for, session, g, flash
from bps.index_bp.service.user_service import get_user
from bps.index_bp.utils.bcrypt_util import bcrypt_hash, bcrypt_verify
from bps.index_bp.service.user_service import secret_key, update_status, add_user, updata_signature_service, update_username_service, update_password_service
import os
import datetime
import math
from bps.admin_bp.utils.util import get_client_ip, get_device_info
from bps.admin_bp.service.dashboard_service import insert_login_log_service

index_bp = Blueprint('index_bp', __name__)




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


# 文件路径：bps/index_bp/index_bp.py
# 只替换down路由部分，其他代码保持不变

@index_bp.route('/down', methods=['GET'])
@index_bp.route('/down/<path:subpath>', methods=['GET'])
def down(subpath=''):
    if 'username' not in session:
        return redirect(f'/login?next={request.path}', code=302)

    # ✅ 修复：统一处理路径末尾斜杠问题
    DOWNLOAD_ROOT = '/www/wwwroot/qingyuweb/downloads'
    # 确保根目录路径标准化，没有末尾斜杠
    DOWNLOAD_ROOT = os.path.normpath(DOWNLOAD_ROOT)
    NGINX_PREFIX = '/downloads'

    # 支持预览的图片扩展名
    IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg'}

    files = []
    folders = []
    error_msg = None
    current_path = subpath

    try:
        # 解码URL路径
        subpath = urllib.parse.unquote(subpath)

        # ✅ 修复：根目录特殊处理
        if not subpath or subpath == '/':
            full_path = DOWNLOAD_ROOT
        else:
            # 安全拼接路径
            full_path = os.path.normpath(os.path.join(DOWNLOAD_ROOT, subpath))

            # ✅ 修复：路径安全检查（更严格更准确）
            if not full_path.startswith(DOWNLOAD_ROOT + os.sep) and full_path != DOWNLOAD_ROOT:
                error_msg = '非法路径访问！'
                # ❌ 不要重定向，直接渲染模板，避免无限循环
                return render_template('bp/index_bp/down.html',
                                       username=session['username'],
                                       folders=[],
                                       files=[],
                                       error_msg=error_msg,
                                       current_path='',
                                       breadcrumbs=[],
                                       is_root=True)

        # 检查路径是否存在
        if not os.path.exists(full_path):
            error_msg = '目录不存在！'
            return render_template('bp/index_bp/down.html',
                                   username=session['username'],
                                   folders=[],
                                   files=[],
                                   error_msg=error_msg,
                                   current_path='',
                                   breadcrumbs=[],
                                   is_root=True)

        # 检查是否是目录
        if not os.path.isdir(full_path):
            error_msg = '这不是一个目录！'
            return render_template('bp/index_bp/down.html',
                                   username=session['username'],
                                   folders=[],
                                   files=[],
                                   error_msg=error_msg,
                                   current_path='',
                                   breadcrumbs=[],
                                   is_root=True)

        # 遍历目录内容
        for entry in os.listdir(full_path):
            entry_path = os.path.join(full_path, entry)

            # 跳过隐藏文件和文件夹
            if entry.startswith('.'):
                continue

            stat_info = os.stat(entry_path)
            mtime_timestamp = stat_info.st_mtime
            mtime_str = datetime.datetime.fromtimestamp(mtime_timestamp).strftime('%Y-%m-%d %H:%M')

            if os.path.isdir(entry_path):
                # 处理文件夹
                folder_url = f'/down/{subpath}/{entry}' if subpath else f'/down/{entry}'
                folders.append({
                    'name': entry,
                    'mtime_str': mtime_str,
                    'url': folder_url
                })
            else:
                # 处理文件
                size_bytes = stat_info.st_size
                if size_bytes == 0:
                    size_str = "0 B"
                else:
                    k = 1024
                    sizes = ['B', 'KB', 'MB', 'GB', 'TB']
                    i = int(math.log(size_bytes, k))
                    size_str = f"{round(size_bytes / (k ** i), 2)} {sizes[i]}"

                # 构建文件URL
                file_url = f'{NGINX_PREFIX}/{subpath}/{entry}' if subpath else f'{NGINX_PREFIX}/{entry}'

                # 判断文件类型
                file_ext = entry.split('.')[-1].lower() if '.' in entry else ''
                is_image = file_ext in IMAGE_EXTENSIONS

                # 获取文件图标类型
                if is_image:
                    icon_type = 'image'
                elif file_ext in {'zip', 'rar', '7z', 'tar', 'gz', 'bz2'}:
                    icon_type = 'archive'
                elif file_ext in {'pdf'}:
                    icon_type = 'pdf'
                elif file_ext in {'doc', 'docx'}:
                    icon_type = 'word'
                elif file_ext in {'xls', 'xlsx'}:
                    icon_type = 'excel'
                elif file_ext in {'ppt', 'pptx'}:
                    icon_type = 'powerpoint'
                elif file_ext in {'txt', 'md', 'json', 'xml', 'html', 'css', 'js', 'py', 'java', 'c', 'cpp'}:
                    icon_type = 'text'
                elif file_ext in {'exe', 'msi', 'deb', 'rpm'}:
                    icon_type = 'executable'
                elif file_ext in {'mp3', 'wav', 'flac', 'aac', 'ogg'}:
                    icon_type = 'audio'
                elif file_ext in {'mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv'}:
                    icon_type = 'video'
                else:
                    icon_type = 'default'

                files.append({
                    'name': entry,
                    'size_str': size_str,
                    'mtime_str': mtime_str,
                    'url': file_url,
                    'is_image': is_image,
                    'icon_type': icon_type
                })

        # 排序：文件夹在前，文件在后；都按修改时间倒序
        folders.sort(key=lambda x: x['mtime_str'], reverse=True)
        files.sort(key=lambda x: x['mtime_str'], reverse=True)

    except Exception as e:
        error_msg = f'加载目录失败: {str(e)}'
        # 发生异常时也直接渲染模板，不重定向
        return render_template('bp/index_bp/down.html',
                               username=session['username'],
                               folders=[],
                               files=[],
                               error_msg=error_msg,
                               current_path='',
                               breadcrumbs=[],
                               is_root=True)

    # 构建面包屑导航
    breadcrumbs = []
    if subpath:
        parts = subpath.split('/')
        current_breadcrumb = ''
        for part in parts:
            if part:
                current_breadcrumb += f'/{part}'
                breadcrumbs.append({
                    'name': part,
                    'url': f'/down{current_breadcrumb}'
                })

    return render_template('bp/index_bp/down.html',
                           username=session['username'],
                           folders=folders,
                           files=files,
                           error_msg=error_msg,
                           current_path=current_path,
                           breadcrumbs=breadcrumbs,
                           is_root=(subpath == ''))


@index_bp.route('/about')
def about():
    if 'username' in session:
        return render_template('bp/index_bp/about.html', username = session['username'])
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
                        insert_login_log_service(user['id'], user['username'], get_client_ip(request), get_device_info(request))
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