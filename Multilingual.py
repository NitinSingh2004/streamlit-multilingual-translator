import streamlit as st
from mtranslate import translate

st.set_page_config(page_title="🌍 Multilingual Translator", page_icon="🌐", layout="centered")

st.title("🌍 Multilingual Text Translator")
st.write("Translate any text into 100+ languages using `mtranslate`.")

# ---------------------------------------------------
# Full language dictionary (Name → Code)
# ---------------------------------------------------
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

# ---------------------------------------------------
# UI Inputs
# ---------------------------------------------------
text = st.text_area("📝 Enter text to translate:", placeholder="Type something here...")

target_lang = st.selectbox(
    "🌐 Choose your target language:",
    list(languages.keys()),
    index=list(languages.keys()).index("Hindi")
)

# ---------------------------------------------------
# Translation
# ---------------------------------------------------
if st.button("🚀 Translate"):
    if text.strip():
        code = languages[target_lang]
        try:
            translated = translate(text, code)
            st.success(f"**Translated to {target_lang}:**")
            st.write(translated)
        except Exception as e:
            st.error("❌ Error during translation. Please try again.")
            st.exception(e)
    else:
        st.warning("⚠️ Please enter some text to translate.")

# ---------------------------------------------------
# Footer
# ---------------------------------------------------
st.markdown("---")
st.caption("💡 Built with ❤️ by Nitin Singh using Streamlit + mtranslate.")
