# my_album_gallery_app/pages/album_gallery_1.py

import streamlit as st
import os

st.set_page_config(
    page_title="🌳 自然風景アルバム",
    page_icon="🌲",
    layout="wide" # HTMLコンテンツを広く表示するためにwideにするのがおすすめ
)

st.title("🌲 美しい自然風景のアルバム 🌲")
st.write("ここでは、心を癒やしてくれる自然の風景写真を集めてみました。")

# HTMLファイルのパスを正確に指定する
# 現在のPythonファイル (album_gallery_1.py) から見て、
# 2つ上のディレクトリ (my_album_gallery_app) に戻り、
# そこから 'static' -> 'album1' -> 'index.html' へと進むパス
html_file_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'album1', 'ex.html')

try:
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # StreamlitにHTMLコンテンツを埋め込む
    # height: 埋め込むHTMLの表示領域の高さ。コンテンツに合わせて調整してね。
    # scrolling: コンテンツが枠に収まらない場合にスクロールバーを表示するか。
    st.components.v1.html(html_content, height=1000, scrolling=True)

except FileNotFoundError:
    st.error(f"エラー: HTMLファイルが見つかりません。パスを確認してください: {html_file_path}")
except Exception as e:
    st.error(f"HTMLファイルの読み込み中にエラーが発生しました: {e}")

st.write("---")
st.info("このアルバムはいかがでしたか？")