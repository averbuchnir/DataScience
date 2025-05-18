# Array Randomizer

**Array Randomizer** is a Python desktop application for generating randomized experimental layouts, such as block designs or full randomizations, commonly used in plant science and agricultural experiments. The application provides a graphical user interface (GUI) built with Tkinter, allowing users to input experimental parameters and export randomized layouts and maps as CSV files.

---

## ✨ Features

- **Block Design and Full Randomization**: Supports both block design and full randomization of treatments.
- **Customizable Parameters**: Input the number of lines, treatments, repetitions, and rows.
- **CSV Export**: Outputs randomized layouts and maps to CSV files.
- **Image Export**: Save the generated layout as an image file.
- **File-Based Input**: Load experimental parameters directly from an `Info.csv` file.
- **User-Friendly GUI**: Intuitive interface with clear error handling and instructions.
- **YouTube Guide**: [Watch tutorial](https://youtu.be/B_aKeMaB5yU)

---

## 🧰 Requirements

- Python 3.x
- numpy  
- pandas  
- pygetwindow  
- Pillow  

Install dependencies with:

```bash
pip install numpy pandas pygetwindow Pillow
```

---

## ▶️ How to Use

### Run from Python:

```bash
python "Randomizer 3.1.py"
```

1. **Input Parameters**  
   - Enter the number of lines, treatments, repetitions, and rows  
   - Fill in names for each line and treatment  
   - Choose between Block Design or Full Randomization

2. **Export Results**  
   - Use buttons to generate CSV files and export layout images

3. **Use `Info.csv` for Input**  
   - Use the "Take me to my files" button to open the folder and edit `Info.csv`

---

## ⚠️ Notes

- Do **not** use commas `,`, underscores `_`, or dashes `-` in line/treatment names.
- All output files are saved in the same directory as the script or `.exe`.
- Close any open output files before generating new results to avoid file access errors.

---

## 🛠️ Compile to .EXE using `py-to-exe`

You can convert this script into a standalone Windows `.exe` application using [`auto-py-to-exe`](https://github.com/brentvollebregt/auto-py-to-exe), a GUI for [PyInstaller](https://pyinstaller.org/).

### Step-by-step Instructions

1. Install `auto-py-to-exe`:

```bash
pip install auto-py-to-exe
```

2. Launch the GUI:

```bash
auto-py-to-exe
```

3. Configure the build:

- **Script Location**: Select `Randomizer 3.1.py`
- ✅ Check **"Onefile"** to bundle into a single `.exe`
- ❌ Uncheck **"Console Window"** (unless you want terminal output)
- (Optional) Add external files under **"Additional Files"**
- Click **"Convert .py to .exe"**

4. Your compiled `.exe` will appear in the `output` folder.

---

## 👤 Author

**Nir Averbuch**  
📧 [averbuch.nir@gmail.com](mailto:averbuch.nir@gmail.com)

If you use this tool in your research, please cite appropriately.

---

## 📜 License

This project is released as-is for educational and research use only.
