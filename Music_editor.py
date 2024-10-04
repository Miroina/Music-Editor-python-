# coding=windows-1251

from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE
from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory

import os
import shutil
import eyed3
import io
from PIL import ImageTk, Image
from mutagen.id3 import ID3

def load_files():

    # Выбор директории для скачивания
    folder = askdirectory(title="Папка для загрузки", initialdir="/")
    if folder == "":
        return
    
    Clear(True)

    # Копирование файлов в локальную диркторию
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    
    shutil.copytree(folder, local_path)

    # Вывод файлов в дерево
    tree.insert("", END, id=local_path, text=os.path.basename(folder), open=True, tag="FOLDER")
    insert_files(local_path, local_path)

def insert_files(path, parrent):
    for el in os.listdir(path):
        if os.path.isdir(os.path.join(path, el)):
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, open=True, tag="FOLDER")
            insert_files(os.path.join(path,el), os.path.join(path,el))
        else:
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, tag="FILE")
            tree.set(os.path.join(path,el), column="#1", value="Скачан")

open_change_var = False
def Open_chage(event):
    global open_change_var
    open_change_var = True

def Select_file(event):
    global open_change_var
    if open_change_var:
        open_change_var = False
        return

    tmp_select = tree.selection()
    if tmp_select == ():
        return
    tmp_select = tmp_select[0]

    if tree.get_children(tmp_select) != ():
        if select_files_var.get():
            Select_children(tmp_select)
            
            Clear(False)
            Unlock_file_info(False, "")
        else:
            return
    else:
        if not select_files_var.get():
            for el in tree_select.get_children(""):
                tree_select.delete(el)

            tree_select.insert("", END, id=tmp_select, text=tree.item(tmp_select,'text'), tag="FILE")
            
            Clear(False)
            Unlock_file_info(True, tmp_select)
        else:
            if tmp_select in tree_select.get_children(""):
                tree_select.delete(tmp_select)
            else:
                tree_select.insert("", END, id=tmp_select, text=tree.item(tmp_select,'text'), tag="FILE")

            Clear(False)
            Unlock_file_info(False, "")
    
    if tree_select.get_children("") == ():
        Clear(False)

def Unlock_file_info(is_select_file, filename):

    artist_unknown.configure(state="normal")
    album_unknown.configure(state="normal")
    artwork_unknown.configure(state="normal")

    artist_text.configure(state="normal")
    album_text.configure(state="normal")
    change.configure(state="normal")

    if is_select_file:
        name_label.configure(text="Имя файла: " + os.path.basename(filename))
        title_text.configure(state="normal")

        audio = eyed3.load(filename)
        if audio.tag.title == None:
            audio.tag.title = " "
        if audio.tag.artist == None:
            audio.tag.artist = " "
        if audio.tag.album == None:
            audio.tag.album = " "

        title_text.insert(END, audio.tag.title)
        artist_text.insert(END, audio.tag.artist)
        album_text.insert(END, audio.tag.album)

        print(audio.tag.images)
        if audio.tag.images != ():
            img = ImageTk.PhotoImage(Image.open(io.BytesIO(audio.tag.images[0].image_data)))
            Label(main_window, image=img).pack()

def Clear(flag):
    if flag:
        for el in tree.get_children(""):
            tree.delete(el)
        for  el in tree_select.get_children(""):
            tree_select.delete(el)

    name_label.configure(text="")

    title_text.configure(state="normal")
    artist_text.configure(state="normal")
    album_text.configure(state="normal")

    title_text.delete(0.0, END)
    artist_text.delete(0.0, END)
    album_text.delete(0.0, END)

    title_text.configure(state="disabled")
    artist_text.configure(state="disabled")
    album_text.configure(state="disabled")

    artist_unknown.configure(state="disabled")
    album_unknown.configure(state="disabled")
    artwork_unknown.configure(state="disabled")
    change.configure(state="disabled")

def Select_children(parrent):
    for el in tree.get_children(parrent):
        if tree.get_children(el) != ():
            Select_children(el)
        else:
            if el in tree_select.get_children(""):
                tree_select.delete(el)
            else:
                tree_select.insert("", END, id=el, text=tree.item(el,'text'), tag="FILE")

if __name__=="__main__":
    main_window = Tk()
    
    #Глобальные переменные
    local_path = os.path.join(os.getcwd(), "tmp")
    select_files_var = BooleanVar()
    artist_unknown_var = BooleanVar()
    album_unknown_var = BooleanVar()
    artwork_unknown_var = BooleanVar()
    
    # Настройка окна
    main_window.title("Редактор тэгов файлов mp3")
    main_window.geometry("1600x780+200+100")
    #main_window.iconbitmap(default="foldermusic.ico")
    main_window.config(background="oldlace")

    # Создание стилей
    style = ttk.Style(main_window)
    style.configure('Files.Treeview.Heading', 
                    background="lightpink1",
                    activebackground="lightpink1")
    style.configure('Files.TFrame', background="antiquewhite")
    style.configure('Menu.TLabelframe', background="seashell1")
    style.configure('Menu.TLabelframe.Label', background="seashell1")
    style.configure('Info.TFrame', background="mistyrose1")
    style.configure('Files.TCheckbutton', background="antiquewhite")
    style.configure('Info.TCheckbutton', background="mistyrose1", font=("Times New Roman", 14),)

    # Создание меню
    menu_frame = ttk.Labelframe(main_window,
        text="Работа с файлами",
        relief=RAISED,
        padding=[2, 3],
        style="Menu.TLabelframe")

    load_btn = Button(menu_frame, 
        text="Загрузить в систему", 
        state="normal", 
        command=load_files,
        height=1,
        background="thistle1")

    upload_btn = Button(menu_frame, 
        text="Выгрузить в папку", 
        state="normal", 
        command=print("pop"),
        height=1,
        background="thistle1")

    load_btn.pack(side="left", padx=2, pady=1)
    upload_btn.pack(side="left", padx=2, pady=1)

    # Выбор и вывод файлов
    files_frame = ttk.Frame(main_window,
        borderwidth=2,
        relief=RAISED,
        padding=[2, 3],
        style="Files.TFrame")

    select_files = ttk.Checkbutton(files_frame,
        text="Выбрать несколько", 
        variable=select_files_var,
        style="Files.TCheckbutton")
    
    tree = ttk.Treeview(files_frame, 
        show="tree headings", 
        columns=("#1"),
        selectmode="browse",
        style="Files.Treeview")

    tree.heading("#0", text="Имя файлов")
    tree.heading("#1", text="Статус")
    tree.column("#0", width=300)
    tree.column("#1", width=90)

    tree.tag_configure("FOLDER", background="lightpink1")
    tree.tag_configure("FILE", background="beige")

    tree.bind("<<TreeviewSelect>>", Select_file)
    tree.bind("<<TreeviewOpen>>", Open_chage)
    tree.bind("<<TreeviewClose>>", Open_chage)

    tree_select = ttk.Treeview(files_frame, 
        show="tree headings",
        selectmode="none",
        style="Files.Treeview")

    tree_select.heading("#0", text="Выбранные файлы")

    tree_select.tag_configure("FOLDER", background="lightpink1")
    tree_select.tag_configure("FILE", background="beige")

    select_files.pack(anchor="center", pady=4)
    tree.pack(expand=True, fill='both', padx=2, pady=1)
    tree_select.pack(fill='both', padx=2, pady=1)

    # Вывод информации о файле
    info_frame = ttk.Frame(main_window,
        borderwidth=2,
        relief=RAISED,
        padding=[2, 3],
        style="Info.TFrame")

    # Имя файла
    name_label = Label(info_frame,
        text="",
        anchor="center",
        font=("Times New Roman", 14),
        background="mistyrose1")

    # Название
    title_frame = ttk.Frame(info_frame,
        padding=[2, 2, 10, 6],
        style="Info.TFrame")

    title_label = Label(title_frame,
        text="Название композиции:  ",
        anchor="w",
        font=("Times New Roman", 14),
        background="mistyrose1")
    title_text = Text(title_frame,
        font=("Times New Roman", 14),
        state="disabled",
        background="oldlace",
        height=1, width=70)

    title_label.pack(side="left")
    title_text.pack(expand=True, fill="x")

    # Исполнитель
    artist_frame = ttk.Frame(info_frame,
        padding=[2, 2, 10, 6],
        style="Info.TFrame")

    artist_label = Label(artist_frame,
        text="Исполнитель:  ",
        anchor="w",
        font=("Times New Roman", 14),
        background="mistyrose1")
    artist_text = Text(artist_frame,
        font=("Times New Roman", 14),
        state="disabled",
        background="oldlace",
        height=1, width=70)

    artist_label.pack(side="left")
    artist_text.pack(expand=True, fill="x")

    artist_unknown = ttk.Checkbutton(info_frame,
        text="Неизвестный исполнитель", 
        variable=artist_unknown_var,
        style="Info.TCheckbutton")

    # Альбом
    album_frame = ttk.Frame(info_frame,
        padding=[2, 2, 10, 6],
        style="Info.TFrame")

    album_label = Label(album_frame,
        text="Альбом:  ",
        anchor="w",
        font=("Times New Roman", 14),
        background="mistyrose1")
    album_text = Text(album_frame,
        font=("Times New Roman", 14),
        state="disabled",
        background="oldlace",
        height=1, width=70)

    album_label.pack(side="left")
    album_text.pack(expand=True, fill="x")

    album_unknown = ttk.Checkbutton(info_frame,
        text="Неизвестный альбом", 
        variable=album_unknown_var,
        style="Info.TCheckbutton")

    # Обложка альбома
    artwork_frame = ttk.Frame(info_frame,
        borderwidth=2,
        relief=RAISED,
        padding=[0],
        style="Info.TFrame")

    artwork_load = Button(artwork_frame, 
        text="Загрузить обложку", 
        state="disabled", 
        command=print("pop"),
        font=("Times New Roman", 14),
        background="mistyrose2")

    artwork_canvas = Canvas(artwork_frame,
        height=400, 
        width=400,
        background="mistyrose2")

    artwork_unknown = ttk.Checkbutton(artwork_frame,
        text="Отсутствует обложка", 
        variable=artwork_unknown_var,
        style="Info.TCheckbutton")

    artwork_load.pack(fill='x', padx=3, pady=4)
    artwork_canvas.pack()
    artwork_unknown.pack(padx=3, pady=4)

    # Кнопки
    change = Button(info_frame, 
        text="Сохранить изменения", 
        state="disabled", 
        command=print("pop"),
        height=4,
        background="mistyrose2")
    
    name_label.pack(side="top")
    artwork_frame.pack(side="right")

    title_frame.pack(fill="x")
    artist_frame.pack(fill="x")
    artist_unknown.pack(fill="x", padx=3, pady=4)
    album_frame.pack(fill="x")
    album_unknown.pack(fill="x", padx=3, pady=4)

    change.pack(fill="x", padx=3, pady=4)

    # Расположение frame
    files_frame.pack(expand=True, side="left", fill='both', padx=3, pady=4)
    menu_frame.pack(fill='both', padx=3, pady=4)
    info_frame.pack(fill='both', padx=3, pady=4)

    main_window.mainloop()