from pathlib import Path
from time import sleep
from tkinter import StringVar, Tk
from tkinter.ttk import Label, Button, Entry, Combobox
from typing import BinaryIO
from pytube import YouTube, exceptions


def download_from_youtube(quality, video):

    video = video.streams.filter(
        progressive=True, file_extension="mp4", res=quality
    ).first()
    video.download(f"{Path.home()}/Downloads")

    good = Label(window, text="Downloaded", font=("jost", 15))
    good.place(x=300, y=60, anchor="center")
    good.after(3000, good.destroy)

    global download_button
    download_button.config(state="disabled")


def selecting_video_quality(url):
    if check_for_exceptions(url):
        video = YouTube(url""", on_progress_callback=progress_function""")
        options = []

        for quality in video.streams.order_by("resolution").filter(
            progressive=True, file_extension="mp4"
        ):
            options.append(quality.resolution)
        options = list(dict.fromkeys(options))

        quality_menu = Combobox(window, values=options, font=(10), state="readonly")
        quality_menu.place(x=475, y=90, anchor="center", width=130)
        quality_menu.set("Select quality")

        global download_button
        download_button.config(
            state="active",
            command=lambda: download_from_youtube(quality_menu.get(), video),
        )


def progress_function(stream, chunk: bytes, bytes_remaining: int):

    size = stream.filesize
    while bytes_remaining <= size:
        """progress = Label(window, text=f"{p}% completed", font=("jost", 15))
        progress.place(x=20, y=90, anchor="center")
        progress.after(300, progress.destroy)"""
        sleep(1)
        print(f"{bytes_remaining} out of {size}")


def percent(tem, total):
    perc = (float(tem) / float(total)) * float(100)
    return perc


def check_for_exceptions(url):
    try:
        video = YouTube(url)
        video.streams.filter(progressive=True, file_extension="mp4").first()
        return True
    except exceptions.VideoUnavailable or exceptions.RegexMatchError:
        bad = Label(window, text="Bad url", font=("jost", 15))
        bad.place(x=300, y=60, anchor="center")
        bad.after(3000, bad.destroy)
        return False


def set_up():
    label = Label(window, text="Youtube Downloader", font=("jost", 30))
    label.place(anchor="s")
    label.pack()
    sv = StringVar()
    sv.trace("w", lambda name, index, mode, sv=sv: selecting_video_quality(sv.get()))
    url_field = Entry(window, width=45, textvariable=sv)
    url_field.place(x=20, y=90, anchor="w")

    global download_button
    download_button = Button(window, text="Download", state="disabled")
    download_button.place(x=475, y=140, anchor="center")
    window.mainloop()


window = Tk()
window.title("Youtube Downloader")
window.geometry("550x180")
window.resizable(False, False)
set_up()
window.mainloop()

# For tests: first one working link, second one not
# https://www.youtube.com/watch?v=du-TY1GUFGk&ab_channel=JimmyHere
# https://www.youtube.com/wsszzvKF_-nvHere
