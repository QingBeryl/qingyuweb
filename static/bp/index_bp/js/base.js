document.addEventListener('DOMContentLoaded', function() {
    // ==============================
    // Flash弹窗功能（保持不变）
    // ==============================
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

    // ==============================
    // 汉堡菜单功能
    // ==============================
    const hamburger = document.getElementById('hamburger');
    const mobileMenu = document.getElementById('mobileMenu');

    // 创建菜单遮罩层
    const menuOverlay = document.createElement('div');
    menuOverlay.className = 'menu-overlay';
    document.body.appendChild(menuOverlay);

    // 切换菜单显示/隐藏
    function toggleMenu() {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        menuOverlay.classList.toggle('active');
        // 禁止页面滚动
        document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
    }

    // 关闭菜单
    function closeMenu() {
        hamburger.classList.remove('active');
        mobileMenu.classList.remove('active');
        menuOverlay.classList.remove('active');
        document.body.style.overflow = '';
    }

    // 汉堡按钮点击事件
    hamburger.addEventListener('click', toggleMenu);

    // 遮罩层点击关闭菜单
    menuOverlay.addEventListener('click', closeMenu);

    // 点击菜单项关闭菜单
    const mobileLinks = document.querySelectorAll('.mobile-navlist a');
    mobileLinks.forEach(link => {
        link.addEventListener('click', closeMenu);
    });

    // 窗口大小变化时关闭菜单
    window.addEventListener('resize', function() {
        if (window.innerWidth > 480) {
            closeMenu();
        }
    });
});