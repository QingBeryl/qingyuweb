// 项目中心功能：搜索(回车/按钮触发) + 分类筛选 + 加载更多
document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('projectSearch');
    const searchBtn = document.getElementById('searchBtn');
    const categoryTags = document.getElementById('categoryTags');
    const projectGrid = document.getElementById('projectGrid');
    const loadMoreBtn = document.getElementById('loadMoreBtn');

    if (!searchInput || !categoryTags || !projectGrid || !loadMoreBtn) return;

    let currentCategory = 'all';
    let currentSearch = '';
    const visibleCount = 12;
    let totalVisible = visibleCount;

    // ======================================
    // 🔥 搜索触发：点击按钮 + 按回车
    // ======================================
    function doSearch() {
        currentSearch = searchInput.value.toLowerCase().trim();
        filterProjects();
    }

    // 点击搜索按钮触发
    searchBtn.addEventListener('click', doSearch);

    // 回车触发搜索
    searchInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter') {
            doSearch();
        }
    });

    // ======================================
    // 分类筛选（保持点击实时生效）
    // ======================================
    document.addEventListener('click', function (e) {
        const tag = e.target.closest('.category-tags .tag');
        if (!tag) return;

        document.querySelectorAll('.category-tags .tag').forEach(t => t.classList.remove('active'));
        tag.classList.add('active');
        currentCategory = tag.dataset.category;
        filterProjects();
    });

    // ======================================
    // 加载更多
    // ======================================
    loadMoreBtn.addEventListener('click', function () {
        totalVisible += visibleCount;
        filterProjects();
    });

    // ======================================
    // 筛选逻辑
    // ======================================
    function filterProjects() {
        const cards = projectGrid.querySelectorAll('.project-card');
        let matchCount = 0;

        cards.forEach((card, index) => {
            const title = card.querySelector('.card-title')?.textContent.toLowerCase() || '';
            const desc = card.querySelector('.card-desc')?.textContent.toLowerCase() || '';
            const category = card.dataset.category || '';

            let tagMatch = false;
            card.querySelectorAll('.tag-small').forEach(t => {
                if (t.textContent.toLowerCase().includes(currentSearch)) tagMatch = true;
            });

            const show =
                (title.includes(currentSearch) || desc.includes(currentSearch) || tagMatch) &&
                (currentCategory === 'all' || category === currentCategory) &&
                index < totalVisible;

            card.style.display = show ? 'flex' : 'none';
            if (show) matchCount++;
        });

        loadMoreBtn.style.display = (matchCount >= totalVisible && matchCount < cards.length)
            ? 'inline-block'
            : 'none';
    }

    // 初始化
    filterProjects();
});