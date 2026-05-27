const slides = document.querySelectorAll('.slide');
const progressBar = document.getElementById('progress-bar');
const pageNumber = document.getElementById('page-number');
let currentPage = 0;
const totalPages = slides.length; // 动态计算总页数


let currentImage = 0;
const gallerySlide = document.getElementById('gallery-slide');
const galleryImage1 = document.getElementById('gallery-image-1');
const galleryImage2 = document.getElementById('gallery-image-2');
const galleryCaption = document.getElementById('gallery-caption');
const galleryPagination = document.getElementById('gallery-pagination');
let isAnimating = false; // 防止动画过程中重复触发
let currentImageElement = galleryImage1; // 当前显示的图片元素
let nextImageElement = galleryImage2; // 下一个要显示的图片元素

// 更新视图
function updateView() {
  slides.forEach((s, idx) => {
    s.classList.toggle('active', idx === currentPage);
  });
  // 进度条
  progressBar.style.width = `${((currentPage+1)/totalPages)*100}%`;
  // 页码
  pageNumber.innerText = `${String(currentPage+1).padStart(2,'0')} / ${totalPages}`;

  // 如果是图片画廊页，更新图片
  if (currentPage === slides.length - 2) { // 图片画廊页是倒数第二页
    updateGallery();
  }
}

// 更新图片画廊
function updateGallery() {
  currentImageElement.src = imageGallery[currentImage].src;
  galleryCaption.textContent = imageGallery[currentImage].caption;
  galleryPagination.textContent = `${String(currentImage+1).padStart(2,'0')} / ${imageGallery.length}`;
}

// 下一页
function nextPage() {
  if(currentPage < totalPages - 1) {
    currentPage++;
    updateView();
  }
}
// 上一页
function prevPage() {
  if(currentPage > 0) {
    currentPage--;
    updateView();
  }
}

// 切换图片
function switchImage(direction) {
  if (isAnimating) return;
  isAnimating = true;

  let newIndex;
  if (direction === 'down') {
    newIndex = (currentImage + 1) % imageGallery.length;
    nextImageElement.style.transform = 'translateY(100%)';
  } else {
    newIndex = (currentImage - 1 + imageGallery.length) % imageGallery.length;
    nextImageElement.style.transform = 'translateY(-100%)';
  }

  // 设置下一张图片的源
  nextImageElement.src = imageGallery[newIndex].src;

  // 触发重排
  void nextImageElement.offsetWidth;

  // 开始动画
  currentImageElement.style.transform = direction === 'down' ? 'translateY(-100%)' : 'translateY(100%)';
  nextImageElement.style.transform = 'translateY(0)';

  setTimeout(() => {
    // 动画结束后更新状态
    currentImage = newIndex;
    galleryCaption.textContent = imageGallery[currentImage].caption;
    galleryPagination.textContent = `${String(currentImage+1).padStart(2,'0')} / ${imageGallery.length}`;

    // 交换当前和下一个图片元素的角色
    [currentImageElement, nextImageElement] = [nextImageElement, currentImageElement];
    isAnimating = false;
  }, 500);
}

// 键盘监听
document.addEventListener('keydown', e => {
  // 如果当前是图片画廊页
  if (currentPage === slides.length - 2) {
    if (e.key === 'ArrowRight' || e.key === ' ') {
      nextPage(); // 右箭头和空格翻页
    } else if (e.key === 'ArrowLeft') {
      prevPage(); // 左箭头翻页
    }
    // 移除上下箭头的处理
  } else {
    // 普通页面，处理左右箭头和空格翻页
    if(e.key === 'ArrowRight' || e.key === ' ') nextPage();
    if(e.key === 'ArrowLeft') prevPage();
  }
});

// 鼠标滚轮监听
gallerySlide.addEventListener('wheel', (e) => {
  e.preventDefault(); // 阻止页面滚动
  if (e.deltaY > 0) {
    // 向下滚动，下一张图片
    switchImage('down');
  } else {
    // 向上滚动，上一张图片
    switchImage('up');
  }
});

updateView();

// ====================== 视频播放逻辑 ======================
const videoPlayer = document.getElementById('video-player');
const videoPagination = document.getElementById('video-pagination');
let currentVideoIndex = 0;

// 加载当前视频
function loadCurrentVideo() {
  if (!videoPlayer) return;
  videoPlayer.src = videoList[currentVideoIndex].src;
  videoPagination.textContent = `${String(currentVideoIndex + 1).padStart(2, '0')} / ${String(videoList.length).padStart(2, '0')}`;
  videoPlayer.preload = "auto";
  videoPlayer.load();
}

// 视频页切换上一个/下一个
function switchVideo(direction) {
  if (direction === 'next') {
    currentVideoIndex = (currentVideoIndex + 1) % videoList.length;
  } else {
    currentVideoIndex = (currentVideoIndex - 1 + videoList.length) % videoList.length;
  }
  loadCurrentVideo();
}

// 进入视频页自动加载第一个视频
const originalUpdateView = updateView;
function newUpdateView() {
  originalUpdateView();
  // 视频页是倒数第三页
  if (currentPage === slides.length - 3) {
    if (videoPlayer && videoPlayer.src === '') {
      loadCurrentVideo();
    }
  } else {
    // 离开视频页暂停视频
    if (videoPlayer) videoPlayer.pause();
  }
}
updateView = newUpdateView;

// 视频页滚轮切换
document.querySelector('.slide:nth-last-child(3)').addEventListener('wheel', (e) => {
  if (currentPage !== slides.length - 3) return;
  e.preventDefault();
  if (e.deltaY > 0) {
    switchVideo('next');
  } else {
    switchVideo('prev');
  }
});