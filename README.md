<p align="center">
<img src="img/logo.png"><br>
<h1 align="center">Renamer</h1>
</p>

You configure how each file needs to be renamed with Python code in [rename.py](rename.py).  
Edit the one-line function `rename_filename()` to define your rename.  
This allows you to rename precisely how you want, as Python code can be as simple or advanced as you want!

## Installing
Open terminal in the cloned folder and create a virtual Python environment called `venv` to prevent package issues:
```shell
python -m venv venv
```
Install required Linux packages: (todo: pyqt may be needed)
```shell
yay -S gobject-introspection 
```
Activate the created virtual environment:
```shell
venv\Scripts\activate
```
Install the required Python packages:
```shell
pip install -r requirements.txt
```

## Usage
Open a terminal in the cloned folder and activate the created virtual environment:
```shell
. venv\bin\activate
```
Edit the [rename.py](rename.py) file to define how files need to be named, and run the [renamer.py](renamer.py) script:
```shell
python renamer.py
```
This launches a file picker to choose the folder in which the files need to be renamed.  
After renaming the files, a `.rename_history_TIMESTAMP.txt` file will be put in the folder.  
This can be used to undo the renaming process.

## Undoing renaming
After renaming the files, a `.rename_history_TIMESTAMP.txt` file is saved in the folder.  
This can be used to undo the renaming by running the [undo_rename.py](undo_rename.py) script:
```shell
python undo_rename.py
```
This launches a folder picker, where you choose a folder in which the renaming needs to be undone.
In the selected folder, it seeks the last created `.rename_history_TIMESTAMP.txt` file, undoes the renaming according to this file, and deletes it.



