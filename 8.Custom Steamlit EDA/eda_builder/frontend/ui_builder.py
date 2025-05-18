import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from sklearn.metrics import r2_score
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import base64
import io
import zipfile

# --- Sample Datasets ---
SAMPLE_DATASETS = {
    "Titanic": "titanic.csv",
    "Iris": "iris.csv",
    "Wine Quality": "winequality.csv",
    "Tips": "tips.csv",
    "Diabetes": "diabetes.csv"
}
SAMPLE_DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "sample_data")
COMPONENTS = ["Histogram", "Boxplot", "Scatter Plot", "Bar Plot", "Line Plot", "Pie Chart"]

REQUIREMENTS = ["streamlit", "pandas", "plotly", "nbformat"]

def get_sample_path(name):
    return os.path.join(SAMPLE_DATA_PATH, SAMPLE_DATASETS[name])

def default_block_config(df, block_type):
    cols = df.columns.tolist()
    config = {
        "x": cols[0] if cols else None,
        "y": cols[1] if len(cols) > 1 else None,
        "hue": None,
        "title": block_type,
        "text_size": 10
    }
    if block_type == "Histogram":
        config = {"x": cols[0] if cols else None, "hue": None, "title": "Histogram", "text_size": 10}
    elif block_type == "Boxplot":
        config = {"x": cols[0] if cols else None, "y": cols[1] if len(cols) > 1 else None, "hue": None, "title": "Boxplot", "text_size": 10}
    elif block_type == "Scatter Plot":
        config = {"x": cols[0] if cols else None, "y": cols[1] if len(cols) > 1 else None, "hue": None, "title": "Scatter Plot", "text_size": 10}
    elif block_type == "Bar Plot":
        config = {"x": cols[0] if cols else None, "y": cols[1] if len(cols) > 1 else None, "hue": None, "title": "Bar Plot", "text_size": 10}
    elif block_type == "Line Plot":
        config = {"x": cols[0] if cols else None, "y": cols[1] if len(cols) > 1 else None, "hue": None, "title": "Line Plot", "text_size": 10}
    elif block_type == "Pie Chart":
        cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        num_cols = df.select_dtypes(include=['number']).columns.tolist()
        config = {"names": cat_cols[0] if cat_cols else None, "values": num_cols[0] if num_cols else None, "title": "Pie Chart", "text_size": 10}
    return config

def render_block(df, block_type, config):
    if block_type == "Histogram":
        if config["x"] in df.columns:
            fig = px.histogram(df, x=config["x"], color=config.get("hue"), title=config["title"])
            fig.update_layout(font=dict(size=config["text_size"]))
            st.plotly_chart(fig, use_container_width=True)
    elif block_type == "Boxplot":
        if config["x"] in df.columns and config["y"] in df.columns:
            fig = px.box(df, x=config["x"], y=config["y"], color=config.get("hue"), title=config["title"])
            fig.update_layout(font=dict(size=config["text_size"]))
            st.plotly_chart(fig, use_container_width=True)
    elif block_type == "Scatter Plot":
        if config["x"] in df.columns and config["y"] in df.columns:
            fig = px.scatter(df, x=config["x"], y=config["y"], color=config.get("hue"), title=config["title"])
            # Compute R^2
            if config["hue"] is None:
                if pd.api.types.is_numeric_dtype(df[config["x"]]) and pd.api.types.is_numeric_dtype(df[config["y"]]):
                    valid = df[[config["x"], config["y"]]].dropna()
                    if len(valid) > 1:
                        r2 = r2_score(valid[config["y"]], valid[config["x"]])
                        fig.add_annotation(
                            text=f"R² = {r2:.3f}",
                            xref="paper", yref="paper",
                            x=0.95, y=0.95, showarrow=False,
                            font=dict(size=14, color="crimson")
                        )
            else:
                hue_col = config["hue"]
                if hue_col in df.columns:
                    groups = df[[config["x"], config["y"], hue_col]].dropna().groupby(hue_col)
                    y_offset = 0.95
                    for idx, (name, group) in enumerate(groups):
                        if pd.api.types.is_numeric_dtype(group[config["x"]]) and pd.api.types.is_numeric_dtype(group[config["y"]]) and len(group) > 1:
                            r2 = r2_score(group[config["y"]], group[config["x"]])
                            fig.add_annotation(
                                text=f"{name}: R²={r2:.3f}",
                                xref="paper", yref="paper",
                                x=0.95, y=y_offset, showarrow=False,
                                font=dict(size=12),
                                bgcolor="white"
                            )
                            y_offset -= 0.07
            fig.update_layout(font=dict(size=config["text_size"]))
            st.plotly_chart(fig, use_container_width=True)
    elif block_type == "Bar Plot":
        if config["x"] in df.columns and config["y"] in df.columns:
            fig = px.bar(df, x=config["x"], y=config["y"], color=config.get("hue"), title=config["title"])
            fig.update_layout(font=dict(size=config["text_size"]))
            st.plotly_chart(fig, use_container_width=True)
    elif block_type == "Line Plot":
        if config["x"] in df.columns and config["y"] in df.columns:
            fig = px.line(df, x=config["x"], y=config["y"], color=config.get("hue"), title=config["title"])
            # Compute R^2
            if config["hue"] is None:
                if pd.api.types.is_numeric_dtype(df[config["x"]]) and pd.api.types.is_numeric_dtype(df[config["y"]]):
                    valid = df[[config["x"], config["y"]]].dropna()
                    if len(valid) > 1:
                        r2 = r2_score(valid[config["y"]], valid[config["x"]])
                        fig.add_annotation(
                            text=f"R² = {r2:.3f}",
                            xref="paper", yref="paper",
                            x=0.95, y=0.95, showarrow=False,
                            font=dict(size=14, color="crimson")
                        )
            else:
                hue_col = config["hue"]
                if hue_col in df.columns:
                    groups = df[[config["x"], config["y"], hue_col]].dropna().groupby(hue_col)
                    y_offset = 0.95
                    for idx, (name, group) in enumerate(groups):
                        if pd.api.types.is_numeric_dtype(group[config["x"]]) and pd.api.types.is_numeric_dtype(group[config["y"]]) and len(group) > 1:
                            r2 = r2_score(group[config["y"]], group[config["x"]])
                            fig.add_annotation(
                                text=f"{name}: R²={r2:.3f}",
                                xref="paper", yref="paper",
                                x=0.95, y=y_offset, showarrow=False,
                                font=dict(size=12),
                                bgcolor="white"
                            )
                            y_offset -= 0.07
            fig.update_layout(font=dict(size=config["text_size"]))
            st.plotly_chart(fig, use_container_width=True)
    elif block_type == "Pie Chart":
        if config.get("names") in df.columns and config.get("values") in df.columns:
            fig = px.pie(df, names=config["names"], values=config["values"], title=config["title"])
            fig.update_layout(font=dict(size=config["text_size"]))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.write("[Pie Chart: Please select a categorical column for names and a numeric column for values]")
    else:
        st.write(f"[{block_type} plot here]")

def generate_notebook(df, layout, block_configs, dataset_name):
    nb = new_notebook()
    cells = []
    # First cell: pip install from requirements.txt
    pip_cell = new_code_cell(f"!pip install -r requirements.txt")
    cells.append(pip_cell)
    # Markdown intro
    cells.append(new_markdown_cell(f"# EDA for {dataset_name}\nThis notebook was generated by the Streamlit EDA Builder."))
    # Code to load data
    cells.append(new_code_cell(
        "import pandas as pd\n"
        "import plotly.express as px\n"
        f"df = pd.read_csv('{dataset_name}')\n"
        "df.head()"
    ))
    # Add a cell for each graph
    for i, row in enumerate(layout):
        for j, block in enumerate(row):
            block_id = f"row{i}_block{j}"
            config = block_configs[block_id]
            cells.append(new_markdown_cell(f"## {config['title']}"))
            # Build code for each plot type
            code = ""
            if block == "Histogram":
                code = f"px.histogram(df, x='{config['x']}', color={repr(config['hue'])}).show()"
            elif block == "Boxplot":
                code = f"px.box(df, x='{config['x']}', y='{config['y']}', color={repr(config['hue'])}).show()"
            elif block == "Scatter Plot":
                code = f"px.scatter(df, x='{config['x']}', y='{config['y']}', color={repr(config['hue'])}).show()"
            elif block == "Bar Plot":
                code = f"px.bar(df, x='{config['x']}', y='{config['y']}', color={repr(config['hue'])}).show()"
            elif block == "Line Plot":
                code = f"px.line(df, x='{config['x']}', y='{config['y']}', color={repr(config['hue'])}).show()"
            elif block == "Pie Chart":
                code = f"px.pie(df, names='{config['names']}', values='{config['values']}', title={repr(config['title'])}).show()"
            cells.append(new_code_cell(code))
    nb['cells'] = cells
    return nb

def get_zip_download_link(nb, requirements, filename_nb='eda_export.ipynb', filename_req='requirements.txt', zipname='eda_export.zip'):
    nb_json = nbformat.writes(nb)
    requirements_txt = '\n'.join(requirements) + '\n'
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zf:
        zf.writestr(filename_nb, nb_json)
        zf.writestr(filename_req, requirements_txt)
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:application/zip;base64,{b64}" download="{zipname}">Download notebook & requirements.zip</a>'

def main_ui():
    st.markdown("""
        <style>
        .block-container {padding-top: 1rem;}
        .drag-block {border: 1px dashed #bbb; border-radius: 6px; padding: 0.5rem; margin: 0.5rem 0; background: #fafafa; cursor: grab;}
        .row-sep {border-top: 1px solid #eee; margin: 1rem 0;}
        </style>
    """, unsafe_allow_html=True)

    # --- HEADER BAR ---
    col1, col2, col3 = st.columns([2, 2, 2])
    with col1:
        st.markdown("<h2 style='margin-bottom:0;'>Custom Streamlit EDA Builder</h2>", unsafe_allow_html=True)
    with col3:
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"], label_visibility="collapsed")
        export_format = st.selectbox("Export", [".py", ".ipynb"], index=0)
        st.button("Help", help="How to use this app")
    st.markdown("---")

    # --- DATA LOADING & INFO ---
    sample = None
    if "first_load_done" not in st.session_state:
        st.session_state["first_load_done"] = True
        if uploaded_file is None:
            sample_list = list(SAMPLE_DATASETS.keys())
            sample = sample_list[0]
            st.session_state["prev_sample_select"] = sample
            sample = st.selectbox("Select a sample dataset", sample_list, key="sample_select")
            data_path = get_sample_path(sample)
            df = pd.read_csv(data_path)
            st.session_state["dataset_name"] = sample
            st.session_state["df"] = df
            st.session_state["prev_sample_select"] = sample
        else:
            df = pd.read_csv(uploaded_file)
            st.session_state["dataset_name"] = uploaded_file.name
            st.session_state["df"] = df
    else:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state["dataset_name"] = uploaded_file.name
            st.session_state["df"] = df
        else:
            sample_list = list(SAMPLE_DATASETS.keys())
            prev_sample = st.session_state.get("prev_sample_select", sample_list[0])
            sample = st.selectbox("Select a sample dataset", sample_list, index=sample_list.index(prev_sample), key="sample_select")
            # If the sample changed and there are graphs, ask for confirmation
            if sample != prev_sample and st.session_state.get("layout", []):
                st.warning("Changing the sample dataset will clear all current graphs. Do you want to proceed?")
                col_confirm, col_cancel = st.columns([1,1])
                confirm = col_confirm.button("Yes, change dataset and clear graphs", key="confirm_sample_change")
                cancel = col_cancel.button("Cancel", key="cancel_sample_change")
                if confirm:
                    data_path = get_sample_path(sample)
                    df = pd.read_csv(data_path)
                    st.session_state["dataset_name"] = sample
                    st.session_state["df"] = df
                    st.session_state["layout"] = []
                    st.session_state["block_configs"] = {}
                    st.session_state["prev_sample_select"] = sample
                    st.rerun()
                elif cancel:
                    st.session_state["sample_select"] = prev_sample
                    st.rerun()
                else:
                    # Don't update dataset until confirmed
                    df = st.session_state["df"]
                    sample = prev_sample
            else:
                data_path = get_sample_path(sample)
                df = pd.read_csv(data_path)
                st.session_state["dataset_name"] = sample
                st.session_state["df"] = df
                st.session_state["prev_sample_select"] = sample
    st.write(f"**File:** {st.session_state['dataset_name']}")
    st.write(f"**Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    st.dataframe(df.head(), use_container_width=True)
    st.markdown("---")

    # --- LAYOUT BUILDER ---
    st.subheader("EDA Layout Builder")
    if "layout" not in st.session_state:
        st.session_state["layout"] = []  # List of rows, each row is a list of blocks
    if "block_configs" not in st.session_state:
        st.session_state["block_configs"] = {}
    if st.button("+ Add Row"):
        st.session_state["layout"].append([])
        st.rerun()
    for i, row in enumerate(st.session_state["layout"]):
        st.markdown(f"<div class='row-sep'></div>", unsafe_allow_html=True)
        st.markdown(f"### Row {i+1}")
        cols = st.columns(len(row)+1 if row else 1)
        for j, block in enumerate(row):
            block_id = f"row{i}_block{j}"
            if block_id not in st.session_state["block_configs"]:
                st.session_state["block_configs"][block_id] = default_block_config(df, block)
            config = st.session_state["block_configs"][block_id]
            with cols[j]:
                remove_key = f"remove_{block_id}"
                colA, colB = st.columns([8, 1])
                with colA:
                    st.markdown(f"<div class='drag-block'>{block}</div>", unsafe_allow_html=True)
                with colB:
                    if st.button("❌", key=remove_key):
                        st.session_state["layout"][i].pop(j)
                        st.rerun()
                st.markdown(f"**{block} Config**")
                cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                if block == "Histogram":
                    config["x"] = st.selectbox(f"X-axis ({block_id})", df.columns, index=df.columns.get_loc(config["x"]) if config["x"] in df.columns else 0, key=f"x_{block_id}")
                    config["hue"] = st.selectbox(f"Hue ({block_id})", [None]+cat_cols, index=([None]+cat_cols).index(config["hue"]) if config["hue"] in [None]+cat_cols else 0, key=f"hue_{block_id}")
                elif block == "Boxplot":
                    config["x"] = st.selectbox(f"X-axis ({block_id})", df.columns, index=df.columns.get_loc(config["x"]) if config["x"] in df.columns else 0, key=f"x_{block_id}")
                    config["y"] = st.selectbox(f"Y-axis ({block_id})", df.columns, index=df.columns.get_loc(config["y"]) if config["y"] in df.columns else 0, key=f"y_{block_id}")
                    config["hue"] = st.selectbox(f"Hue ({block_id})", [None]+cat_cols, index=([None]+cat_cols).index(config["hue"]) if config["hue"] in [None]+cat_cols else 0, key=f"hue_{block_id}")
                elif block == "Scatter Plot":
                    config["x"] = st.selectbox(f"X-axis ({block_id})", df.columns, index=df.columns.get_loc(config["x"]) if config["x"] in df.columns else 0, key=f"x_{block_id}")
                    config["y"] = st.selectbox(f"Y-axis ({block_id})", df.columns, index=df.columns.get_loc(config["y"]) if config["y"] in df.columns else 0, key=f"y_{block_id}")
                    config["hue"] = st.selectbox(f"Hue ({block_id})", [None]+cat_cols, index=([None]+cat_cols).index(config["hue"]) if config["hue"] in [None]+cat_cols else 0, key=f"hue_{block_id}")
                elif block == "Bar Plot":
                    config["x"] = st.selectbox(f"X-axis ({block_id})", df.columns, index=df.columns.get_loc(config["x"]) if config["x"] in df.columns else 0, key=f"x_{block_id}")
                    config["y"] = st.selectbox(f"Y-axis ({block_id})", df.columns, index=df.columns.get_loc(config["y"]) if config["y"] in df.columns else 0, key=f"y_{block_id}")
                    config["hue"] = st.selectbox(f"Hue ({block_id})", [None]+cat_cols, index=([None]+cat_cols).index(config["hue"]) if config["hue"] in [None]+cat_cols else 0, key=f"hue_{block_id}")
                elif block == "Line Plot":
                    config["x"] = st.selectbox(f"X-axis ({block_id})", df.columns, index=df.columns.get_loc(config["x"]) if config["x"] in df.columns else 0, key=f"x_{block_id}")
                    config["y"] = st.selectbox(f"Y-axis ({block_id})", df.columns, index=df.columns.get_loc(config["y"]) if config["y"] in df.columns else 0, key=f"y_{block_id}")
                    config["hue"] = st.selectbox(f"Hue ({block_id})", [None]+cat_cols, index=([None]+cat_cols).index(config["hue"]) if config["hue"] in [None]+cat_cols else 0, key=f"hue_{block_id}")
                elif block == "Pie Chart":
                    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                    num_cols = df.select_dtypes(include=['number']).columns.tolist()
                    config["names"] = st.selectbox(f"Names (category) ({block_id})", cat_cols, index=cat_cols.index(config["names"]) if config["names"] in cat_cols else 0, key=f"names_{block_id}") if cat_cols else None
                    config["values"] = st.selectbox(f"Values (numeric) ({block_id})", num_cols, index=num_cols.index(config["values"]) if config["values"] in num_cols else 0, key=f"values_{block_id}") if num_cols else None
                config["title"] = st.text_input(f"Title ({block_id})", config["title"], key=f"title_{block_id}")
                config["text_size"] = st.slider(f"Text Size ({block_id})", 8, 20, config["text_size"], key=f"text_size_{block_id}")
                render_block(df, block, config)
        with cols[-1]:
            add_block_key = f"add_block_{i}"
            with st.form(key=f"form_add_block_{i}", clear_on_submit=True):
                add_block = st.selectbox(f"Add graph to row {i+1}", [None]+COMPONENTS, key=add_block_key)
                submitted = st.form_submit_button("Add")
                if submitted and add_block:
                    st.session_state["layout"][i].append(add_block)
                    st.rerun()
        if st.button(f"Remove Row {i+1}", key=f"rm_row_{i}"):
            st.session_state["layout"].pop(i)
            st.rerun()
    st.markdown("<div class='row-sep'></div>", unsafe_allow_html=True)

    # --- BOTTOM TABS ---
    tabs = st.tabs(["Preview Dashboard", "Export"])
    with tabs[0]:
        st.write("[Preview of dashboard will appear here]")
        # Optionally, render all blocks as a dashboard preview
        for i, row in enumerate(st.session_state["layout"]):
            st.markdown(f"#### Row {i+1}")
            cols = st.columns(len(row) if row else 1)
            for j, block in enumerate(row):
                block_id = f"row{i}_block{j}"
                config = st.session_state["block_configs"][block_id]
                with cols[j]:
                    render_block(df, block, config)
    with tabs[1]:
        st.write("[Exported code as .py will appear here]")
        nb = generate_notebook(df, st.session_state["layout"], st.session_state["block_configs"], st.session_state["dataset_name"])
        st.markdown(get_zip_download_link(nb, REQUIREMENTS), unsafe_allow_html=True) 