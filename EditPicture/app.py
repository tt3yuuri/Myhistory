import streamlit as st
from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont
import io
from rembg import remove
import datetime

st.set_page_config(
    page_title="多機能画像編集ソフト",
    layout="wide",
)

st.title('🖼️ 多機能画像編集ソフト')
st.write('写真をアップロードして編集してみましょう。')

# --- 画像アップローダー ---
uploaded_file = st.file_uploader(
    "写真を選択してください",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGBA")
    
    st.sidebar.header("編集ツール")
    
    # --- サイドバーにExpanderを使って機能を整理 ---
    with st.sidebar.expander("🎨 フィルター", expanded=True):
        effect = st.selectbox('フィルターを選択', ['なし', 'グレースケール'])

    with st.sidebar.expander("💡 色調補正"):
        brightness = st.slider('明るさ', 0.0, 2.0, 1.0)
        contrast = st.slider('コントラスト', 0.0, 2.0, 1.0)
    
    with st.sidebar.expander("✂️ トリミング"):
        st.subheader("サイズ変更")
        new_width = st.slider("幅", 50, original_image.width, original_image.width)
        new_height = st.slider("高さ", 50, original_image.height, original_image.height)
        st.subheader("背景削除")
        remove_bg_checkbox = st.checkbox("背景を削除する")

    with st.sidebar.expander("📝 文字入力"):
        st.subheader("文字入力")
        text_input = st.text_input("画像に入力する文字", "")
        font_size = st.slider("文字のサイズ", 10, 100, 30)
        text_color = st.color_picker("文字の色", "#ffffff")
        text_x = st.slider("文字のX座標", 0, original_image.width, 10)
        text_y = st.slider("文字のY座標", 0, original_image.height, 10)

    with st.sidebar.expander("✨ スタンプ"):
        st.subheader("スタンプ")
        stamp_options = {
            "なし": None,
            "フレーム1": "stamps/frame1.png",
            "スタンプ1": "stamps/stamp1.png"
        }
        selected_stamp = st.selectbox("スタンプを選択", list(stamp_options.keys()))

    with st.sidebar.expander("📅 日付"):
        st.subheader("日付の追加")
        add_date = st.checkbox("日付を追加する")
        date_x = st.slider("日付のX座標", 0, original_image.width, 10)
        date_y = st.slider("日付のY座標", 0, original_image.height, original_image.height - 40)
        date_font_size = st.slider("日付の文字サイズ", 10, 50, 20)

    # --- 編集処理 ---
    edited_image = original_image.copy().convert("RGBA")

    # フィルター処理
    if effect == 'グレースケール':
        edited_image = ImageOps.grayscale(edited_image)
        edited_image = edited_image.convert("RGBA")

    # 色調補正処理
    enhancer = ImageEnhance.Brightness(edited_image)
    edited_image = enhancer.enhance(brightness)
    enhancer = ImageEnhance.Contrast(edited_image)
    edited_image = enhancer.enhance(contrast)

    # サイズ変更処理
    if new_width != original_image.width or new_height != original_image.height:
        edited_image = edited_image.resize((new_width, new_height))
    
    # 背景削除処理
    if remove_bg_checkbox:
        edited_image = remove(edited_image)
    
    # スタンプ機能
    if stamp_options[selected_stamp] is not None:
        try:
            stamp_image = Image.open(stamp_options[selected_stamp]).convert("RGBA")
            stamp_image = stamp_image.resize(edited_image.size)
            edited_image.paste(stamp_image, (0, 0), stamp_image)
        except FileNotFoundError:
            st.warning(f"スタンプファイル '{stamp_options[selected_stamp]}' が見つかりません。")

    # 文字描画処理
    if text_input:
        draw = ImageDraw.Draw(edited_image)
        try:
            font = ImageFont.truetype("KiwiMaru-light.ttf", font_size)
        except IOError:
            st.warning("フォントファイルが見つかりません。デフォルトのフォントを使用します。")
            font = ImageFont.load_default()
        draw.text((text_x, text_y), text_input, font=font, fill=text_color)

    # 日付描画処理
    if add_date:
        draw = ImageDraw.Draw(edited_image)
        current_date = datetime.date.today().strftime("%Y/%m/%d")
        try:
            date_font = ImageFont.truetype("KiwiMaru-light.ttf", date_font_size)
        except IOError:
            st.warning("フォントファイルが見つかりません。デフォルトのフォントを使用します。")
            date_font = ImageFont.load_default()
        
        draw.text((date_x, date_y), current_date, font=date_font, fill="#ffffff")

    # --- 画像の表示 ---
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('元の写真')
        st.image(original_image, use_container_width=True)
    with col2:
        st.subheader('編集後の写真')
        st.image(edited_image, use_container_width=True)

    # --- ダウンロード機能 ---
    img_byte_arr = io.BytesIO()
    
    file_extension = uploaded_file.name.split('.')[-1].lower()
    
    if file_extension == 'webp':
        edited_image.save(img_byte_arr, format='WEBP')
        mime_type = "image/webp"
    elif file_extension == 'png':
        edited_image.save(img_byte_arr, format='PNG')
        mime_type = "image/png"
    else:
        if remove_bg_checkbox or text_input or selected_stamp is not None or add_date:
            edited_image.save(img_byte_arr, format='PNG')
            mime_type = "image/png"
            file_extension = "png"
        else:
            edited_image.save(img_byte_arr, format='JPEG')
            mime_type = "image/jpeg"

    st.download_button(
        label="編集後の画像をダウンロード",
        data=img_byte_arr.getvalue(),
        file_name=f'edited_photo.{file_extension}',
        mime=mime_type
    )

else:
    st.info('画像をアップロードして、サイドバーから編集を始めましょう。')