# A simple way to make transponder file to Gpredict

I got tired of writing together transponders in notepad++ files and automating parts of it, so I created this program whit some help from AI.

## How it works
Quite simple, you enter the data you have access to and then you press save .trsp file, and voila, you have a ready transponder file!
As for the moment, I have only tested it on my Windows 11 computer, I will try to make an HTML file to be able to get around OS support.
It is written in Python and run with PyInstaller to create an .EXE file, but I have put the Python program in the scr folder in case you have a different operating system or want to test it.
If you have several different transponders on the same satellite, you can add blocks for each transponder.

![trsp](https://github.com/user-attachments/assets/a63105b4-18ee-4293-861f-6a2712618e3d)

I recommend saving all files in a separate folder and then copying them to --> C:\Users\<Username>\Gpredict\trsp (on Windows) because every time you update the transponder data it will be overwritten. Or just make it read-only =)
