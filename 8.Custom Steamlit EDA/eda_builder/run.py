import streamlit as st
from frontend.ui_builder import main_ui

def main():
    st.set_page_config(page_title="Custom Streamlit EDA Builder", layout="wide")
    main_ui()

if __name__ == "__main__":
    main() 