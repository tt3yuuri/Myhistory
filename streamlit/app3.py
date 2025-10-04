import streamlit as st
from PIL import Image
import os
import shutil
import streamlit.components.v1 as components

# --- アプリケーション設定 ---
st.set_page_config(page_title="アルバム作成 & 管理", layout="wide")

st.title("📸 アルバム作成 & 管理")

# --- 画像処理フォルダの設定 ---
ALBUM_FOLDER = 'albums'
if not os.path.exists(ALBUM_FOLDER):
    os.makedirs(ALBUM_FOLDER)

# --- ページ状態を管理するセッションステート ---
if 'page' not in st.session_state:
    st.session_state.page = 'manage'  # デフォルトはアルバム管理画面
if 'selected_album' not in st.session_state:
    st.session_state.selected_album = None
if 'album_to_delete' not in st.session_state:
    st.session_state.album_to_delete = None

# --- アルバム表示ページ ---
# --- アルバム表示ページ ---
def show_album_page(album_name):
    st.header(f"アルバム: {album_name}")
    
    # アルバム管理画面に戻るボタン
    if st.button("アルバム管理画面に戻る"):
        st.session_state.page = 'manage'
        st.session_state.selected_album = None
        st.rerun()
    
    # 物理的なファイルパス
    physical_album_path = os.path.join(ALBUM_FOLDER, album_name)
    # 物理パスを使ってフォルダの中身をリストアップ
    image_files = sorted([f for f in os.listdir(physical_album_path) if f.startswith('1-')])

    # ローカルにあるHTMLファイルを埋め込む例
    with open("my_local_page.html", "r", encoding="utf-8") as f:
        local_html = f.read()

    components.html(local_html, height=500)

# --- メインページ（タブ）の表示ロジック ---
if st.session_state.page == 'manage':
    tab1, tab2 = st.tabs(["🖼️ アルバム作成", "🗂️ アルバム管理"])
    
    # --- 1. アルバム作成タブ ---
    with tab1:
        st.header("ステップ1: アルバム情報を入力して画像を選択")
        
        album_name = st.text_input("アルバム名を入力してください", "新しいアルバム")

        uploaded_files = st.file_uploader("ここに画像をドラッグ＆ドロップするか、ファイルを選択してください。（8枚）",
                                          type=["jpg", "jpeg", "png", "webp"],
                                          accept_multiple_files=True)

        if uploaded_files:
            if len(uploaded_files) != 8:
                st.warning(f"現在 {len(uploaded_files)} 枚の画像が選択されています。8枚選択してください。")
            else:
                st.success("8枚の画像が選択されました！")
                
                st.subheader("プレビュー")
                cols = st.columns(4)
                for i, file in enumerate(uploaded_files):
                    with cols[i % 4]:
                        st.image(file, caption=f"選択順: {i+1}", use_container_width=True)

                if st.button("アルバムを作成", key="create_album_btn"):
                    new_album_path = os.path.join(ALBUM_FOLDER, album_name)
                    
                    if os.path.exists(new_album_path):
                        st.error(f"'{album_name}'という名前のアルバムは既に存在します。別の名前を入力してください。")
                    else:
                        os.makedirs(new_album_path)

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
                                    
                                    filename = f"{prefix}-{i+1}.{original_ext}"
                                    save_path = os.path.join(new_album_path, filename)
                                    resized_img.save(save_path)
                                
                                progress_bar.progress((i + 1) / 8)

                            except Exception as e:
                                st.error(f"画像の処理中にエラーが発生しました: {e}")
                                shutil.rmtree(new_album_path)
                                break
                        else:
                            st.success(f"'{album_name}'アルバムの生成が完了しました！アルバム管理タブで確認できます。")
                            st.balloons()
                        
                        progress_bar.empty()

    # --- 2. アルバム管理タブ ---
    with tab2:
        st.header("ステップ2: 作成済みアルバムの管理")

        def get_albums():
            album_dirs = [d for d in os.listdir(ALBUM_FOLDER) if os.path.isdir(os.path.join(ALBUM_FOLDER, d))]
            return sorted(album_dirs)

        album_names = get_albums()

        if not album_names:
            st.info("まだアルバムがありません。アルバム作成タブから作成してください。")
        else:
            st.subheader("アルバム一覧")

            cols = st.columns(4)
            for i, album_name in enumerate(album_names):
                with cols[i % 4]:
                    if st.button(f"'{album_name}'", key=f"album_btn_{album_name}", use_container_width=True):
                        st.session_state.page = 'view_album'
                        st.session_state.selected_album = album_name
                        st.rerun()
            
            st.markdown("---")
            
            # 削除ボタン
            st.subheader("アルバム削除")
            for album_name in album_names:
                if st.button(f"'{album_name}'アルバムを削除", key=f"delete_album_{album_name}"):
                    st.session_state.album_to_delete = album_name
                    st.rerun() # 削除確認の表示のために再読み込み

            # 削除確認のロジック
            if st.session_state.album_to_delete:
                album_to_delete_name = st.session_state.album_to_delete
                st.warning(f"本当に'{album_to_delete_name}'アルバムを削除しますか？")
                col_confirm, col_cancel = st.columns(2)
                with col_confirm:
                    if st.button("はい、削除します", key=f"confirm_delete_{album_to_delete_name}"):
                        try:
                            shutil.rmtree(os.path.join(ALBUM_FOLDER, album_to_delete_name))
                            st.success(f"'{album_to_delete_name}'アルバムを削除しました。")
                            st.session_state.album_to_delete = None
                        except Exception as e:
                            st.error(f"アルバムの削除中にエラーが発生しました: {e}")
                        st.rerun()
                with col_cancel:
                    if st.button("キャンセル", key=f"cancel_delete_{album_to_delete_name}"):
                        st.info("削除をキャンセルしました。")
                        st.session_state.album_to_delete = None
                        st.rerun()


elif st.session_state.page == 'view_album' and st.session_state.selected_album:
    show_album_page(st.session_state.selected_album)

# --- フッター ---
st.markdown("---")
st.markdown("Powered by Streamlit")