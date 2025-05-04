# Django-Shop-Mini

Django-Shop-Mini helps you to get more familiar with Django tools and deploying dynamically 👌

## Features
- celery-beat to automate tasks like removing OTP codes (One Time Password)
- Caching auth and user information using Redis 
- adding django-ckeditor, a powerful writing app which helps you in the admin panel to create your desired descriptions 
like an Office Word editor!
- Using boto3 to connect to your buckets instead of using static storage
- sending OTP codes using Kavenegar (which I'm using, you can change it.)
- 

## Installation
```bash
git clone https://github.com/Lvnc9/Django-Shop-Mini.git
cd Django-Shop-Mini
pip install -r requirements.txt

# if you get an error while installing **psycopg**, use:
pip install psycopg2-binary

# you need to restart your PostgreSQL 
# install if you don't have (debian family):
sudo apt install postgres 

# restart it
sudo systemctl restart postgresql.service

sudo -u postgres psql
#(enter your password)

CREATE DATABASE djangoShop;
ALTER USER postgres PASSWORD 'postgres';
#ctrl^c

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
