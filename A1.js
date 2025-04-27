const displayImage = document.getElementById("displayImage");
const prevButton = document.getElementById("prevButton");
const nextButton = document.getElementById("nextButton");

const images = ["images/mannami.jpg", "images/takaya.jpg", "images/yanagi.jpg"]; // 画像のファイル名を配列で管理
let currentIndex = 0;

function updateImage() {
    displayImage.src = images[currentIndex];
}

prevButton.addEventListener('click', () => {
    currentIndex--;
    if (currentIndex < 0) {
        currentIndex = images.length - 1; // 最初に戻る
    }
    updateImage();
});

nextButton.addEventListener('click', () => {
    currentIndex++;
    if (currentIndex >= images.length) {
        currentIndex = 0; // 最後に戻る
    }
    updateImage();
});

// 初期表示
updateImage();