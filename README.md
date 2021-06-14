# Valorant Daily Skins

This project gets your daily in-store skins in Valorant without starting the actual game. (WebApp &amp; Windows executable)

## Windows Executable Version
Python is used to authenticate users, fetch skins and create the graphical user interface via Tkinter. Pyinstaller is used to create the Windows executable file.

PS.Check out this project's Flask Web App Code [here](https://github.com/deepsidh9/Valorant-Daily-Skins/tree/flaskwebapp)  and its hosting on https://trackvalorantskins.com
## Installation
### Prerequisites : Python3.x and Pyinstaller
You can clone this repository and run the following command to generate the Windows executable file (.exe).
```sh
pyinstaller -F --add-data "final_skins.json;." --add-data "textfield.png;." --add-data "img0.png;." --add-data "favicon.ico;." -w .\window.py
```
## Usage
You'll see your in-store skins for that day after these steps :
- Click on the generated window.exe file in the *dist* folder
- Enter your credentials*
- Hit submit

*You can inspect the code and see that running this file does not send your credentials to any other server than Riot's. Everything happens locally, on your device. The 'Remember me' feature stores the credentials only on your device ,for your own convenience.

## Credits
This project's authentication flow is inspired by [dylantheriot's work](https://github.com/dylantheriot/valorant-match-history). 

## Disclaimer
This is a fan-made project. Riot Games does not endorse, sponsor or affiliate with this project. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
