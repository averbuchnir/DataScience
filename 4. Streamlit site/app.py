import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
from pandas import json_normalize
import plotly.express as px
import os
import logging
import csv

from dashboard import dash_board

# # Define the log directory path called log
# log_dir = 'logs'
# print(os.path.exists(log_dir))

# # Create logs directory if it does not exist
# if not os.path.exists(log_dir):
#     os.makedirs(log_dir)

    
# # Configure logging
# logging.basicConfig(
#     filename=os.path.join(log_dir, 'app.log'),
#     level=logging.INFO,
#     format='%(asctime)s,%(levelname)s,%(message)s',
#     datefmt='%Y-%m-%d %H:%M:%S'
# )
# Add custom CSS for background
def add_bg_with_gradient():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(to right, #d4fc79, #96e6a1);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


def main():
    add_bg_with_gradient()
    dash_board()

if __name__ == '__main__':
    main()
