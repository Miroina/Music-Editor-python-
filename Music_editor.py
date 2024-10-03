# coding=windows-1251

from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory

import os
import shutil

local_path = os.path.join(os.getcwd(), "tmp")

def Change_file_info():
    print("Poop")

def load_files():
    # ����� ���������� ��� ����������
    folder = askdirectory(title="����� ��� ��������", initialdir="/")
    if folder == "":
        return

    # ����������� ������ � ��������� ���������
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    
    shutil.copytree(folder, local_path)

    # ����� ������ � ������
    insert_files(local_path, "")

def insert_files(path, parrent):
    for el in os.listdir(path):
        if os.path.isdir(os.path.join(path, el)):
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, open=True, tag="FOLDER")
            insert_files(os.path.join(path,el), os.path.join(path,el))
        else:
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, tag="FILE")
            tree.set(os.path.join(path,el), column="#1", value="������")

if __name__=="__main__":
    main_window = Tk()
    
    # ��������� ����
    main_window.title("�������� ����� ������ mp3")
    main_window.geometry("1600x780+200+100")
    main_window.iconbitmap(default="foldermusic.ico")
    main_window.attributes("-toolwindow", True)

    # �������� ������
    style = ttk.Style(main_window)
    style.configure('Files.Treeview.Heading', 
                    background="lightpink1",
                    activebackground="lightpink1")
    style.configure('Files.TFrame', background="antiquewhite")
    style.configure('Files.TCheckbutton', background="antiquewhite")

    # �������� ����
    main_menu = Menu(main_window)

    file_menu = Menu(main_menu)
    file_menu.add_command(label="��������� � �������", command=load_files)
    file_menu.add_command(label="���������")

    main_menu.add_cascade(label="����", menu=file_menu)
    main_window.config(menu=main_menu)

    # ����� � ����� ������
    files_frame = ttk.Frame(
        borderwidth=2,
        relief=RAISED,
        padding=[2, 3],
        style="Files.TFrame")

    select_files_var = BooleanVar()
    select_files = ttk.Checkbutton(files_frame,
        text="������� ���������", 
        var=select_files_var,
        style="Files.TCheckbutton")

    tree = ttk.Treeview(files_frame, 
        show="tree headings", 
        columns=("#1"),
        selectmode="browse",
        style="Files.Treeview")

    tree.heading("#0", text="��� ������")
    tree.heading("#1", text="������")
    tree.column("#0", width=300)
    tree.column("#1", width=90)

    tree.tag_configure("FOLDER", background="lightpink1")
    tree.tag_configure("FILE", background="beige")

    select_files.pack(anchor="center", pady=4)
    tree.pack(expand=True, fill='both', padx=2, pady=1)

    # ����� ���������� � �����
    info_frame = Frame()

    info = Label(info_frame, text="����� ����� ��������� � �����", width=60)
    change = Button(info_frame, 
        text="��������� ���������", 
        state="disabled", 
        command=Change_file_info,
        height=4)

    info.pack(expand=True, fill='both')
    change.pack(fill='x', side='bottom')

    # ������������ frame
    files_frame.pack(side="left", fill='y', padx=3, pady=4)
    info_frame.pack(expand=True, fill='both')

    main_window.mainloop()