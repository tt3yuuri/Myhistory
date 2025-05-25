# my_album_gallery_app/main_page.py

import streamlit as st

st.set_page_config(
    page_title="私のデジタルアルバムギャラリー",
    page_icon="📸",
    layout="centered"
)

st.title("🌟 デジタルアルバムギャラリーへようこそ！ 🌟")

st.write("このアプリでは、私が作った様々なアルバムやプロジェクトを紹介しています。")
st.write("左側のサイドバーから、見たいアルバムを選んでくださいね！")

st.header("使い方")
st.markdown("""
1.  左のサイドバーにあるアルバム名をクリックします。
2.  各アルバムのページで、写真やコンテンツを楽しんでください！
""")

st.info("何かご意見やご感想があれば、お気軽にお知らせください！")

# 必要であれば、ここにイメージ画像などを追加
# st.image("path/to/some/welcome_image.png", use_column_width=True)