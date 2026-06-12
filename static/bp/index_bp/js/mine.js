    // 编辑签名模态框
    function openSignatureModal() {
        document.getElementById('signatureModal').style.display = 'flex';
    }

    function closeSignatureModal() {
        document.getElementById('signatureModal').style.display = 'none';
    }

    // 修改用户名模态框
    function openUsernameModal() {
        document.getElementById('usernameModal').style.display = 'flex';
    }

    function closeUsernameModal() {
        document.getElementById('usernameModal').style.display = 'none';
    }

    // 修改密码模态框
    function openPasswordModal() {
        document.getElementById('passwordModal').style.display = 'flex';
    }

    function closePasswordModal() {
        document.getElementById('passwordModal').style.display = 'none';
    }

    // 点击模态框外部关闭
    window.onclick = function(event) {
        if (event.target.id === 'signatureModal') {
            closeSignatureModal();
        }
        if (event.target.id === 'usernameModal') {
            closeUsernameModal();
        }
        if (event.target.id === 'passwordModal') {
            closePasswordModal();
        }
    }