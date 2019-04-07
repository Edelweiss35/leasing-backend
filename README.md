 Leasing Django backend setup for Linux and Mac machine
 =========================================================

#### OUR ASSUMPTIONS : ####
> We are already assuming that you have virtualenv installed on your machine.
> Your machine is running Python verison 2.
> You have a running instance of postgresql.

#### INSTALLATION: ####
```
$ cd ~/
$ virtualenv -p python2 --no-site-packages env_leasing
$ cd env_leasing
$ git clone git@gitlab.com:zcm/DjangoAPI.git
$ cd DjangoAPI
$ source ../bin/activate
$ pip install -r requirements.txt
```
#### Updating database settings for up & running ####
> To update the database settings you need to update the settings/dev_db.py  file
> In setttings/dev_db.py file rename all occurences of  YOUR_FIRST_NAME  with your actual first name

#### Creating a postgres database for you locally  ####
> we are assuming you have a postrgesql database  instance running on your system
```
$ psql -U postgres
# Above command will open postgres shell, run following commands to create a datbase
> create database <database_name>;  # make sure this database_name is same as in settings/dev_db.py
>\q
```
#### Running Django DB migrations on postgres database ####
```
./manage.py makemigrations
$ python manage.py migrate
```
#### CREATING INITIAL USER ACCOUNT WITH ALL ACCESS ####
```
$ python manage.py createsuperuser
```
>  fill the desire data as prompted, and a superuser will be created


#### Running the django dev server ####
```
$ python manage.py runserver [host]:[port]
```

> open your browser, call for http://localhost:8000
> and login using the created superadmin credentials
[a workaround link]