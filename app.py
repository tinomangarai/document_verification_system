import streamlit as st
from PIL import Image
import pytesseract

st.set_page_config(page_title="Utility Bill Verifier", layout="centered")
st.title("🔍 Utility Bill Verifier")
st.markdown("Upload a utility bill image to check if it's **Real or Fake** using text analysis.")

uploaded_file = st.file_uploader("📄 Upload Utility Bill Image", type=["png", "jpg", "jpeg"])

def extract_text(image):
    return pytesseract.image_to_string(image)

def detect_forgery_from_text(text):
    required_keywords = ["electricity", "account", "meter", "bill", "customer"]
    found_keywords = [kw for kw in required_keywords if kw in text.lower()]

    if len(found_keywords) < 2:
        return True, f"Suspicious: Found only {', '.join(found_keywords) or 'none'} of the required keywords."
    return False, "Document appears legitimate."

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Utility Bill", use_column_width=True)

    with st.spinner("🔍 Extracting and analyzing text..."):
        text = extract_text(image)
        is_fake, reason = detect_forgery_from_text(text)

    st.subheader("📄 Extracted Text")
    st.text(text)

    st.subheader("✅ Verification Result")
    if is_fake:
        st.error("❌ FAKE DOCUMENT DETECTED")
    else:
        st.success("✅ DOCUMENT APPEARS REAL")

    st.markdown(f"**Reason:** {reason}")
