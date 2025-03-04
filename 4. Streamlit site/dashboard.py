import streamlit as st
import logging
from datetime import datetime
import pandas as pd
import re
import plotly.express as px
import numpy as np
from graphs import plot_graph




def apply_iqr_filter(df, column, n=1.5):
    """Apply IQR filter to the dataframe."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    filter = (df[column] >= Q1 - n * IQR) & (df[column] <= Q3 + n * IQR)
    df.loc[~filter, column] = np.nan
    return df

def apply_std_filter(df, column, n=2.5):
    """Apply Standard Deviation filter to the dataframe."""
    mean = df[column].mean()
    std_dev = df[column].std()
    filter = (df[column] >= mean - n * std_dev) & (df[column] <= mean + n * std_dev)
    df.loc[~filter, column] = np.nan
    return df

def apply_zscore_filter(df, column, threshold=3):
    """Apply Z-Score filter to the dataframe."""
    mean = df[column].mean()
    std_dev = df[column].std()
    df['zscore'] = (df[column] - mean) / std_dev
    filter = np.abs(df['zscore']) < threshold
    df.loc[~filter, column] = np.nan
    return df

def dash_board():
    """Main function to display the dashboard."""
    df_full_data_modify = pd.read_csv("Sample_DATA.csv")
    if df_full_data_modify.empty:
        st.error("No data available.")
        logging.error("No data available.")
        return
    else:
        st.session_state['original_data'] = df_full_data_modify

    with st.sidebar:
        st.title("Data Visualization")
        graph_type = st.selectbox("Select Graph Type", ('scatter', 
                                    'line','histogram',"heatmap"), key='graph_type')
        parameter = ""
        sorted_names = []
        parameter_units = {}
        time_interval = None
        label_optinos = None

        filter_method = st.selectbox("Select Outlier Detection Method", ('None', 'IQR-Outlier filter', 'Standard Deviation filter', 'Z-Score filter'), key='filter_method')
        if filter_method == 'IQR-Outlier filter':
            st.markdown("[Interquartile Range (IQR) Outlier Filter](https://en.wikipedia.org/wiki/Interquartile_range): This method identifies outliers by looking at the spread of the middle 50% of the data.")
            n_iqr_slider = st.slider('Select IQR multiplier', min_value=0.5, max_value=3.0, value=2.5, step=0.1, key='IQR_multiplier_slider')
        elif filter_method == 'Standard Deviation filter':
            st.markdown("[Standard Deviation Outlier Filter](https://en.wikipedia.org/wiki/Standard_deviation): This method identifies outliers by looking at how many standard deviations a data point is from the mean.")
            n_std_slider = st.slider('Select Standard Deviation multiplier', min_value=1.0, max_value=5.0, value=2.5, step=0.5, key='STD_multiplier_slider')
        elif filter_method == 'Z-Score filter':
            st.markdown("[Z-Score Outlier Filter](https://en.wikipedia.org/wiki/Standard_score): This method identifies outliers by looking at the Z-score, which measures how many standard deviations a data point is from the mean.")
            n_z_slider = st.slider('Select Z-Score multiplier', min_value=1.0, max_value=5.0, value=3.0, step=0.5, key='Z_Score_multiplier_slider')
        if graph_type != 'heatmap':
            parameter = st.selectbox('Select Parameter', ['temperature', 'humidity', 'light', 'barometric_pressure', 'barometric_temp', 'battery'], key='select_parameter')
            parameter_units = {
                'temperature': '°C',
                'humidity': '%',
                'light': 'lux',
                'barometric_pressure': 'millibars',
                'barometric_temp': '°C',
                'battery': 'Voltage',
            }


            bins = None
            if graph_type == "histogram":
                bins = st.slider('Select Number of Bins', min_value=5, max_value=50, value=10, step=1, key='bins_slider')

            labels = [col for col in st.session_state['original_data'].columns if col.startswith("#")]
            labels.insert(0, None)
            label_optinos = st.selectbox("Select Label", labels, key='label_options')



            if label_optinos is not None:
                st.selectbox('Select Time Interval', ['minute', 'hour'], key='time_interval_select_box')
                if st.session_state['time_interval_select_box'] == 'minute':
                    time_interval = st.slider('Select Time Interval (minutes)', min_value=3, max_value=60, value=3, step=3, key='time_interval_slider')
                    time_interval = str(time_interval) + 'min'
                else:
                    time_interval = st.slider('Select Time Interval (hours)', min_value=1, max_value=24, value=1, step=1, key='time_interval_slider')
                    time_interval = str(time_interval) + 'H'

        if st.button('Show Graphs for Selected Parameter', key='show_graphs_button'):
            try:
                df = st.session_state['original_data'].copy()

                if filter_method == 'IQR-Outlier filter':
                    df = apply_iqr_filter(df, parameter, n_iqr_slider)
                elif filter_method == 'Standard Deviation filter':
                    df = apply_std_filter(df, parameter, n_std_slider)
                elif filter_method == 'Z-Score filter':
                    df = apply_zscore_filter(df, parameter)

                sorted_names = sorted(df['Name'].unique())

                # Ensure time_interval is passed only if not None
                if time_interval:
                    fig = plot_graph(df, parameter, sorted_names, parameter_units, graph_type, label_optinos, time_interval,bins)
                else:
                    fig = plot_graph(df, parameter, sorted_names, parameter_units, graph_type, label_optinos)
    
                st.session_state['fig'] = fig
                if graph_type != 'heatmap':
                    if label_optinos is not None:
                        df_grouped = df.groupby(['TimeStamp', label_optinos]).agg(
                            avg_parameter=(parameter, 'mean'),
                            std_parameter=(parameter, 'std')
                        ).reset_index()
                        # set time as index
                        df_grouped.set_index('TimeStamp', inplace=True)

                        st.session_state['df_pivot'] = df_grouped
                    else:                    
                        df_pivot = df.pivot_table(index='TimeStamp', columns='Name', values=parameter, aggfunc='mean')
                        df_pivot.index = pd.to_datetime(df_pivot.index)
                        df_pivot.index = df_pivot.index.strftime('%Y-%m-%dT%H:%M')
                        df_pivot.index = pd.to_datetime(df_pivot.index).round('3min').strftime('%Y-%m-%dT%H:%M:%S')
                        df_pivot.index.name = "TimeStamp"
                        st.session_state['df_pivot'] = df_pivot
                else: # create df called df_corr for heatmap
                    df_corr = df[['light', 'temperature', 'humidity', 'barometric_pressure', 'barometric_temp', 'battery']].corr()
                    st.session_state['df_corr'] = df_corr

            except KeyError:
                if graph_type!='heatmap':
                    st.error("No data available for the selected parameter.")
                    logging.error("No data available for the selected parameter.")

    if 'fig' in st.session_state:
        # Set layout properties for the figure


        # Render the plot in Streamlit with container width adjustment
        st.plotly_chart(fig,use_container_width=True)

    if 'df_pivot' in st.session_state:
        df_pivot = st.session_state['df_pivot']
        csv = df_pivot.to_csv(index=True).encode('utf-8')
        st.sidebar.download_button(f"Press to Download {parameter}", csv, f"{parameter}.csv", "text/csv", key='download_csv_button')
    if 'df_corr' in st.session_state:
        df_corr = st.session_state['df_corr']
        csv = df_corr.to_csv(index=True).encode('utf-8')
        st.sidebar.download_button(f"Press to Download Correlation Matrix", csv, "correlation_matrix.csv", "text/csv", key='download_corr_csv_button')
