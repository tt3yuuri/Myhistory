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


// 投稿フォームで送信したときの処理

document.getElementById('album-post-form').addEventListener('submit', function(e) {
    e.preventDefault(); // ページのリロードを防ぐ

    const iconType = Math.random() > 0.5 ? 'fa-solid' : 'fa-regular';

    // 1. 入力された値を取得
    const title = document.getElementById('albumTitle').value;
    const name = document.getElementById('nickname').value;
    //const description = document.getElementById('albumDescription').value;
    const imageFile = document.getElementById('albumImage').files[0];

    // 2. 次のカードが「左」か「右」か判断する
    // 現在のカードの数を数えて、偶数なら左、奇数なら右にする
    const container = document.querySelector('.timeline-container');
    const existingNodes = container.querySelectorAll('.timeline-node');
    const side = existingNodes.length % 2 === 0 ? 'left' : 'right';

    // 3. 画像の処理（一時的なURLを作成）
    let imageUrl = 'https://via.placeholder.com/300x200?text=No+Image'; // 画像がない時の代わり
    if (imageFile) {
        imageUrl = URL.createObjectURL(imageFile); // 選択した画像を一時的に表示可能なURLに変換
    }

    // 4. 新しいタイムラインノード（HTML）を組み立てる
    const newNode = document.createElement('div');
    newNode.className = `timeline-node ${side}`;
    
    newNode.innerHTML = `
        <div class="timeline-card card shadow-sm">
            <img src="${imageUrl}" class="card-img-top" alt="${title}">
            <div class="card-body">
                <h5 class="card-title text-center mb-3">
                    <i class="fa-regular fa-snowflake snowflake-icon"></i>
                    ${title}
                    <i class="fa-regular fa-snowflake snowflake-icon"></i>
                </h5>
                <h6 class="card-subtitle mb-2 text-muted">by ${name}</h6>
            </div>
        </div>
    `;

    // 5. タイムラインの最後（フォームよりは上）に追加する
    // 終了マーカー（end-marker）の直前に挿入するのが綺麗です
    const endMarker = container.querySelector('.end-marker');
    container.insertBefore(newNode, endMarker);

    // 6. フォームを空にする
    this.reset();


    // 7. 完了メッセージ（アラート）
    alert('アルバムを一時的に追加しました！(リロードすると消えます)');
});