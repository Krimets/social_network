### Automated bot
bot.py

### config file
config.json


# Social Network

## install requirement project's packages

```commandline
pip install -r requirements.txt
```

## Run project

Go to the folder with manage.py file, run library

```commandline

python manage.py makemigrations
python manage.py migrate
python manage.py runserver

```

## All urls

```
http://localhost:8000/
http://127.0.0.1:8000/register/
http://127.0.0.1:8000/login/
http://127.0.0.1:8000/create_post/
http://127.0.0.1:8000/logout/

http://127.0.0.1:8000/api/register/
http://127.0.0.1:8000/api/login/
http://127.0.0.1:8000/api/create_post/
http://127.0.0.1:8000/api/like_post/<int:post_id>/
http://127.0.0.1:8000/api/unlike_post/<int:post_id>/
http://127.0.0.1:8000/api/analytics/?date_from=2023-04-01&date_to=2023-04-27

http://127.0.0.1:8000/api/token/
http://127.0.0.1:8000/api/token/refresh/
```