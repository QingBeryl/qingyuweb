const slides = document.querySelectorAll('.slide');
const progressBar = document.getElementById('progress-bar');
const pageNumber = document.getElementById('page-number');
let currentPage = 0;
const totalPages = slides.length;

// 更新视图
function updateView() {
  slides.forEach((s, idx) => {
    s.classList.toggle('active', idx === currentPage);
  });
  // 进度条
  progressBar.style.width = `${((currentPage+1)/totalPages)*100}%`;
  // 页码
  pageNumber.innerText = `${String(currentPage+1).padStart(2,'0')} / ${totalPages}`;

  // 如果是视频页，自动加载视频
  if (currentPage === slides.length - 2) {
    if (videoPlayer && videoPlayer.src === '') {
      loadCurrentVideo();
    }
  } else {
    // 离开视频页暂停视频
    if (videoPlayer) videoPlayer.pause();
  }
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

// 键盘监听
document.addEventListener('keydown', e => {
  if(e.key === 'ArrowRight' || e.key === ' ') nextPage();
  if(e.key === 'ArrowLeft') prevPage();
});

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

// 视频页滚轮切换
document.querySelector('.slide:nth-last-child(2)').addEventListener('wheel', (e) => {
  if (currentPage !== slides.length - 2) return;
  e.preventDefault();
  if (e.deltaY > 0) {
    switchVideo('next');
  } else {
    switchVideo('prev');
  }
});

updateView();