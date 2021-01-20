# practice12

# Teamwork

#### Pre-requisites
    Python 3.5

#### Installation
    Clone repo
    Create environment with Python 3.7
    python3.7 -m virtualenv MyEnv
    source MyEnv/bin/activate
    pip install -r requirements.txt

### Create super user
    cd teamwork
    python manage.py createsuperuser

### Run server
    python manage.py runserver
    go to 127.0.0.1 and create user and login

### Additional information
    All user can see files and comments on them    

### Database settings
    if you want to use Mysql then install mysqlclient
    then change your DATABASES in settings file like below

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'DBname',
            'USER': 'username',
            'PASSWORD': 'passwd',
        }
  }    