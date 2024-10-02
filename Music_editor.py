from importlib.metadata import files
from lzma import FILTER_LZMA2
from msilib.schema import File
import select
from textwrap import fill
from tkinter import *
import tkinter.ttk as ttk

files_list = (
    "f1",
    "f2",
    "d/f3",
    "d/f4"
)

def Change_file_info():
    print("Poop")

def print_files():
    for f in files_list:
        if "/" in f:
            pos = f.find("/")
            f_dir = f[:pos]
            if not f_dir in tree.get_children(""):
                tree.insert("", END, id=f_dir, text=f_dir)
            tree.insert(f_dir, END, id=f[pos+1:], text=f[pos+1:])
        else:
            tree.insert("", END, id=f, text=f)

main_window = Tk()

# Настройка окна
main_window.title("Edit music files")

#Выбор и вывод файлов
files_frame = Frame(width=20, height=40)

select_files_var = BooleanVar()
select_files = ttk.Checkbutton(files_frame, 
                               text="Select several", 
                               var=select_files_var)

tree = ttk.Treeview(files_frame, 
                    show="tree", 
                    columns=("#1"))
tree.heading("#1", text="File name")

select_files.pack(expand=True, fill='x')
tree.pack(expand=True, fill='both')

#Вывод информации о файле
info_frame = Frame(width=60, height=20)

info = Label(info_frame, text="Here wil be info about file")
change = Button(info_frame, 
                text="Change params", 
                state="disabled", 
                command=Change_file_info,
                height=4)

info.pack(expand=True, fill='both')
change.pack(fill='x', side='bottom')

#Расположение frame
files_frame.pack(side="left", expand=True, fill='y')
info_frame.pack(expand=True, fill='both')

main_window.mainloop()

print_files