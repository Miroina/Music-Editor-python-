# coding=windows-1251

from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE
from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename

import os
import shutil
from PIL.ImageFile import LOAD_TRUNCATED_IMAGES
import eyed3
import io
from PIL import ImageTk, Image
import time
import pygame

# Загрузка файлов в локальную директорию
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

# Вставка имен файлов в дерево
def insert_files(path, parrent):
    for el in os.listdir(path):
        if os.path.isdir(os.path.join(path, el)):
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, open=True, tag="FOLDER")
            insert_files(os.path.join(path,el), os.path.join(path,el))
        else:
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, tag="FILE")
            tree.set(os.path.join(path,el), column="#1", value="Скачан")

# Обработка нажатия Treeview
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

# Разблокировка окон и вывод информации
def Unlock_file_info(is_select_file, filename):
    global ALBUM_IMAGE
    global MUSIC_LENGTH
    global UPDATER
    global FILE_NAME

    artist_unknown.configure(state="normal")
    album_unknown.configure(state="normal")
    artwork_unknown.configure(state="normal")

    artwork_load.configure(state="normal")
    artwork_return.configure(state="normal")

    artist_text.configure(state="normal")
    album_text.configure(state="normal")
    change.configure(state="normal")

    if is_select_file:
        FILE_NAME = filename
        name_label.configure(text="Имя файла: " + os.path.basename(filename))
        title_text.configure(state="normal")

        progress_scale.configure(state="normal")
        play_button.configure(state="normal")

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

        if list(audio.tag.images) != []:
            img = Image.open(io.BytesIO(audio.tag.images[0].image_data))
            img = img.resize((400, 400))
            ALBUM_IMAGE = ImageTk.PhotoImage(img)
            artwork_canvas.create_image(0, 0, anchor="nw", image=ALBUM_IMAGE)

        # Добавление аудио в звуковую дорожку
        MUSIC_LENGTH = audio.info.time_secs
        music_duration_label.configure(text=Duration_from_sec(MUSIC_LENGTH))
        progress_scale.configure(to=MUSIC_LENGTH)
        play_button.configure(image=play_icon)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        pygame.mixer.music.pause()

# Очистка и блокировка окон
def Clear(flag):
    global PAUSE_BUTTON_STATE
    global LOAD_IMAGE
    global ALBUM_IMAGE

    PAUSE_BUTTON_STATE = True
    LOAD_IMAGE = None
    ALBUM_IMAGE = None

    main_window.after_cancel(UPDATER)

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

    artwork_canvas.delete("all")
    artwork_load.configure(state="disabled")
    artwork_return.configure(state="disabled")

    progress_scale.configure(value=0)
    time_elapsed_label.configure(text="00:00")

    progress_scale.configure(state="disabled")
    play_button.configure(state="disabled")

    artist_unknown.configure(state="disabled")
    album_unknown.configure(state="disabled")
    artwork_unknown.configure(state="disabled")
    change.configure(state="disabled")

# Рекурсивный выбор всех детей
def Select_children(parrent):
    for el in tree.get_children(parrent):
        if tree.get_children(el) != ():
            Select_children(el)
        else:
            if el in tree_select.get_children(""):
                tree_select.delete(el)
            else:
                tree_select.insert("", END, id=el, text=tree.item(el,'text'), tag="FILE")

# Перевод из секунд в время (string)
def Duration_from_sec(secs):
    m, s = divmod(secs, 60)
    timelapsed = "{:02d}:{:02d}".format(int (m), int (s))

    return timelapsed

# Воспроизведение аудио
def Play_song():
    global PAUSE_BUTTON_STATE
    global UPDATER

    if PAUSE_BUTTON_STATE:
        PAUSE_BUTTON_STATE = False
        play_button.configure(image=stop_icon)

        pygame.mixer.music.unpause()
        Scale_update()
    else:
        main_window.after_cancel(UPDATER)
        PAUSE_BUTTON_STATE = True
        play_button.configure(image=play_icon)

        pygame.mixer.music.pause()

# Обновление полосы времени
def Scale_update():
    global UPDATER
    if progress_scale['value'] < MUSIC_LENGTH:
        progress_scale['value'] += 1

        time_elapsed_label['text'] = Duration_from_sec(progress_scale.get())
        UPDATER = main_window.after(1000, Scale_update)
    else:
        progress_scale['value'] = 0
        time_elapsed_label['text'] = "00:00"

# Изменение времени
def Scale_moved(x):
    global UPDATER
    global PAUSE_BUTTON_STATE

    main_window.after_cancel(UPDATER)
    at = progress_scale.get()
    pygame.mixer.music.play(0,at)
    if PAUSE_BUTTON_STATE:
        pygame.mixer.music.pause()
    else:
        Scale_update()

# Загрузить обложку альбома
def Load_artwork():
    global LOAD_IMAGE

    file_types = [("Изображение", "*.jpg"), ("Изображение", "*.jpeg"), ("Изображение", "*.png")]
    filename = askopenfilename(filetypes=file_types)
    
    if filename == "":
        return

    img = Image.open(filename)
    img = img.resize((400, 400))
    LOAD_IMAGE = ImageTk.PhotoImage(img)

    artwork_canvas.delete("all")
    artwork_canvas.create_image(0, 0, anchor="nw", image=LOAD_IMAGE)

def Return_atrwork():
    global ALBUM_IMAGE
    artwork_canvas.delete("all")

    if ALBUM_IMAGE != None:
        artwork_canvas.create_image(0, 0, anchor="nw", image=ALBUM_IMAGE)

if __name__=="__main__":
    pygame.init()
    main_window = Tk()
    
    #Глобальные переменные GUI
    local_path = os.path.join(os.getcwd(), "tmp")
    select_files_var = BooleanVar()
    artist_unknown_var = BooleanVar()
    album_unknown_var = BooleanVar()
    artwork_unknown_var = BooleanVar()

    play_icon = Image.open('image/play-button.png')
    play_icon = play_icon.resize((40, 40))
    play_icon = ImageTk.PhotoImage(play_icon)

    stop_icon = Image.open('image/pause.png')
    stop_icon = stop_icon.resize((40, 40))
    stop_icon = ImageTk.PhotoImage(stop_icon)

    UPDATER = main_window.after(0, '')
    main_window.after_cancel(UPDATER)
    
    # Настройка окна
    main_window.title("Редактор тэгов файлов mp3")
    main_window.geometry("1600x780+200+100")
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
    style.configure('TScale', background="mistyrose1")

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
        command=Load_artwork,
        font=("Times New Roman", 14),
        background="mistyrose2")

    artwork_return = Button(artwork_frame, 
        text="Вернуть обложку", 
        state="disabled", 
        command=Return_atrwork,
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

    artwork_canvas.pack()
    artwork_unknown.pack(padx=3, pady=4)
    artwork_load.pack(fill='x', padx=3, pady=4)
    artwork_return.pack(fill='x', padx=3, pady=4)

    # Воспроизвести аудио
    play_frame = ttk.Frame(info_frame,
        padding=[0],
        borderwidth=2,
        style="Info.TFrame")

    time_elapsed_label = Label(play_frame,
        text="00:00",
        padx=5,
        background="mistyrose1")
    music_duration_label = Label(play_frame,
        text="00:00",
        padx=15,
        background="mistyrose1")

    progress_scale = ttk.Scale(play_frame,
        orient="horizontal",
        from_=0,
        length=380,
        state="disable",
        command=Scale_moved,
        style="TScale")

    play_button = Button(play_frame,
        cursor='hand2',
        command=Play_song,
        borderwidth=0,
        image=play_icon,
        background="mistyrose1",
        state="disable",
        activebackground="mistyrose1")

    play_button.pack(side='left', padx=3, pady=4)
    time_elapsed_label.pack(side='left', padx=3, pady=4)
    progress_scale.pack(side='left', padx=3, pady=4)
    music_duration_label.pack(side='left', padx=3, pady=4)

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

    play_frame.pack(fill="x", padx=3, pady=4)
    change.pack(fill="x", padx=3, pady=4)

    # Расположение frame
    files_frame.pack(expand=True, side="left", fill='both', padx=3, pady=4)
    menu_frame.pack(fill='both', padx=3, pady=4)
    info_frame.pack(fill='both', padx=3, pady=4)

    main_window.mainloop()