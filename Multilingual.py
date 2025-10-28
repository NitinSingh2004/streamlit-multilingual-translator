import streamlit as st
from mtranslate import translate
from PIL import Image
import easyocr
import numpy as np
import os
from fpdf import FPDF

# -------------------- Page Setup --------------------
st.set_page_config(page_title="🌍 OCR + Multilingual Translator", page_icon="🌐", layout="centered")

st.title("📷 OCR + 🌍 Multilingual Text Translator")
st.write("Extract text from images or type manually, then translate it into 100+ languages!")

# -------------------- Language Dictionary --------------------
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

# -------------------- Mode Selection --------------------
mode = st.radio("📂 Choose Input Mode:", ["🖼️ Upload Image", "✍️ Type or Paste Text"])

target_lang = st.selectbox("🌐 Choose Target Language:", list(languages.keys()), index=list(languages.keys()).index("Hindi"))

# -------------------- EasyOCR Setup --------------------
MODEL_DIR = os.path.join(os.getcwd(), "models")
os.makedirs(MODEL_DIR, exist_ok=True)
reader = easyocr.Reader(['en', 'hi'], model_storage_directory=MODEL_DIR, gpu=False)

# -------------------- OCR or Text Input --------------------
extracted_text = ""

if mode == "🖼️ Upload Image":
    img_file = st.file_uploader("📸 Upload an image", type=["png", "jpg", "jpeg"])
    if img_file:
        image = Image.open(img_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        with st.spinner("🔍 Extracting text using OCR..."):
            result = reader.readtext(np.array(image))
            extracted_text = " ".join([res[1] for res in result])
        st.subheader("📝 Extracted Text:")
        st.write(extracted_text if extracted_text.strip() else "⚠️ No text detected.")

else:
    extracted_text = st.text_area("🧾 Enter your text below:")

# -------------------- Translation --------------------
if st.button("🚀 Translate"):
    if extracted_text.strip():
        code = languages[target_lang]
        try:
            translated = translate(extracted_text, code)
            st.success(f"✅ Translated to {target_lang}:")
            st.write(translated)

            # PDF Export Option
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt="Original Text:\n" + extracted_text)
            pdf.ln(10)
            pdf.multi_cell(0, 10, txt=f"Translated Text ({target_lang}):\n" + translated)
            pdf_output = "translation_output.pdf"
            pdf.output(pdf_output)

            with open(pdf_output, "rb") as f:
                st.download_button("📥 Download PDF", f, file_name="translation_result.pdf")

        except Exception as e:
            st.error("❌ Error during translation. Please try again.")
            st.exception(e)
    else:
        st.warning("⚠️ Please enter or extract some text first!")

# -------------------- Footer --------------------
st.markdown("---")
st.caption("💡 Built with ❤️ by Nitin Singh using Streamlit, EasyOCR, and mtranslate.")




