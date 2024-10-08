# coding=windows-1251

from lib2to3.refactor import get_all_fix_names
from ssl import ALERT_DESCRIPTION_BAD_CERTIFICATE
from sys import _current_frames
from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import askdirectory, askopenfilename, askopenfilenames

import os
import shutil
from PIL.ImageFile import LOAD_TRUNCATED_IMAGES
import eyed3
import io
from PIL import ImageTk, Image
import time
import pygame
from collections import namedtuple

# �������� ������ � ��������� ����������
def load_files():
    # ����� ���������� ��� ����������
    folder = askdirectory(title="����� ��� ��������", initialdir="/")
    if folder == "":
        return
    
    Clear(True)

    # ����������� ������ � ��������� ���������
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    
    shutil.copytree(folder, local_path)

    # ����� ������ � ������
    tree.insert("", END, id=local_path, text="��������� �����", open=True, tag="FOLDER")
    insert_files(local_path, local_path)

# �������� ���������� � ������
def add_files():
    file_types = [("����������� ����", "*.mp3")]
    files = askopenfilenames(filetypes=file_types)

    if files == "":
        return

    if not os.path.exists(local_path):
        os.mkdir(local_path)
    if not tree.exists(local_path):
        tree.insert("", END, id=local_path, text="��������� �����", open=True, tag="FOLDER")

    for f in files:
        if tree.exists(f):
            continue

        el = os.path.basename(f)
        tree.insert(local_path, END, id=os.path.join(local_path,el), text=el, tag="FILE")
        tree.set(os.path.join(local_path,el), column="#1", value="������")

# ������� ���� ������ � ������
def insert_files(path, parrent):
    for el in os.listdir(path):
        if os.path.isdir(os.path.join(path, el)):
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, open=True, tag="FOLDER")
            insert_files(os.path.join(path,el), os.path.join(path,el))
        else:
            tree.insert(parrent, END, id=os.path.join(path,el), text=el, tag="FILE")
            tree.set(os.path.join(path,el), column="#1", value="������")

# ��������� ����� ������ ������
def Change_select():
    for el in tree_select.get_children(""):
        tree_select.delete(el)
    Clear(False)

# ��������� ������� Treeview
open_change_var = False
def Open_chage(event):
    global open_change_var
    open_change_var = True

def Select_file(event):
    global open_change_var
    global FILE_NAME
    FILE_NAME = None

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

# ������������� ���� � ����� ����������
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
        name_label.configure(text="��� �����: " + os.path.basename(filename))
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
            ALBUM_IMAGE = ["", ImageTk.PhotoImage(img)]
            artwork_canvas.create_image(0, 0, anchor="nw", image=ALBUM_IMAGE[1])

        # ���������� ����� � �������� �������
        MUSIC_LENGTH = audio.info.time_secs
        music_duration_label.configure(text=Duration_from_sec(MUSIC_LENGTH))
        progress_scale.configure(to=MUSIC_LENGTH)
        play_button.configure(image=play_icon)

        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        pygame.mixer.music.pause()

# ������� � ���������� ����
def Clear(flag):
    global PAUSE_BUTTON_STATE
    global LOAD_IMAGE
    global ALBUM_IMAGE

    PAUSE_BUTTON_STATE = True
    LOAD_IMAGE = None
    ALBUM_IMAGE = None

    main_window.after_cancel(UPDATER)
    pygame.mixer.music.unload()

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

# ����������� ����� ���� �����
def Select_children(parrent):
    for el in tree.get_children(parrent):
        if tree.get_children(el) != ():
            Select_children(el)
        else:
            if el in tree_select.get_children(""):
                tree_select.delete(el)
            else:
                tree_select.insert("", END, id=el, text=tree.item(el,'text'), tag="FILE")

# ������� �� ������ � ����� (string)
def Duration_from_sec(secs):
    m, s = divmod(secs, 60)
    timelapsed = "{:02d}:{:02d}".format(int (m), int (s))

    return timelapsed

# ��������������� �����
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

# ���������� ������ �������
def Scale_update():
    global UPDATER
    if progress_scale['value'] < MUSIC_LENGTH:
        progress_scale['value'] += 1

        time_elapsed_label['text'] = Duration_from_sec(progress_scale.get())
        UPDATER = main_window.after(1000, Scale_update)
    else:
        progress_scale['value'] = 0
        time_elapsed_label['text'] = "00:00"

# ��������� �������
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

# ��������� ������� �������
def Load_artwork():
    global LOAD_IMAGE

    file_types = [("�����������", "*.jpg"), ("�����������", "*.jpeg"), ("�����������", "*.png")]
    filename = askopenfilename(filetypes=file_types, initialdir="/")
    
    if filename == "":
        return

    img = Image.open(filename)
    img = img.resize((400, 400))
    LOAD_IMAGE = [filename, ImageTk.PhotoImage(img)]

    artwork_canvas.delete("all")
    artwork_canvas.create_image(0, 0, anchor="nw", image=LOAD_IMAGE[1])

# ������� ��������� ������� �������
def Return_atrwork():
    global ALBUM_IMAGE
    global LOAD_IMAGE
    artwork_canvas.delete("all")

    if ALBUM_IMAGE != None:
        artwork_canvas.create_image(0, 0, anchor="nw", image=ALBUM_IMAGE[1])

    LOAD_IMAGE = None

# ��������� ��������� �����
def Save_changes():
    global LOAD_IMAGE
    global ALBUM_IMAGE
    global RESULT_FILES

    res = []
    res_file = namedtuple('res_file', 'first_name name title artist album artwork')

    for f in tree_select.get_children(""):
        audio = eyed3.load(f)
        
        get_title_text = title_text.get(0.0, END)[:-1]
        get_artist_text = artist_text.get(0.0, END)[:-1]
        get_album_text = album_text.get(0.0, END)[:-1]

        if title_text['state'] == "disabled":
            title = audio.tag.title
        else:
            title = get_title_text

        if artist_unknown_var.get():
            artist = "����������� �����������"
        elif get_artist_text == "":
            artist = audio.tag.artist
        else:
            artist = get_artist_text

        if album_unknown_var.get():
            artist = "����������� ������"
        elif get_album_text == "":
            album = audio.tag.album
        else:
            album = get_album_text

        if artwork_unknown_var.get():
            artwork = None
        elif LOAD_IMAGE != None:
            artwork = LOAD_IMAGE
        elif ALBUM_IMAGE != None:
            artwork = ALBUM_IMAGE
        elif list(audio.tag.images) != []:
            img = Image.open(io.BytesIO(audio.tag.images[0].image_data))
            img = img.resize((400, 400))
            artwork = ["", ImageTk.PhotoImage(img)]
        else:
            artwork = None

        name = artist + " - " + title + ".mp3"
        res.append(res_file(first_name=f,
            name=name, 
            title=title, 
            artist=artist,
            album=album,
            artwork=artwork))

    RESULT_FILES = res
    Ask_save()

# ����� ���������� � ����������� �����
def Ask_save():
    global RESULT_FILES

    second_window = Toplevel()

    canvas_window = Canvas(second_window,height=500, width=1000, background="mistyrose1")
    ask_scroll = ttk.Scrollbar(second_window, orient="horizontal", command = canvas_window.xview)
    canvas_window["xscrollcommand"] = ask_scroll.set

    ask_window = ttk.Label(canvas_window,
        style="Info.TFrame")
    ask_window.bind(
        "<Configure>",
        lambda e: canvas_window.configure(
            scrollregion=canvas_window.bbox("all")
        )
    )

    confirm = Button(second_window, 
        text="���������", 
        state="normal", 
        command=lambda: (second_window.destroy(), Confirm()),
        height=2, width=100,
        background="mistyrose2")
    cancel = Button(second_window, 
        text="��������", 
        state="normal", 
        command=lambda: second_window.destroy(),
        height=2, width=100,
        background="mistyrose2")

    canvas_window.create_window((0,0), window=ask_window, anchor="nw")
    canvas_window.pack(side="top", fill='both')
    ask_scroll.pack(fill="x")
    confirm.pack(side="left", padx=3, pady=4)
    cancel.pack(side="left", padx=3, pady=4)

    Label(ask_window, text="��� �����: ", background="mistyrose1", borderwidth=2, font=("Times New Roman", 14),).grid(row=0, column=0)
    Label(ask_window, text="��������: ", background="mistyrose1", borderwidth=2, font=("Times New Roman", 14),).grid(row=1, column=0)
    Label(ask_window, text="�����������: ", background="mistyrose1", borderwidth=2, font=("Times New Roman", 14),).grid(row=2, column=0)
    Label(ask_window, text="������: ", background="mistyrose1", borderwidth=2, font=("Times New Roman", 14),).grid(row=3, column=0)
    Label(ask_window, text="�������: ", background="mistyrose1", borderwidth=2, font=("Times New Roman", 14),).grid(row=4, column=0)
    
    col = 1
    for el in RESULT_FILES:
        Label(ask_window, text=el.name, background="mistyrose1", font=("Times New Roman", 14),).grid(row=0, column=col)
        Label(ask_window, text=el.title, background="mistyrose1", font=("Times New Roman", 14),).grid(row=1, column=col)
        Label(ask_window, text=el.artist, background="mistyrose1", font=("Times New Roman", 14),).grid(row=2, column=col)
        Label(ask_window, text=el.album, background="mistyrose1", font=("Times New Roman", 14),).grid(row=3, column=col)
        if el.artwork == None:
            Label(ask_window, text="��� �������", background="mistyrose1", borderwidth=2).grid(row=4, column=col)
        else:
            Label(ask_window, image=el.artwork[1], background="mistyrose1", borderwidth=2).grid(row=4, column=col)

        col += 1

def Confirm():
    global RESULT_FILES

    Clear(False)

    # first_name name title artist album artwork
    for f in RESULT_FILES:
        index = tree.index(f.first_name)
        parent = tree.parent(f.first_name)

        tree.delete(f.first_name)
        tree_select.delete(f.first_name)

        path = os.path.dirname(f.first_name)
        name = os.path.join(path, f.name)
        os.rename(f.first_name, name)

        audio = eyed3.load(name)

        audio.tag.title = f.title
        audio.tag.artist = f.artist
        audio.tag.album = f.album

        if f.artwork == None:
            for descr in [audio_image.description for audio_image in audio.tag.images]:
                audio.tag.images.remove(descr)
        elif not f.artwork[0] == "":
            for descr in [audio_image.description for audio_image in audio.tag.images]:
                audio.tag.images.remove(descr)
            audio.tag.images.set(3, open(f.artwork[0], 'rb').read(), 'image/jpeg')

        audio.tag.save()

        tree.insert(parent, index, id=name, text=f.name, tag="FILE")
        tree.set(name, column="#1", value="�������")

# �������� �����
def Change_folder():
    if tree_select.get_children("") == ():
        return

    folder = askdirectory(title="�������� �����", initialdir=local_path)
    if folder == "":
        return

    Clear(False)

    folder = os.path.abspath(folder)
    Set_folder(folder)

    for f in tree_select.get_children(""):
        shutil.move(f, folder)

        parrent = tree.parent(f)
        tree.delete(f)
        tree_select.delete(f)
        if tree.get_children(parrent) == ():
            tree.delete(parrent)

        tree.insert(folder, END, id=os.path.join(folder, os.path.basename(f)), text=os.path.basename(f), tag="FILE")

# ������ �����
def Set_folder(cur_dir):
    if local_path == cur_dir:
        return
    
    folder_split = list(os.path.split(cur_dir))
    Set_folder(folder_split[0])

    if not tree.exists(cur_dir):
        tree.insert(folder_split[0], END, id=cur_dir, text=folder_split[1], open=True, tag="FOLDER")

# ��������� ����� � �����
def Upload_files():
    folder = askdirectory(title="����� ��� ��������", initialdir="/")
    if folder == "":
        return

    shutil.copytree(local_path, folder, dirs_exist_ok=True)
    Clear(True)

if __name__ == "__main__":
    pygame.init()
    main_window = Tk()
    
    #���������� ���������� GUI
    local_path = os.path.join(os.getcwd(), "temporary_music")
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
    
    # ��������� ����
    main_window.title("�������� ����� ������ mp3")
    main_window.geometry("1600x780+200+100")
    main_window.config(background="oldlace")

    # �������� ������
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

    # �������� ����
    menu_frame = ttk.Labelframe(main_window,
        text="������ � �������",
        relief=RAISED,
        padding=[2, 3],
        style="Menu.TLabelframe")

    load_btn = Button(menu_frame, 
        text="��������� � �������", 
        state="normal", 
        command=load_files,
        height=1,
        background="thistle1")
    
    add_btn = Button(menu_frame, 
        text="�������� �����", 
        state="normal", 
        command= add_files,
        height=1,
        background="thistle1")

    change_dir_btn = Button(menu_frame, 
        text="�������� �����", 
        state="normal", 
        command=Change_folder,
        height=1,
        background="thistle1")

    upload_btn = Button(menu_frame, 
        text="��������� � �����", 
        state="normal", 
        command=Upload_files,
        height=1,
        background="thistle1")

    load_btn.pack(side="left", padx=2, pady=1)
    add_btn.pack(side="left", padx=2, pady=1)
    change_dir_btn.pack(side="left", padx=2, pady=1)
    upload_btn.pack(side="left", padx=2, pady=1)

    # ����� � ����� ������
    files_frame = ttk.Frame(main_window,
        borderwidth=2,
        relief=RAISED,
        padding=[2, 3],
        style="Files.TFrame")

    select_files = ttk.Checkbutton(files_frame,
        text="������� ���������", 
        variable=select_files_var,
        command=Change_select,
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

    tree.bind("<<TreeviewSelect>>", Select_file)
    tree.bind("<<TreeviewOpen>>", Open_chage)
    tree.bind("<<TreeviewClose>>", Open_chage)

    tree_select = ttk.Treeview(files_frame, 
        show="tree headings",
        selectmode="none",
        style="Files.Treeview")

    tree_select.heading("#0", text="��������� �����")

    tree_select.tag_configure("FOLDER", background="lightpink1")
    tree_select.tag_configure("FILE", background="beige")

    select_files.pack(anchor="center", pady=4)
    tree.pack(expand=True, fill='both', padx=2, pady=1)
    tree_select.pack(fill='both', padx=2, pady=1)

    # ����� ���������� � �����
    info_frame = ttk.Frame(main_window,
        borderwidth=2,
        relief=RAISED,
        padding=[2, 3],
        style="Info.TFrame")

    # ��� �����
    name_label = Label(info_frame,
        text="",
        anchor="center",
        font=("Times New Roman", 14),
        background="mistyrose1")

    # ��������
    title_frame = ttk.Frame(info_frame,
        padding=[2, 2, 10, 6],
        style="Info.TFrame")

    title_label = Label(title_frame,
        text="�������� ����������:  ",
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

    # �����������
    artist_frame = ttk.Frame(info_frame,
        padding=[2, 2, 10, 6],
        style="Info.TFrame")

    artist_label = Label(artist_frame,
        text="�����������:  ",
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
        text="����������� �����������", 
        variable=artist_unknown_var,
        style="Info.TCheckbutton")

    # ������
    album_frame = ttk.Frame(info_frame,
        padding=[2, 2, 10, 6],
        style="Info.TFrame")

    album_label = Label(album_frame,
        text="������:  ",
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
        text="����������� ������", 
        variable=album_unknown_var,
        style="Info.TCheckbutton")

    # ������� �������
    artwork_frame = ttk.Frame(info_frame,
        borderwidth=2,
        relief=RAISED,
        padding=[0],
        style="Info.TFrame")

    artwork_load = Button(artwork_frame, 
        text="��������� �������", 
        state="disabled", 
        command=Load_artwork,
        font=("Times New Roman", 14),
        background="mistyrose2")

    artwork_return = Button(artwork_frame, 
        text="������� �������", 
        state="disabled", 
        command=Return_atrwork,
        font=("Times New Roman", 14),
        background="mistyrose2")

    artwork_canvas = Canvas(artwork_frame,
        height=400, 
        width=400,
        background="mistyrose2")

    artwork_unknown = ttk.Checkbutton(artwork_frame,
        text="����������� �������", 
        variable=artwork_unknown_var,
        style="Info.TCheckbutton")

    artwork_canvas.pack()
    artwork_unknown.pack(padx=3, pady=4)
    artwork_load.pack(fill='x', padx=3, pady=4)
    artwork_return.pack(fill='x', padx=3, pady=4)

    # ������������� �����
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

    # ������
    change = Button(info_frame, 
        text="��������� ���������", 
        state="disabled", 
        command=Save_changes,
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

    # ������������ frame
    files_frame.pack(expand=True, side="left", fill='both', padx=3, pady=4)
    menu_frame.pack(fill='both', padx=3, pady=4)
    info_frame.pack(fill='both', padx=3, pady=4)

    main_window.mainloop()