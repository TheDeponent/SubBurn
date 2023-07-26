This is a simple script which burns subtitles into a video file.
I use this to cast subtitled videos to my Chromecast through VLC, as .srt files are not supported when casting.

To use, follow these steps:
1. Download FFMPEG & add bin directory to PATH environment variables, import dependencies (tqdm, tk)
2. Save the video and subtitle files to the same directory as the 'Subburn.py' script
3. Run the script
4. Insert the names and file types of the video and srt files into the GUI (eg. Video1.avi; Sub1.srt)
5. Nominate a title for the output file
6. Nominate a filetype to output
7. Click 'Burn Subtitles' to run the script - a progress bar will display in the terminal.