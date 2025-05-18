# Custom Streamlit EDA Builder

A powerful, interactive Streamlit app for building custom Exploratory Data Analysis (EDA) dashboards—no coding required!
Upload your own CSV or use built-in sample datasets, add and configure multiple plot types, and export your dashboard as a reproducible Jupyter notebook.

---

## Features

- **No-code EDA dashboard builder**: Add multiple rows and graphs, each with independent configuration using buttons and selectboxes (not drag-and-drop).
- **Supported plot types**: Histogram, Boxplot, Scatter Plot (with R²), Bar Plot, Line Plot (with R²), Pie Chart.
- **Flexible axes**: Choose any column (categorical or numeric) for X and Y axes.
- **Hue support**: Add a categorical column as hue for grouped plots and see R² per group (where applicable).
- **Live preview**: Instantly see your dashboard as you build it.
- **Export**: Download your dashboard as a Jupyter notebook (`.ipynb`) and requirements file (`requirements.txt`) in a single zip. The notebook is fully reproducible and includes all your plots.
- **Sample datasets**: Titanic, Iris, Wine Quality, Tips, Diabetes.

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run eda_builder/run.py
```

---

## Usage

1. **Upload a CSV** or select a sample dataset.
2. **Add rows and graphs**: Click "+ Add Row", then add any plot type to each row.
3. **Configure each graph**: Choose X, Y, hue, and other options. For Pie Chart, select a categorical column for "names" and a numeric column for "values".
4. **Remove graphs or rows** as needed.
5. **Preview your dashboard** in the "Preview Dashboard" tab.
6. **Export**: Go to the "Export" tab and download a zip containing your Jupyter notebook and requirements file.

---

## Requirements

- Python 3.8+
- See `requirements.txt` for details.

---

## Example Plots

- Histogram
- Boxplot
- Scatter Plot (with R², per group if hue is set)
- Bar Plot
- Line Plot (with R², per group if hue is set)
- Pie Chart

---

## License

MIT License

---

## Acknowledgements

- Built with [Streamlit](https://streamlit.io/) and [Plotly](https://plotly.com/python/).
- Sample datasets from [Seaborn](https://github.com/mwaskom/seaborn-data) and UCI.

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## Contact

For questions or suggestions, open an issue or contact [your-email@example.com](mailto:your-email@example.com). 