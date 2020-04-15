#####Required:
* python3.8
* django 3.0
#####Optional:
* virtual env

#####Installation process:
* Clone repository: **git clone https://github.com/adrianashymoniak/News-website.git**
* Create virtual env:  run command in terminal **python -m venv myvenv**
* Activate virtual env (optional): 
    - For Linux: **source myvenv/bin/activate**
* run: **pip install -r requirements.txt** (for installing required libraries in your virtual env)
* Install postgresql: 
    - run **sudo apt-get update** 
    - run **sudo apt-get install postgresql postgresql-contrib**

* Create db and db user: 
    * **sudo -i -u postgres**
    * run: **psql**
    * CREATE USER **set_user_name_here** WITH PASSWORD '**set_password_here**';
    * CREATE DATABASE news_website;
    
* For setting correct db time zone go to terminal and run:
    * **sudo -u postgres psql**
    * **\c news_website;**
    * **DATABASE news_website SET timezone TO 'UTC';**
    * **SELECT pg_reload_conf();**
    
* Edit .env file with updating the params in <> (remove "<""">" and add your
 params)
* Make sure your virtual environment is activated and requirements are installed    
* Go to root project folder and run migration: **python manage.py migrate
 --settings=news_website.settings.dev**
* Run server locally: **python manage.py runserver --settings=news_website
.settings.dev***
* Open browser and go to  **http://127.0.0.1:8000/** -> click signup and create your own user
 


