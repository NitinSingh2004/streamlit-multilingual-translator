import streamlit as st
from mtranslate import translate
from PyPDF2 import PdfReader

st.set_page_config(page_title="🌍 Multilingual Translator", page_icon="🌐", layout="centered")

st.title("🌍 Multilingual Text & PDF Translator")
st.write("Translate text or uploaded PDF files into 100+ languages using `mtranslate`.")

# ---------------------------------------------------
# Language Dictionary (Name → Code)
# ---------------------------------------------------
languages = {
    "Afrikaans": "af", "Albanian": "sq", "Amharic": "am", "Arabic": "ar", "Armenian": "hy",
    "Bengali": "bn", "Bulgarian": "bg", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Dutch": "nl", "English": "en", "French": "fr", "German": "de", "Greek": "el",
    "Gujarati": "gu", "Hebrew": "iw", "Hindi": "hi", "Indonesian": "id", "Italian": "it",
    "Japanese": "ja", "Kannada": "kn", "Korean": "ko", "Malay": "ms", "Malayalam": "ml",
    "Marathi": "mr", "Persian": "fa", "Polish": "pl", "Portuguese": "pt", "Punjabi": "pa",
    "Russian": "ru", "Spanish": "es", "Swahili": "sw", "Tamil": "ta", "Telugu": "te",
    "Thai": "th", "Turkish": "tr", "Ukrainian": "uk", "Urdu": "ur", "Vietnamese": "vi"
}

# ---------------------------------------------------
# Inputs
# ---------------------------------------------------
mode = st.radio("Choose input type:", ["📝 Text", "📄 PDF"])

target_lang = st.selectbox(
    "🌐 Choose target language:",
    list(languages.keys()),
    index=list(languages.keys()).index("Hindi")
)

# ---------------------------------------------------
# TEXT MODE
# ---------------------------------------------------
if mode == "📝 Text":
    text = st.text_area("Enter text to translate:", placeholder="Type or paste your text here...")
    if st.button("🚀 Translate Text"):
        if text.strip():
            code = languages[target_lang]
            try:
                translated = translate(text, code)
                st.success(f"**Translated to {target_lang}:**")
                st.write(translated)
            except Exception as e:
                st.error("❌ Error during translation.")
                st.exception(e)
        else:
            st.warning("⚠️ Please enter some text.")

# ---------------------------------------------------
# PDF MODE
# ---------------------------------------------------
else:
    uploaded_file = st.file_uploader("📤 Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        try:
            reader = PdfReader(uploaded_file)
            text = ""
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content + "\n"

            if text.strip():
                st.success(" PDF text extracted successfully!")
                st.text_area("📄 Extracted Text", text[:1500] + "..." if len(text) > 1500 else text, height=200)

                if st.button("🌐 Translate PDF"):
                    code = languages[target_lang]
                    translated = translate(text, code)
                    st.text_area(f"Translated ({target_lang})", translated, height=200)
            else:
                st.warning(" Could not extract text from this PDF (might be scanned images).")
        except Exception as e:
            st.error(" Error while reading PDF file.")
            st.exception(e)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("💡 Built with ❤️ by Nitin Singh using Streamlit + mtranslate.")
