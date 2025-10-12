const bgms = document.querySelectorAll(".bgm");
const toggleButtons = document.querySelectorAll(".bgm-toggle");

toggleButtons.forEach((button, index) => {
  let isPlaying = false;

  button.addEventListener("click", () => {
    // まず全BGM停止（排他再生）
    bgms.forEach((bgm, i) => {
      bgm.pause();
      bgm.currentTime = 0;
      toggleButtons[i].textContent = "▶";
    });

    if (!isPlaying) {
      bgms[index].play();
      button.textContent = "■";
    } else {
      bgms[index].pause();
      button.textContent = "▶";
    }

    isPlaying = !isPlaying;
  });
});
