let imageURLs = [
    "images/mannami.jpg",
    "images/takaya.jpg",
    "images/yanagi.jpg",
    // ... 他の画像のURL ...
];
let currentIndex = 0;
let currentImageElement = document.getElementById("currentImage");
let prevImageElement = document.getElementById("prevImage");
let nextImageElement = document.getElementById("nextImage");

function updateImages() {
    currentImageElement.src = imageURLs[currentIndex];

    let prevIndex = (currentIndex - 1 + imageURLs.length) % imageURLs.length;
    let nextIndex = (currentIndex + 1) % imageURLs.length;

    prevImageElement.src = imageURLs[prevIndex];
    nextImageElement.src = imageURLs[nextIndex];
}

function showPrev() {
    currentIndex = (currentIndex - 1 + imageURLs.length) % imageURLs.length;
    updateImages();
}

function showNext() {
    currentIndex = (currentIndex + 1) % imageURLs.length;
    updateImages();
}

// 最初の画像を表示
updateImages();