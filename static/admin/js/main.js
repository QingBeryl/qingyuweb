// 编辑用户模态框
function openEditModal(userId, username, signature) {
    document.getElementById('edit-username').value = username;
    document.getElementById('edit-signature').value = signature;
    document.getElementById('edit-password').value = '';
    document.getElementById('editForm').action = '/admin/user/edit/' + userId;
    document.getElementById('editModal').classList.add('show');
}

function closeModal() {
    document.getElementById('editModal').classList.remove('show');
}

// 点击模态框外部关闭
window.onclick = function(event) {
    const modal = document.getElementById('editModal');
    if (event.target == modal) {
        closeModal();
    }
}