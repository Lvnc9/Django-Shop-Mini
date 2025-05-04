# Project Name

Django-Shop-Mini helps you to get more familliar with django tools and deploying dynamically 👌

## Features
- celery-beat to automate the tasks like removing OTP codes (One Time Password)
- caching auth and user information using redice 
- adding django-ckeditor. a powerful writing app which helps you in admin pannel to create your desired descriptions 
like a Office-Word editter!
- using boto3 to connect to your buckets instead of using static storage
- sending OTP codes using Kavenegar (which I'm using you can change it.)
- 

## Installation
```bash
git clone https://github.com/Lvnc9/Django-Shop-Mini.git
cd Django-Shop-Mini
pip install -r requirements.txt

if you got error in installing **psycopg** use:
pip install psycopg2-binary

you need to restart you postgres 
install if you don't have (debian familly):
sudo apt install postgres 

and the restart it 
sudo systemctl restart postgresql.service

sudo -u postgres psql
(enter your password)

CREATE DATABASE djangoShop;
ALTER USER postgres PASSWORD 'postgres';
ctrl^c

sudo systemctl restart rabbitmq-server.service

sudo apt install supervisor
sudo nano /etc/supervisor/conf.d/django-shop.conf

# replace __fvolizer__ to the user you want
[program:django-shop]
user=fvolizer
directory=/home/fvolizer/Me/Django-projs/E-commers/A/
command=/home/fvolizer/.local/bin/celery -A A worker -l INFO
numprocs=1
autostart=true
autorestart=true
stdout_logfile=/var/log/django-shop/celery_out.log
stderr_logfile=/var/log/django-shop/celery_err.log

# save and come back to terminal by ctrl^x then **y** **y**
touch /var/log/django-shop/celery_err.log && touch /var/log/django-shop/celery_out.log

supervisorctl reread
supervisor update

systemctl start redis-server.service


python manage.py  migrate
python manage.py  runserver
