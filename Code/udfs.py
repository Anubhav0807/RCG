import os, sys
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
try:
    import mysql.connector as msc
except ModuleNotFoundError:
    messagebox.showwarning("Module Not Found", "Module named mysql.connector was not found. \nGo to the command prompt and run the command: \npip install mysql-connector-python")
    quit()

# Variables

Palettes = [
    ['#FFAE6D', '#E3C770', '#FECD70', '#F3E0B5'],   # Yellow
    ['#B1B2FF', '#AAC4FF', '#D2DAFF', '#EEF1FF'],   # Blue 1
    ['#898AA6', '#C9BBCF', '#B7D3DF', '#D6EFED'],   # Blue 2
    ['#2F8F9D', '#3BACB6', '#82DBD8', '#B3E8E5'],   # Blue 3
    ['#14C38E', '#00FFAB', '#B8F1B0', '#E3FCBF'],   # Green 1
    ['#8EC3B0', '#9ED5C5', '#BCEAD5', '#DEF5E5'],   # Green 2
    ['#DBA39A', '#F0DBDB', '#F5EBE0', '#FEFCF3'],   # Pink
]

ShortForm = {
    "Pre-Midterm"   :   "pmt",
    "Midterm"       :   "mt",
    "Pre-Quarterly" :   "pq",
    "Quarterly"     :   "q",
    "Rivision-1"    :   "r1",
    "Half-Yearly"   :   "hy",
    "Revision-2"    :   "r2",
    "Pre-Board"     :   "pb"
}

RomanToNum = {
    "I"    : "1",
    "II"   : "2",
    "III"  : "3",
    "IV"   : "4",
    "V"    : "5",
    "VI"   : "6",
    "VII"  : "7",
    "VIII" : "8",
    "IX"   : "9",
    "X"    : "10",
    "XI"   : "11",
    "XII"  : "12",
}

Exams = ["Pre-Midterm", "Midterm", "Pre-Quarterly", "Quarterly", "Rivision-1", "Half-Yearly", "Revision-2", "Pre-Board"]
Sci_Subs = ("Physics", "Chemistry", "Mathematics", "Psychology", "English", "Computer Science", "Engineering Graphics", "Biology")
Comm_Subs = ("English", "Business Studies", "Economics", "Accountancy", "Legal Studies Maths", "Applied Maths", "Entrepreneurship")

# UDFs

def Animate(widget):
    "Changes the color of widget when mouse pointer enters and leaves"
    if widget["state"] == "disabled": return False
    widget.configure(cursor="hand2")
    color = widget["bg"]
    if color=="SystemButtonFace": hover_color = GetColor("#F0F0F0")
    else: hover_color = GetColor(color)
    widget.bind("<Enter>", lambda e: on_enter(e, hover_color))
    widget.bind("<Leave>", lambda e: on_leave(e, color))

def InAnimate(widget):
    "Removes the animation"
    widget.configure(cursor="arrow")
    widget.unbind("<Enter>")
    widget.unbind("<Leave>")

def on_enter(event, c1):
    event.widget["bg"] = c1
    
def on_leave(event, c2):
    event.widget["bg"] = c2

def GetColor(color):
    d = 1
    color = color.replace('#', '')
    lst = list(color)
    for i in range(6):
        byte = int(lst[i], 16)  # Hexadecimal has a base 16
        if byte<=15-d:
            lst[i] = hex(byte+d)[2:]
        elif byte>=d:
            lst[i] = hex(byte-d)[2:]
    hover_color = ''.join(lst)
    return '#'+hover_color

def GetTableName(exam, clas, sec):
    if sec in ('A', 'B', 'C', 'D'):
        group = "sci"
    elif sec in ('E', 'F'):
        group = "comm"
    table_name = ""
    table_name += ShortForm[exam]  + '_'
    table_name += RomanToNum[clas] + '_'
    table_name += group
    return table_name

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def Exit(root, db, specs):
    specs.save_data()
    try: db.mycon.close()
    except AttributeError: pass
    root.destroy()