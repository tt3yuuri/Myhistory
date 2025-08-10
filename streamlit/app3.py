# app_streamlit.py

import streamlit as st
from PIL import Image
import os
import shutil

# --- アプリケーション設定 ---
st.set_page_config(page_title="アルバム作成 & 管理", layout="wide")

st.title("📸 アルバム作成 & 管理")

# --- 画像処理フォルダの設定 ---
ALBUM_FOLDER = 'albums'
if not os.path.exists(ALBUM_FOLDER):
    os.makedirs(ALBUM_FOLDER)

# --- タブによるページ切り替え ---
tab1, tab2 = st.tabs(["🖼️ アルバム作成", "🗂️ アルバム管理"])

# --- 1. アルバム作成タブ ---
with tab1:
    st.header("ステップ1: アルバム情報を入力して画像を選択")
    
    # アルバム名を入力
    album_name = st.text_input("アルバム名を入力してください", "新しいアルバム")

    # ファイルアップローダーウィジェット
    uploaded_files = st.file_uploader("ここに画像をドラッグ＆ドロップするか、ファイルを選択してください。（8枚）",
                                      type=["jpg", "jpeg", "png", "webp"],
                                      accept_multiple_files=True)

    if uploaded_files:
        if len(uploaded_files) != 8:
            st.warning(f"現在 {len(uploaded_files)} 枚の画像が選択されています。8枚選択してください。")
        else:
            st.success("8枚の画像が選択されました！")
            
            # プレビュー表示
            st.subheader("プレビュー")
            cols = st.columns(4)
            for i, file in enumerate(uploaded_files):
                with cols[i % 4]:
                    st.image(file, caption=f"選択順: {i+1}", use_container_width=True)

            # 「アルバムを作成」ボタン
            if st.button("アルバムを作成", key="create_album_btn"):
                # アルバム名をフォルダ名として使用
                new_album_path = os.path.join(ALBUM_FOLDER, album_name)
                
                # 同じアルバム名が既に存在するかチェック
                if os.path.exists(new_album_path):
                    st.error(f"'{album_name}'という名前のアルバムは既に存在します。別の名前を入力してください。")
                else:
                    os.makedirs(new_album_path)

                    # プログレスバーを表示
                    progress_bar = st.progress(0)
                    st.info(f"'{album_name}'アルバムを生成中...")

                    for i, file in enumerate(uploaded_files):
                        try:
                            img = Image.open(file)
                            original_ext = img.format.lower()
                            if original_ext == 'jpeg':
                                original_ext = 'jpg'

                            RESIZE_WIDTHS = {400: '1', 800: '2', 1200: '3'}
                            for width_px, prefix in RESIZE_WIDTHS.items():
                                aspect_ratio = img.width / img.height
                                new_height = int(width_px / aspect_ratio)
                                resized_img = img.resize((width_px, new_height), Image.Resampling.LANCZOS)
                                
                                # ファイル名を生成し、新しいフォルダに保存
                                filename = f"{prefix}-{i+1}.{original_ext}"
                                save_path = os.path.join(new_album_path, filename)
                                resized_img.save(save_path)
                            
                            progress_bar.progress((i + 1) / 8)

                        except Exception as e:
                            st.error(f"画像の処理中にエラーが発生しました: {e}")
                            shutil.rmtree(new_album_path) # エラーが発生したら作成したフォルダを削除
                            break
                    else:
                        st.success(f"'{album_name}'アルバムの生成が完了しました！アルバム管理タブで確認できます。")
                        st.balloons()
                    
                    progress_bar.empty()

# --- 2. アルバム管理タブ ---
with tab2:
    st.header("ステップ2: 作成済みアルバムの管理")

    def get_albums():
        # albumsフォルダ内のディレクトリ（アルバム名）を取得
        album_dirs = [d for d in os.listdir(ALBUM_FOLDER) if os.path.isdir(os.path.join(ALBUM_FOLDER, d))]
        return sorted(album_dirs)

    album_names = get_albums()

    if not album_names:
        st.info("まだアルバムがありません。アルバム作成タブから作成してください。")
    else:
        st.subheader("アルバム一覧")

        for album_name in album_names:
            album_path = os.path.join(ALBUM_FOLDER, album_name)
            
            # 各アルバムをエクスパンダーで表示
            with st.expander(album_name):
                # アルバム内の画像ファイルを取得
                image_files = sorted(os.listdir(album_path))
                
                # HTMLのレイアウトを再現するため、4列のグリッドを作成
                cols = st.columns(4)
                
                # 幅400pxの画像を代表として表示
                for i, filename in enumerate(image_files):
                    if filename.startswith('1-'):
                        with cols[i % 4]:
                            st.image(os.path.join(album_path, filename), use_container_width=True)
                            st.caption(filename)
                
                # 削除ボタン
                if st.button(f"'{album_name}'アルバムを削除", key=f"delete_album_{album_name}"):
                    # フォルダごと削除
                    st.warning(f"本当に'{album_name}'アルバムを削除しますか？")
                    col_confirm, col_cancel = st.columns(2)
                    with col_confirm:
                        if st.button("はい、削除します", key=f"confirm_delete_{album_name}"):
                            shutil.rmtree(album_path)
                            st.success(f"'{album_name}'アルバムを削除しました。")
                            st.experimental_rerun()
                    with col_cancel:
                        if st.button("キャンセル", key=f"cancel_delete_{album_name}"):
                            st.info("削除をキャンセルしました。")
                            st.experimental_rerun()