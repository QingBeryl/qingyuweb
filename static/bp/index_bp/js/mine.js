const $ = s => document.querySelector(s);
const closeModal = m => m.style.display = 'none';

// 自动隐藏flash消息
setTimeout(() => {
    document.querySelectorAll('.flash-message').forEach(msg => {
        msg.style.opacity = '0';
        setTimeout(() => msg.remove(), 300);
    });
}, 3000);

// ✅ 修复：通用表单提交函数（直接提交到主窗口，让后端处理重定向）
function submitForm(action, data) {
    // 创建临时表单
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = action;

    // 添加表单字段
    for (const key in data) {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = key;
        input.value = data[key];
        form.appendChild(input);
    }

    // 添加到页面并提交
    document.body.appendChild(form);
    form.submit();
}

// 1. 头像上传 + 预览
$('#avatarContainer').onclick = () => $('#avatarInput').click();
$('#avatarInput').onchange = e => {
    const f = e.target.files[0];
    if(!f || !f.type.startsWith('image/')) return alert('请选择图片');
    if(f.size > 2*1024*1024) return alert('图片最大2MB');

    // 预览
    new FileReader().onload = r => $('#avatar').innerHTML = `<img src="${r.target.result}">`;
    new FileReader().readAsDataURL(f);

    // 上传
    const fd = new FormData();
    fd.append('avatar', f);
    fetch(window.API_URLS.upload_avatar, {method: 'POST', body: fd})
    .then(() => location.reload());
};

// 2. 编辑签名
const sigModal = $('#signatureModal'), sigInp = $('#signatureInput'), sigCount = $('#signatureCharCount');
sigCount.innerText = sigInp.value.length;
sigInp.oninput = () => sigCount.innerText = sigInp.value.length;

$('#editSignatureBtn').onclick = () => {
    sigInp.value = $('#signatureDisplay').innerText;
    sigCount.innerText = sigInp.value.length;
    sigModal.style.display = 'block';
};

$('#saveSignatureBtn').onclick = () => {
    const signature = sigInp.value.trim();
    if (!signature) {
        alert('签名不能为空');
        return;
    }
    if (signature.length > 255) {
        alert('签名长度不能超过255个字符');
        return;
    }

    submitForm(window.API_URLS.update_signature, {
        signature: signature
    });
};

// 3. 修改用户名
const userModal = $('#usernameModal'), userInp = $('#usernameInput');

$('#editUsernameItem').onclick = () => {
    userInp.value = $('#usernameDisplay').innerText;
    userModal.style.display = 'block';
};

$('#saveUsernameBtn').onclick = () => {
    const username = userInp.value.trim();
    if (!username) {
        alert('用户名不能为空');
        return;
    }
    if (username.length > 255) {
        alert('用户名长度不能超过255个字符');
        return;
    }

    submitForm(window.API_URLS.update_username, {
        username: username
    });
};

// 4. 修改密码
const pwdModal = $('#passwordModal'),
      oldPwd = $('#oldPasswordInput'),
      newPwd = $('#newPasswordInput'),
      rePwd = $('#confirmPasswordInput');

$('#changePasswordItem').onclick = () => {
    oldPwd.value = newPwd.value = rePwd.value = '';
    pwdModal.style.display = 'block';
};

$('#savePasswordBtn').onclick = () => {
    const raw_password = oldPwd.value;
    const new_password1 = newPwd.value;
    const new_password2 = rePwd.value;

    if (!raw_password || !new_password1 || !new_password2) {
        alert('请填写所有密码字段');
        return;
    }

    if (new_password1 !== new_password2) {
        alert('两次输入的密码不一致');
        return;
    }

    if (new_password1.length > 20) {
        alert('新密码长度不能超过20个字符');
        return;
    }

    submitForm(window.API_URLS.update_password, {
        raw_password: raw_password,
        new_password1: new_password1,
        new_password2: new_password2
    });
};

// 5. 通用关闭弹窗
document.querySelectorAll('.close,.cancel').forEach(el => {
    el.onclick = () => document.querySelectorAll('.modal').forEach(m => closeModal(m));
});
window.onclick = e => e.target.classList.contains('modal') && closeModal(e.target);