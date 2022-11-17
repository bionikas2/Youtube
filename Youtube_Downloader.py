from pathlib import Path
from tkinter import Tk
from tkinter.ttk import Label, Button, Entry
from pytube import YouTube, exceptions


def download_from_youtube(url):
    try:
        video = YouTube(url)
        video = video.streams.filter(
            progressive=True, file_extension="mp4"
        ).get_highest_resolution()
        video.download(f"{Path.home()}/Downloads")

        good = Label(window, text="Downloaded", font=("jost", 15))
        good.place(x=300, y=60, anchor="center")
        good.after(3000, good.destroy)

    except exceptions.VideoUnavailable or exceptions.RegexMatchError:
        bad = Label(window, text="Bad url", font=("jost", 15))
        bad.place(x=300, y=60, anchor="center")
        bad.after(3000, bad.destroy)


def set_up():
    window.title("Youtube Downloader")
    window.geometry("550x120")
    window.resizable(False, False)

    label = Label(window, text="Youtube Downloader", font=("jost", 30))
    label.place(anchor="s")
    label.pack()

    url_field = Entry(window, width=30, font=("jost", 15))
    url_field.place(x=20, y=90, anchor="w")

    download_button = Button(
        window,
        text="Download",
        command=lambda: download_from_youtube(url_field.get()),
    )
    download_button.place(x=475, y=90, anchor="center")
    window.mainloop()


window = Tk()
set_up()

# https://www.youtube.com/watch?v=du-TY1GUFGk&ab_channel=JimmyHere
# https://www.youtube.com/wsszzvKF_-nvHere
