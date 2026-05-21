const container = document.querySelector('#container');
const signInButton = document.querySelector('#signIn');
const signUpButton = document.querySelector('#signUp');

signUpButton.addEventListener('click',() => container.classList.add('right-pannrl-active'))
signInButton.addEventListener('click',() => container.classList.remove('right-pannrl-active'))







document.addEventListener('DOMContentLoaded', function() {
    const overlay = document.getElementById('flashOverlay');
    const closeBtn = document.getElementById('flashClose');

    if (overlay) {
        // 显示弹窗
        setTimeout(() => {
            overlay.classList.add('show');
        }, 100);

        // 自动关闭（3秒后）
        const autoCloseTimer = setTimeout(() => {
            closeFlash();
        }, 3000);

        // 点击关闭按钮
        closeBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            closeFlash();
            clearTimeout(autoCloseTimer);
        });

        // 点击遮罩层关闭
        overlay.addEventListener('click', function(e) {
            if (e.target === overlay) {
                closeFlash();
                clearTimeout(autoCloseTimer);
            }
        });

        // 关闭函数
        function closeFlash() {
            overlay.classList.remove('show');
            setTimeout(() => {
                overlay.remove();
            }, 300);
        }
    }
});