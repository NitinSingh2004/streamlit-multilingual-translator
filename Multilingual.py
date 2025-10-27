import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import time
from mtranslate import translate
from transformers import pipeline

# -------------------- Page Setup --------------------
st.set_page_config(page_title="📷 OCR + Translator", page_icon="🌍", layout="centered")

st.title("📷 OCR + Translation App (EasyOCR Version)")
st.write("Extract or enter text, then translate it instantly using mtranslate or Hugging Face models!")

# -------------------- Language Setup --------------------
languages = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
    "Azerbaijani": "az", "Basque": "eu", "Belarusian": "be", "Bengali": "bn", "Bosnian": "bs",
    "Bulgarian": "bg", "Catalan": "ca", "Cebuano": "ceb", "Chichewa": "ny", "Chinese (Simplified)": "zh-CN",
    "Chinese (Traditional)": "zh-TW", "Corsican": "co", "Croatian": "hr", "Czech": "cs", "Danish": "da",
    "Dutch": "nl", "English": "en", "Esperanto": "eo", "Estonian": "et", "Filipino": "tl",
    "Finnish": "fi", "French": "fr", "Frisian": "fy", "Galician": "gl", "Georgian": "ka",
    "German": "de", "Greek": "el", "Gujarati": "gu", "Haitian Creole": "ht", "Hausa": "ha",
    "Hawaiian": "haw", "Hebrew": "iw", "Hindi": "hi", "Hmong": "hmn", "Hungarian": "hu",
    "Icelandic": "is", "Igbo": "ig", "Indonesian": "id", "Irish": "ga", "Italian": "it",
    "Japanese": "ja", "Javanese": "jw", "Kannada": "kn", "Kazakh": "kk", "Khmer": "km",
    "Korean": "ko", "Kurdish (Kurmanji)": "ku", "Kyrgyz": "ky", "Lao": "lo", "Latin": "la",
    "Latvian": "lv", "Lithuanian": "lt", "Luxembourgish": "lb", "Macedonian": "mk", "Malagasy": "mg",
    "Malay": "ms", "Malayalam": "ml", "Maltese": "mt", "Maori": "mi", "Marathi": "mr",
    "Mongolian": "mn", "Myanmar (Burmese)": "my", "Nepali": "ne", "Norwegian": "no", "Pashto": "ps",
    "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa", "Romanian": "ro",
    "Russian": "ru", "Samoan": "sm", "Scots Gaelic": "gd", "Serbian": "sr", "Sesotho": "st",
    "Shona": "sn", "Sindhi": "sd", "Sinhala": "si", "Slovak": "sk", "Slovenian": "sl",
    "Somali": "so", "Spanish": "es", "Sundanese": "su", "Swahili": "sw", "Swedish": "sv",
    "Tajik": "tg", "Tamil": "ta", "Telugu": "te", "Thai": "th", "Turkish": "tr",
    "Ukrainian": "uk", "Urdu": "ur", "Uzbek": "uz", "Vietnamese": "vi", "Welsh": "cy",
    "Xhosa": "xh", "Yiddish": "yi", "Yoruba": "yo", "Zulu": "zu"
}

target_lang = st.selectbox("🌐 Choose Target Language", list(languages.keys()), index=1)
engine = st.radio("⚙️ Choose Translation Engine", ["mtranslate (Fast)", "Hugging Face (Accurate, Slow)"])

# -------------------- EasyOCR Reader --------------------
st.write("🔍 Initializing OCR engine...")
reader = easyocr.Reader(['en', 'hi'], gpu=False)
st.success("✅ EasyOCR is ready!")

# -------------------- Input Mode --------------------
mode = st.radio("🎯 Choose Input Mode", ["📸 Camera", "🖼️ Upload Image", "✍️ Type or Paste Text"])
refresh_time = st.slider("⏱️ Refresh every (seconds)", 2, 10, 4, help="Used only for camera mode.")
start = st.toggle("▶️ Start Translation")

# -------------------- Translation Function --------------------
def translate_text(text, target_lang):
    """Translate text using chosen engine."""
    if not text.strip():
        return "⚠️ No text provided!"
    if engine == "mtranslate (Fast)":
        return translate(text, languages[target_lang])
    else:
        if target_lang == "Hindi":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-hi")
        elif target_lang == "English":
            translator = pipeline("translation", model="Helsinki-NLP/opus-mt-hi-en")
        else:
            return translate(text, languages[target_lang])
        translated = translator(text)
        return translated[0]['translation_text']

# -------------------- OCR Function --------------------
def extract_text(image):
    """Extract text using EasyOCR."""
    result = reader.readtext(np.array(image))
    text = " ".join([res[1] for res in result])
    return text.strip()

# -------------------- MAIN APP LOGIC --------------------
if start:
    placeholder_text = st.empty()
    placeholder_trans = st.empty()

    if mode == "📸 Camera":
        st.info("Camera is active. Keep text visible for detection.")
        while True:
            img_file = st.camera_input("📷 Show text to the camera", key=time.time())
            if img_file is not None:
                image = Image.open(img_file)
                text = extract_text(image)

                if text:
                    placeholder_text.subheader("📝 Detected Text:")
                    placeholder_text.write(text[:400] + "..." if len(text) > 400 else text)

                    translated_text = translate_text(text, target_lang)
                    placeholder_trans.subheader(f"🌐 Translated to {target_lang}:")
                    placeholder_trans.write(translated_text)
                else:
                    placeholder_text.warning("⚠️ No readable text detected.")
            else:
                placeholder_text.info("Waiting for image capture...")

            time.sleep(refresh_time)
            st.rerun()

    elif mode == "🖼️ Upload Image":
        img_file = st.file_uploader("📤 Upload an image", type=["png", "jpg", "jpeg"])
        if img_file:
            image = Image.open(img_file)
            text = extract_text(image)
            st.subheader("📝 Extracted Text:")
            st.write(text if text else "⚠️ No text detected.")
            if st.button("Translate Text"):
                translated_text = translate_text(text, target_lang)
                st.subheader(f"🌐 Translated to {target_lang}:")
                st.write(translated_text)

    elif mode == "✍️ Type or Paste Text":
        user_text = st.text_area("🧾 Enter your text below:")
        if st.button("Translate Text"):
            translated_text = translate_text(user_text, target_lang)
            st.subheader(f"🌐 Translated to {target_lang}:")
            st.write(translated_text)



