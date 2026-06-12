// 标签页切换功能
document.addEventListener('DOMContentLoaded', function() {
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    let currentTabIndex = 0;

    tabButtons.forEach((button, index) => {
        button.addEventListener('click', function() {
            const targetTabId = this.getAttribute('data-tab');
            const targetTab = document.getElementById(targetTabId);

            // 如果点击的是当前标签，不做任何操作
            if (this.classList.contains('active')) {
                return;
            }

            // 移除所有按钮的active类
            tabButtons.forEach(btn => btn.classList.remove('active'));
            // 给当前点击的按钮添加active类
            this.classList.add('active');

            // 确定切换方向
            const direction = index > currentTabIndex ? 'right' : 'left';

            // 移除所有内容的active和prev类
            tabContents.forEach(content => {
                content.classList.remove('active');
                content.classList.remove('prev');
            });

            // 设置前一个标签的类
            if (direction === 'right') {
                tabContents[currentTabIndex].classList.add('prev');
            } else {
                targetTab.classList.add('prev');
                // 强制重绘
                void targetTab.offsetWidth;
                targetTab.classList.remove('prev');
            }

            // 给目标标签添加active类
            setTimeout(() => {
                targetTab.classList.add('active');
            }, direction === 'left' ? 10 : 0);

            // 更新当前标签索引
            currentTabIndex = index;
        });
    });

    // 修复邮箱链接
    const emailLink = document.querySelector('a[href="2045660167@qq.com"]');
    if (emailLink) {
        emailLink.href = 'mailto:2045660167@qq.com';
    }
});