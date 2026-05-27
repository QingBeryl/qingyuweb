// 卡片跳转
function sfsCardLink() {
  window.location.href = sfscardUrl; // 这里改成你卡片的链接
}

// 按钮跳转（独立，不被覆盖）
function sfsBtnLink(e) {
  e.stopPropagation(); // 阻止冒泡，核心！
  window.location.href = sfsbtnUrl; // 这里可以写死，或者用 Flask 路由
}


// 卡片跳转
function attCardLink() {
  window.location.href = attcardUrl; // 这里改成你卡片的链接
}

// 按钮跳转（独立，不被覆盖）
function attBtnLink(e) {
  e.stopPropagation(); // 阻止冒泡，核心！
  window.location.href = attbtnUrl; // 这里可以写死，或者用 Flask 路由
}