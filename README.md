Task Management API Setup Guide
Prerequisites:
* Python 3.8+
* pip (Python package manager)
* 
# Create a new directory for your project
1. mkdir task_manager_api

Step 1: Set Up Virtual Environment
> python -m venv myenv

##### window system myenv activate
> .\myenv\Scripts\activate 
## or Linux system myenv activate
>source myenv/bin/activate

Step 2: Install Required Packages
Install Django and DRF
> pip install django djangorestframework

Step 3: Create Django Project and App:
>django-admin startproject taskmanager .
>python manage.py startapp tasks

Step 4: Configure Settings:
Edit taskmanager/settings.py:
INSTALLED_APPS = [
      . .
    'rest_framework',
    'tasks',
]
** database setup:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'taskmanager',
        'USER': 'postgres',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
* but i'm using DBsqlite3
* restframework:
   REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],

}

but i'm using simple jwttoken for authentication of API:
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

Step 5: Create Models
Edit tasks/models.py:
