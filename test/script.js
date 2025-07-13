// script.js
document.addEventListener('DOMContentLoaded', () => {
    const imageUpload = document.getElementById('imageUpload');
    const imagePreviews = document.getElementById('imagePreviews');
    const createAlbumBtn = document.getElementById('createAlbumBtn');
    const viewAlbumSection = document.getElementById('viewAlbumSection'); // 新しく追加
    const viewAlbumBtn = document.getElementById('viewAlbumBtn');       // 新しく追加

    let selectedFiles = [];

    // ユーザーが8枚の画像を選ぶ
    imageUpload.addEventListener('change', (event) => {
        selectedFiles = Array.from(event.target.files);
        imagePreviews.innerHTML = ''; // 既存のプレビューをクリア
        viewAlbumSection.style.display = 'none'; // 新しい画像を選択したらボタンを非表示にする

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

        // ボタンを無効化して多重送信を防ぐ
        createAlbumBtn.disabled = true;
        createAlbumBtn.textContent = 'アルバム生成中...';

        const formData = new FormData();
        selectedFiles.forEach((file, index) => {
            formData.append(`image_${index + 1}`, file); // ファイルを順番に付加
        });

        try {
            const response = await fetch('/create_album', { // Pythonバックエンドへのエンドポイント
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const result = await response.json();
                alert('アルバムが正常に作成されました！');
                console.log('サーバーからの応答:', result);
                // 1. 生成完了、同時にボタンを出現させる
                viewAlbumSection.style.display = 'block'; // ボタンセクションを表示
                createAlbumBtn.style.display = 'none'; // 作成ボタンを非表示にする（オプション）

            } else {
                alert('アルバム作成中にエラーが発生しました。');
                const errorText = await response.text();
                console.error('サーバーエラー:', errorText);
            }
        } catch (error) {
            console.error('ネットワークエラー:', error);
            alert('ネットワークエラーが発生しました。');
        } finally {
            createAlbumBtn.disabled = false; // エラーでも有効に戻す
            createAlbumBtn.textContent = 'アルバムを作成';
        }
    });

    // 2. 「作成されたアルバムを見る」ボタンがクリックされた時の処理
    viewAlbumBtn.addEventListener('click', () => {
        // ここに開発者様が作成済みのアルバムレイアウトのプログラムを動かすロジックを記述します。
        // 例: 特定のURLにリダイレクト
        alert('アルバムを表示します！ (この後、実際のアルバムページに移動します)');
        window.location.href = '/view_my_album'; // ここを実際のアルバム表示URLに置き換えてください
    });
});