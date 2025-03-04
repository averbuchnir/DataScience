import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import numpy as np
import plotly.graph_objects as go

def plot_graph(df, parameter, sorted_names, parameter_units, graph_type, 
               label_options=None, time_interval='3min', bins=None):
    """
    Plots a graph based on the selected parameters, and allows for time-based aggregation.

    Parameters:
    - df: DataFrame containing the data.
    - parameter: The parameter to plot (e.g., temperature, humidity).
    - sorted_names: List of unique names.
    - parameter_units: Dictionary containing the units of the parameters.
    - graph_type: Type of graph ('line', 'scatter', or 'histogram').
    - label_options: Column to use for color/hue (starts with #).
    - time_interval: Time aggregation interval (e.g., '5T' for 5 minutes, '10T' for 10 minutes).
    - bins: Number of bins for the histogram (only applicable if graph_type is 'histogram').
    """

    # Convert the TimeStamp column to datetime if it's not already
    df['TimeStamp'] = pd.to_datetime(df['TimeStamp'])

    # Round timestamps to the nearest interval (e.g., '5T' for 5 minutes)
    df['TimeStamp'] = df['TimeStamp'].dt.round(time_interval)

    if graph_type == 'heatmap':
        # Calculate the correlation matrix
        corr_matrix = df[['light', 'temperature', 'humidity', 'barometric_pressure', 'barometric_temp', 'battery']].corr()
        # Create a heatmap of the correlation matrix
        z = np.around(corr_matrix.values, decimals=2)
        x = corr_matrix.columns.tolist()
        y = corr_matrix.index.tolist()
        fig = ff.create_annotated_heatmap(z, x=x, y=y, 
                        annotation_text=z.astype(str), colorscale='RdYlGn', showscale=True)
        fig.update_layout(title='Correlation Matrix Heatmap')

    if label_options is not None:
        # Group by both TimeStamp and the selected label, then calculate mean and std
        df_grouped = df.groupby(['TimeStamp', label_options]).agg(
            avg_parameter=(parameter, 'mean'),
            std_parameter=(parameter, 'std')
        ).reset_index()

        # Create upper and lower bounds for mean ± std
        df_grouped['upper_bound'] = df_grouped['avg_parameter'] + df_grouped['std_parameter']
        df_grouped['lower_bound'] = df_grouped['avg_parameter'] - df_grouped['std_parameter']

        # Plot based on the graph type
        if graph_type == 'line':
            fig = px.line(
                df_grouped,
                x='TimeStamp',
                y='avg_parameter',
                color=label_options,
                error_y='std_parameter',  # Error bars using standard deviation
                labels={'avg_parameter': f'{parameter} ({parameter_units[parameter]})'},
                title=f'Average {parameter.capitalize()} over Time (Aggregated by {time_interval})'
            )
        elif graph_type == 'scatter':
            fig = px.scatter(
                df_grouped,
                x='TimeStamp',
                y='avg_parameter',
                color=label_options,
                error_y='std_parameter',  # Error bars using standard deviation
                labels={'avg_parameter': f'{parameter} ({parameter_units[parameter]})'},
                title=f'Average {parameter.capitalize()} Scatter Plot (Aggregated by {time_interval})'
            )
        elif graph_type == 'histogram':
            fig = px.histogram(
                df_grouped,
                x='avg_parameter',
                color=label_options,
                nbins=bins,  # Control over the number of bins
                labels={'avg_parameter': f'{parameter} ({parameter_units[parameter]})'},
                title=f'Histogram of Average {parameter.capitalize()}'
            )
                                                                                                             
    else:
        # Original plotting without averaging if no label options selected
        if graph_type == 'line':
            fig = px.line(
                df,
                x='TimeStamp',
                y=parameter,
                color='Name',
                line_group='Name',
                labels={parameter: f'{parameter} ({parameter_units[parameter]})'},
                title=f'{parameter.capitalize()} over Time (Aggregated by {time_interval})'
            )
        elif graph_type == 'scatter':
            fig = px.scatter(
                df,
                x='TimeStamp',
                y=parameter,
                color='Name',
                labels={parameter: f'{parameter} ({parameter_units[parameter]})'},
                title=f'{parameter.capitalize()} Scatter Plot (Aggregated by {time_interval})'
            )
        elif graph_type == 'histogram':
            fig = px.histogram(
                df,
                x=parameter,
                color='Name',
                nbins=bins,  # Control over the number of bins
                labels={parameter: f'{parameter} ({parameter_units[parameter]})'},
                title=f'Histogram of {parameter.capitalize()}'
            )
    return fig
