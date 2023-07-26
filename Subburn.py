import os
import re
import subprocess
import tkinter as tk
from tkinter import ttk
from tqdm import tqdm
import threading

root = tk.Tk()
root.title('Subtitle Burner')

# Variables
video_file = tk.StringVar()
subtitle_file = tk.StringVar()
output_file = tk.StringVar()
quality = tk.IntVar(value=1)
file_types = ['.avi', '.mkv', '.mp4']
file_type = tk.StringVar()

# Layout
tk.Label(root, text='Video file:').grid(row=0, column=0, sticky='e')
tk.Entry(root, textvariable=video_file).grid(row=0, column=1)

tk.Label(root, text='Subtitle file:').grid(row=1, column=0, sticky='e')
tk.Entry(root, textvariable=subtitle_file).grid(row=1, column=1)

tk.Label(root, text='Output file:').grid(row=2, column=0, sticky='e')
tk.Entry(root, textvariable=output_file).grid(row=2, column=1)

tk.Label(root, text='File Type:').grid(row=3, column=0, sticky='e')
file_type_dd = ttk.Combobox(root, textvariable=file_type)
file_type_dd['values'] = file_types
file_type_dd.current(0)  # set initial value
file_type_dd.grid(row=3, column=1)


def burn_subtitles():
    try:
        # Check if the files exist
        if not os.path.isfile(video_file.get()):
            raise FileNotFoundError(f"The video file '{video_file.get()}' does not exist")

        if not os.path.isfile(subtitle_file.get()):
            raise FileNotFoundError(f"The subtitle file '{subtitle_file.get()}' does not exist")

        # The FFmpeg command to burn the subtitles into the video
        command = f'ffmpeg -i {video_file.get()} -vf "subtitles={subtitle_file.get()}" -q:v {quality.get()} {output_file.get() + file_type.get()}'

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        duration = None
        pbar = None

        for line in iter(process.stdout.readline, ""):
            if duration is None:
                match = re.search(r"Duration: (\d{2}):(\d{2}):(\d{2}).\d{2}", line)
                if match:
                    duration = int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3))
                    pbar = tqdm(total=duration)
                    continue
            if pbar is not None:
                match = re.search(r"time=(\d{2}):(\d{2}):(\d{2}).\d{2}", line)
                if match:
                    current_time = int(match.group(1)) * 3600 + int(match.group(2)) * 60 + int(match.group(3))
                    pbar.update(current_time - pbar.n)

        if pbar is not None:
            pbar.close()

        print(f'Success! The output video is {output_file.get() + file_type.get()}')

    except Exception as e:
        print(f"An error occurred: {e}")


def start_burn_subtitles_thread(event):
    global burn_subtitles_thread
    burn_subtitles_thread = threading.Thread(target=burn_subtitles)
    burn_subtitles_thread.daemon = True

    burn_subtitles_thread.start()
    root.after(20, check_burn_subtitles_thread)


def check_burn_subtitles_thread():
    if burn_subtitles_thread.is_alive():
        root.after(20, check_burn_subtitles_thread)


burn_button = tk.Button(root, text='Burn Subtitles')
burn_button.bind('<Button-1>', start_burn_subtitles_thread)
burn_button.grid(row=4, column=0, columnspan=2)

root.mainloop()
