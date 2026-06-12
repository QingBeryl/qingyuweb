// 刷新按钮
document.getElementById('refreshBtn').addEventListener('click', function() {
    window.location.reload();
});

// 图片预览功能
const modal = document.getElementById('imageModal');
const modalImage = document.getElementById('modalImage');
const modalTitle = document.getElementById('modalTitle');
const modalDownload = document.getElementById('modalDownload');
const closeModal = document.getElementById('closeModal');

// 所有预览按钮
document.querySelectorAll('.preview-btn').forEach(btn => {
    btn.addEventListener('click', function() {
        const url = this.getAttribute('data-url');
        const name = this.getAttribute('data-name');

        modalImage.src = url;
        modalTitle.textContent = name;
        modalDownload.href = url;
        modalDownload.download = name;

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    });
});

// 关闭模态框
function closeImageModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

closeModal.addEventListener('click', closeImageModal);

// 点击模态框背景关闭
modal.addEventListener('click', function(e) {
    if (e.target === modal) {
        closeImageModal();
    }
});

// 按ESC键关闭
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeImageModal();
    }
});