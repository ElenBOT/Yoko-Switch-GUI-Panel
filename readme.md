# Yoko Switch GUI Panel
An GUI panel for using YOKOGAWA to operate microwave switch.

# Usage
1. Auto setup: double click `auto_setup.bat` again to open GUI.

2. Manual setup: `python -m streamlit run app.py` to open GUI.
![alt text](image.png)

# Auto setup
Require windows >= 7 computer, anaconda or miniconda, git.
1. create a folder to be the workspace.
2. download `auto_setup.bat`, put it inside that folder, double click to run it.
> [!Tip]
> This batch file can be used as setup, as well as open GUI.

# Manual setup
Clone via git or download as zip.
```
git clone https://github.com/ElenBOT/Yoko-Switch-GUI-Panel.git
```
Then optionally delete `auto_setup.bat` inside it. Then install required packages
```
pip install numpy streamlit pyvisa
```
To run, use
```
python -m streamlit run app.py
```
