import os
from pathlib import Path
from time import sleep
from tkinter import IntVar, StringVar, Tk
from tkinter.ttk import Label, Button, Entry, Combobox, Radiobutton
from pytube import YouTube, exceptions
from threading import Thread

global download_button
global quality_menu
global url_field
radio_buttons = []


def disable_UI_element(element):
    element.config(state="disabled")


def enable_UI_element(element):
    element.config(state="active")


def download_video_from_youtube(quality, video):

    disable_UI_element(download_button)
    quality_menu.destroy()
    disable_UI_element(url_field)

    video.streams.filter(
        progressive=True, file_extension="mp4", res=quality
    ).first().download(f"{Path.home()}/Downloads")

    good = Label(window, text="Downloaded", font=("jost", 15))
    good.place(x=300, y=60, anchor="center")
    good.after(3000, good.destroy)

    enable_UI_element(url_field)


def download_audio_from_youtube(audio):
    disable_UI_element(download_button)
    try:
        if quality_menu.winfo_exists():
            quality_menu.destroy()
    except:
        pass
    disable_UI_element(url_field)

    for button in radio_buttons:
        button.destroy()

    file = (
        audio.streams.filter(only_audio=True)
        .first()
        .download(f"{Path.home()}/Downloads")
    )
    try:
        base, ext = os.path.splitext(file)
        new_file = base + ".mp3"
        os.rename(file, new_file)
    except FileExistsError:
        base, ext = os.path.splitext(file)
        new_file = base + ".mp3"
        os.remove(new_file)
        os.rename(file, new_file)

    good = Label(window, text="Downloaded", font=("jost", 15))
    good.place(x=300, y=60, anchor="center")
    good.after(3000, good.destroy)

    enable_UI_element(url_field)


def selecting_file_quality(url):
    video = YouTube(url, on_progress_callback=on_progress)
    options = []

    for quality in video.streams.order_by("resolution").filter(
        progressive=True, file_extension="mp4"
    ):
        options.append(quality.resolution)
    options = list(dict.fromkeys(options))

    global quality_menu
    quality_menu = Combobox(window, values=options, font=(10), state="readonly")
    quality_menu.place(x=475, y=150, anchor="center", width=130)
    quality_menu.set("")

    quality = quality_menu.get()
    enable_UI_element(download_button)
    download_button.config(
        command=lambda: Thread(
            target=download_video_from_youtube,
            args=(
                (
                    quality,
                    video,
                )
            ),
        ).start()
    )


def getting_type(url):
    if check_for_exceptions(url):
        global radio_buttons
        r1 = Radiobutton(
            window,
            value="mp3",
            command=lambda: audio_download_button(url),
            text="mp3",
        )
        r1.place(x=475, y=90)
        radio_buttons.append(r1)

        r2 = Radiobutton(
            window,
            value="mp4",
            command=lambda: Thread(target=selecting_file_quality, args=(url,)).start(),
            text="mp4",
        )
        r2.place(x=475, y=110)
        radio_buttons.append(r2)


def audio_download_button(url):
    try:
        if quality_menu.winfo_exists():
            quality_menu.destroy()
    except:
        pass
    audio = YouTube(url, on_progress_callback=on_progress)
    enable_UI_element(download_button)
    download_button.config(
        command=lambda: Thread(
            target=download_audio_from_youtube,
            args=((audio,)),
        ).start()
    )


def on_progress(stream, chunk: bytes, bytes_remaining: int):
    try:
        if progress.winfo_exists():
            progress.destroy()
    except UnboundLocalError:
        pass
    size = stream.filesize
    progress = Label(
        window,
        text=f"{percent(size - bytes_remaining, size)}% completed",
        font=("jost", 15),
    )
    progress.place(x=100, y=150, anchor="center")
    if progress.cget("text") == f"100% completed":
        sleep(1)
        progress.destroy()


def percent(tem, total):
    perc = int((float(tem) / float(total)) * float(100))
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
    sv.trace(
        "w",
        lambda name, index, mode, sv=sv: Thread(
            target=getting_type,
            args=(sv.get(),),
        ).start(),
    )
    global url_field
    url_field = Entry(window, width=45, textvariable=sv)
    url_field.place(x=20, y=90, anchor="w")

    global download_button
    download_button = Button(window, text="Download", state="disabled")
    download_button.place(x=475, y=200, anchor="center")


window = Tk()
window.title("Youtube Downloader")
window.geometry("550x230")
window.resizable(False, False)
set_up()
window.mainloop()

# For tests: first one working link, second one not
# https://www.youtube.com/watch?v=du-TY1GUFGk&ab_channel=JimmyHere
# https://www.youtube.com/wsszzvKF_-nvHere
