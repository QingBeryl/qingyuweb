// 卡片跳转
function goCardLink() {
  window.location.href = cardUrl; // 这里改成你卡片的链接
}

// 按钮跳转（独立，不被覆盖）
function goBtnLink(e) {
  e.stopPropagation(); // 阻止冒泡，核心！
  window.location.href = btnUrl; // 这里可以写死，或者用 Flask 路由
}