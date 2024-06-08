# read this to deploy on WINDOWS
# Make sure that you have python installed

# After cloned the project



👇🏽Install modules via `VENV` (windows) 👇🏽

$ virtualenv env ✔️ (if don't work use: "python -m venv env")
$ .\env\Scripts\activate ✔️
$ pip3 install -r requirements.txt ✔️



👇🏽Set Up Database👇🏽
## You need to import first your databases on mysql.
$ python manage.py makemigrations ✔️
$ python manage.py migrate ✔️



👇🏽Start the APP👇🏽
$ python manage.py createsuperuser # create the admin ✔️
$ python manage.py runserver       # start the project✔️

