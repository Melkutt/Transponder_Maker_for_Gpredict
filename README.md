# A simple way to make transponder file to Gpredict

I got tired of writing together transponders in notepad++ files and automating parts of it, so I created this program whit some help from AI.
I made a EXE file for easy use, but if you alredy have Python installed you can just run my Python code it in a terminal.

## How it works
Quite simple, you enter the data you have access to and then you press save .trsp file, and voila, you have a ready transponder file!
As for the moment, I have only tested it on my Windows 11 computer, I've been thinking about making an HTML page so that you don't have to be independent of which operating system you have, but we'll see.
It is written in Python and run with PyInstaller to create an .EXE file, but I have put the Python program in the scr folder in case you have a different operating system or want to test it.
If you have several different transponders on the same satellite you can add new blocks for each transponder. When you save your transponder file, it is automatically saved after the NORAD ID, for example 12345.trsp


![TRSP_V1 3](https://github.com/user-attachments/assets/6a15ccd2-6228-41e4-b663-30634107ea91)


I recommend saving all files in a separate folder and then copying them to --> C:\Users\<Username>\Gpredict\trsp (on Windows) ~~because every time you update the transponder data it will be overwritten. Or just make it read-only =)~~

New feature, you can make the trsp file as a read-only!
