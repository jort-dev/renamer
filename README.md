<p align="center">
<img src="img/logo.png"><br>
<h1 align="center">Renamer</h1>
</p>

[Demo](https://youtu.be/oi0998oBm-c)  
You configure how each file needs to be renamed with Python code.  
In [rename.py](rename.py), edit the one-line function `rename_filename()` to define your rename.  
This allows you to rename without limitations, as Python code can be as simple or advanced as you want!

## Usage
* Edit the [rename.py](rename.py) file to define how files need to be named
* Run the [renamer.py](renamer.py) script by double clicking it  
* Select a folder in which to rename the files in

You will need to have the [latest Python version](https://www.python.org/downloads/) installed.

## Undoing renaming
* Double click the [undo_rename.py](undo_rename.py) script
* Select the folder in which to undo renaming in

## Advanced options
### Call from terminal
You can also run the scripts from the terminal, offering more options.  
See the available command line options:

```shell
python rename.py -h
```

### Installing additional features
The script comes with optional pip packages to improve functionality:
* iterate files as shown in file explorer
* allow picking multiple folders with system picker

Open terminal in the cloned folder and create a virtual Python environment called `venv` to prevent package issues:
```shell
python -m venv venv
```
Activate the created virtual environment:
```shell
venv\Scripts\activate
```
Install required Linux packages, pyqt may also be needed:
```shell
yay -S gobject-introspection 
```
Install the required Python packages:
```shell
pip install -r requirements.txt
```
On Windows, you might need to install some C++ redistributable (see error you will get)

### Debugging / testing
Run the script with the verbose option `-v` and testing option `-t` for example.  
See all options with `-v`.

### How does undoing renaming work?

How it works:
After renaming the files, a `.rename_history_TIMESTAMP.txt` file is saved in the folder.  
This can be used to undo the renaming by running the [undo_rename.py](undo_rename.py) script:
```shell
python undo_rename.py
```
This launches the folder picker again, where you choose a folder in which the renaming needs to be undone.
In the selected folder, it seeks the last created `.rename_history_TIMESTAMP.txt` file, undoes the renaming according to this file, and deletes it.






