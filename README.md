# how to run django app

## this file is using tailwind css

### you must install tailwind package

- $ python -m pip install django-tailwind

### once installed you must also run the django service

- $ python manage.py tailwind start

### in another terminal you could now start the django server

- $ python manage.py runserver


## make sure to change credentials profile for s3 in add photo view function

- s3 = boto3.Session(profile_name='keyboardcollector').client('s3')