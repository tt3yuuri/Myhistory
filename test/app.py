# app.py (例: Flaskを使用)
from flask import Flask, request, jsonify, send_from_directory,render_template
from PIL import Image
import os

app = Flask(__name__)

# 保存先のディレクトリを設定
UPLOAD_FOLDER = 'uploads'
ALBUM_FOLDER = 'albums'

# --- 新しく追加する部分 ---
# /albums/ というURLでalbumsフォルダの中のファイルを公開する
@app.route('/albums/<path:filename>')
def serve_album_images(filename):
    return send_from_directory(ALBUM_FOLDER, filename)
# --------------------------

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(ALBUM_FOLDER):
    os.makedirs(ALBUM_FOLDER)


# 画像のリサイズ幅
RESIZE_WIDTHS = {
    400: '1',
    800: '2',
    1200: '3'
}

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def serve_css():
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def serve_js():
    return send_from_directory('.', 'script.js')

@app.route('/create_album', methods=['POST'])
def create_album():
    if request.method == 'POST':
        if not request.files:
            return jsonify({'error': 'ファイルがアップロードされていません'}), 400

        processed_images = []
        for i in range(1, 9): # 1から8までの画像
            file_key = f'image_{i}'
            if file_key in request.files:
                file = request.files[file_key]
                try:
                    img = Image.open(file.stream)

                    # 元のファイル拡張子を取得
                    original_ext = img.format.lower()
                    if original_ext == 'jpeg':
                        original_ext = 'jpg'

                    for width_px, prefix in RESIZE_WIDTHS.items():
                        # アスペクト比を維持して高さを計算
                        aspect_ratio = img.width / img.height
                        new_height = int(width_px / aspect_ratio)
                        resized_img = img.resize((width_px, new_height), Image.Resampling.LANCZOS)

                        # ファイル名を生成: (幅のプレフィックス)-(選択順).拡張子
                        filename = f"{prefix}-{i}.{original_ext}"
                        save_path = os.path.join(ALBUM_FOLDER, filename)
                        resized_img.save(save_path)
                        processed_images.append(filename)

                except Exception as e:
                    print(f"画像の処理中にエラーが発生しました: {e}")
                    return jsonify({'error': f'画像の処理中にエラーが発生しました: {e}'}), 500
            else:
                return jsonify({'error': f'{file_key} が見つかりません。8枚の画像が必要です。'}), 400

        return jsonify({'message': 'アルバムが正常に作成されました', 'files': processed_images}), 200

# 新しく追加: ダミーのアルバム表示ページのエンドポイント
@app.route('/view_my_album')
def view_my_album():
    # ここに、開発者様が作成済みのアルバムレイアウトのHTMLを返すロジックを実装します。
    # 例: return render_template('your_album_template.html')
    # 今は動きの確認のため、簡単なメッセージを返します。
    return render_template('layout.html')

if __name__ == '__main__':
    app.run(debug=True)