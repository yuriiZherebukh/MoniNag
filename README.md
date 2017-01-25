# MoniNag

## Install
We are assuming that you're using bash & you have to install or clone such packages:

* Install PostgreSQL server on local machine
  
  ```
  sudo apt-get install postgresql postgresql-contrib
  sudo apt-get install python-psycopg2
  sudo apt-get install libpq-dev
  ```
* Clone this repository to your local machine
  
  ```
  git clone https://github.com/Lv-219-Python/MoniNag.git
  ```
* Go to the local copy of repository. Open terminal and run the following command
  
  ```
  pip install -r moninag/requirements.txt
  ```
* Create your *local_settings.py* in the folder with *settings.py* and configure it 
  * Database settings
    
    ```
    DATABASES = {            
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': database_name,
            'USER': database_username,
            'PASSWORD': user_password,
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
    ```