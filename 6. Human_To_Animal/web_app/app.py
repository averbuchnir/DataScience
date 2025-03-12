import streamlit as st
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from utils import extract_human_features, load_animal_data, compute_similarity, get_most_similar_image

st.title("🐾 Human-to-Animal Match Web App")
st.write("Upload your photo and see which animal you resemble the most!")

uploaded_file = st.file_uploader("📸 Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display uploaded image (Smaller size)
    st.image(uploaded_file, caption="Uploaded Image", width=250)  # Smaller display

    # Extract features & find best match
    human_features = extract_human_features(uploaded_file)
    if human_features is not None:
        animal_features, labels = load_animal_data()
        results, best_match_index = compute_similarity(human_features, animal_features, labels)
        best_match_path = get_most_similar_image(best_match_index, labels)

        # Create two columns for Best Match Image and Pie Chart
        col1, col2 = st.columns([1, 1])  # Equal width columns

        with col1:
            # Display Best Match Image (Larger)
            st.subheader(f"Best Match: {list(results.keys())[0]} 🐾")
            if best_match_path:
                best_match_img = Image.open(best_match_path)
                st.image(best_match_img, caption="Most Similar Animal", use_container_width=True)
            else:
                st.write("No similar animal found.")

        with col2:
            # Create Pie Chart
            st.subheader("Similarity Score Distribution")
            fig, ax = plt.subplots()
            ax.pie(results.values(), labels=results.keys(), autopct="%1.1f%%", startangle=140, colors=plt.cm.Paired.colors)
            st.pyplot(fig)
