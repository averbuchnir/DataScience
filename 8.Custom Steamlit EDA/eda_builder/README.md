# Custom Streamlit EDA Builder

A local-first, no-code data exploration tool. Upload a CSV or use built-in datasets, visually build your EDA dashboard, and export as Streamlit or Jupyter code.

## Features
- Drag-and-drop dashboard builder
- Real-time preview
- Export to `.py` or `.ipynb`
- Built-in sample datasets
- Optional ChatGPT-powered assistant

## Quick Start
```bash
git clone <repo-url>
cd eda_builder
pip install -r requirements.txt
streamlit run run.py
```

## Structure
```
eda_builder/
├── frontend/
│   ├── ui_builder.py
│   └── drag_components.py
├── backend/
│   ├── file_handler.py
│   ├── ai_assistant.py
│   └── exporter.py
├── sample_data/
│   ├── titanic.csv
│   ├── iris.csv
│   ├── winequality.csv
│   ├── tips.csv
│   └── diabetes.csv
├── run.py
├── README.md
└── requirements.txt
``` 