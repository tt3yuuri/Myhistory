// script.js
document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const imagePreviews = document.getElementById('imagePreviews');
    const createAlbumBtn = document.getElementById('createAlbumBtn');
    let selectedFiles = [];

    // 1. ユーザーが8枚の画像を選ぶ
    imageUpload.addEventListener('change', (event) => {
        selectedFiles = Array.from(event.target.files);
        imagePreviews.innerHTML = ''; // 既存のプレビューをクリア

        if (selectedFiles.length === 8) {
            createAlbumBtn.disabled = false; // 8枚選択されたらボタンを有効化
            selectedFiles.forEach((file, index) => {
                const reader = new FileReader();
                reader.onload = (e) => {
                    const imgContainer = document.createElement('div');
                    imgContainer.classList.add('image-item');
                    const img = document.createElement('img');
                    img.src = e.target.result;
                    img.alt = `画像 ${index + 1}`;
                    const p = document.createElement('p');
                    p.textContent = `選択順: ${index + 1}`; // 選択された順番を表示
                    imgContainer.appendChild(img);
                    imgContainer.appendChild(p);
                    imagePreviews.appendChild(imgContainer);
                };
                reader.readAsDataURL(file);
            });
        } else {
            createAlbumBtn.disabled = true; // 8枚でなければ無効化
            alert('画像を8枚選択してください。');
        }
    });

    // アルバム作成ボタンがクリックされた時の処理
    createAlbumBtn.addEventListener('click', async () => {
        if (selectedFiles.length !== 8) {
            alert('画像を8枚選択してください。');
            return;
        }

        const formData = new FormData();
        selectedFiles.forEach((file, index) => {
            formData.append(`image_${index + 1}`, file); // ファイルを順番に付加
        });

        // 2. このサイト内で画像サイズを調整する
        // 3. 画像が1で選択された順番に、名前を付ける。
        // これらの処理はバックエンド（Python）で行うため、JavaScriptからリクエストを送信します。
        try {
            const response = await fetch('/create_album', { // Pythonバックエンドへのエンドポイント
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                alert('アルバムが正常に作成されました！');
                console.log('サーバーからの応答:', result);
                // 必要に応じて、作成されたアルバムへのリンクなどを表示
            } else {
                alert('アルバム作成中にエラーが発生しました。');
                const errorText = await response.text();
                console.error('サーバーエラー:', errorText);
            }
        } catch (error) {
            console.error('ネットワークエラー:', error);
            alert('ネットワークエラーが発生しました。');
        }
    });
});