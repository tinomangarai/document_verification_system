import streamlit as st
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image

# Load the trained model
model = load_model('fake_real_classifier.keras')

# Set image size (same as training)
img_size = (224, 224)

# App title
st.title("Fake vs Real Image Classifier")

# Upload image
uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display uploaded image
    img = Image.open(uploaded_file)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    # Preprocess image
    img = img.resize(img_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0  # Normalize

    # Make prediction
    prediction = model.predict(img_array)[0][0]
    label = "Real" if prediction > 0.5 else "Fake"
    confidence = prediction if prediction > 0.5 else 1 - prediction

    # Show result
    st.markdown(f"### Prediction: **{label}**")
    st.markdown(f"### Confidence: **{confidence:.2%}**")
