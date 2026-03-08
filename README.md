# A simple way to make transponder file to Gpredict

I got tired of writing together transponders in notepad++ files and automating parts of it, so I created this program whit some help from AI.

## How it works
Quite simple, you enter the data you have access to and then you press save .trsp file, and voila, you have a ready transponder file!
As for the moment, I have only tested it on my Windows 11 computer, I've been thinking about making an HTML page so that you don't have to be independent of which operating system you have, but we'll see.
It is written in Python and run with PyInstaller to create an .EXE file, but I have put the Python program in the scr folder in case you have a different operating system or want to test it.
If you have several different transponders on the same satellite, you can add blocks for each transponder. 


![TRSP_V1 3](https://github.com/user-attachments/assets/73827bce-d69a-409c-bb3f-543ce86c08a7)


I recommend saving all files in a separate folder and then copying them to --> C:\Users\<Username>\Gpredict\trsp (on Windows) ~~because every time you update the transponder data it will be overwritten. Or just make it read-only =)~~

New featur, you can make the trsp file as a read-only!
