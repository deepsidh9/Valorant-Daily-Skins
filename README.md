# Valorant Daily Skins

This project gets your daily in-store skins in Valorant without starting the actual game. (WebApp &amp; Windows executable)

## Flask Web Application Version
Python is used to authenticate users, fetch skins and serve the HTML templates via Flask. Gunicorn is used to serve requests if the application is running through Docker.

PS. Check out this project's hosting on https://trackvalorantskins.com and the Windows Executable Version's Code [here](https://github.com/deepsidh9/Valorant-Daily-Skins/tree/windowsapp) .

## Installation

The web app can be run in two ways:
- Directly running the Flask-App
- Dockerizing the application and then running the container with gunicorn serving requests.


### Flask-app

#### Prerequisites 
- Python3.x
- Run the following command in the project's root directory (assuming you have cloned this repository) to install all other dependencies

```sh
pip install -r requirements.txt
```
#### Usage
- Run the following command to start the server at http://localhost:5000 :
```sh
python app.py
```
- Go to http://localhost:5000, enter your credentials* and hit submit.
 
 You can then see your in-store skins for that day.
 
*You can inspect the code and see that running this project does not store your credentials anywhere. 

### Dockerized Flask-app

#### Prerequisites 

Follow the same steps as for the Flask app installation as given above. You will additionally need to have Docker installed on your device.
#### Usage
- Build your image by :
```sh
docker build -t valorantdailyskins:v1 .
```
- Run your image by:
```sh
docker run -p 5000:5000 valorantdailyskins:v1
```
## Credits
This project's authentication flow is inspired by [dylantheriot's work](https://github.com/dylantheriot/valorant-match-history). 

## Disclaimer
This is a fan-made project. Riot Games does not endorse, sponsor or affiliate with this project. Riot Games, and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
