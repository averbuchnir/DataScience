import sys
import os
import streamlit as st
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'eda_builder')))
from eda_builder.frontend.ui_builder import main_ui

def main():
    st.set_page_config(page_title="Custom Streamlit EDA Builder", layout="wide")
    main_ui()

if __name__ == "__main__":
    main() 