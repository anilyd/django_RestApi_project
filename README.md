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

from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    TASK_TYPES = (
        ('P', 'Personal'),
        ('W', 'Work'),
        ('S', 'Shopping'),
        ('O', 'Other'),
    )
    
    STATUS_CHOICES = (
        ('P', 'Pending'),
        ('I', 'In Progress'),
        ('C', 'Completed'),
    )
    
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    task_type = models.CharField(max_length=1, choices=TASK_TYPES, default='O')
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    assigned_users = models.ManyToManyField(User, related_name='tasks')

    def __str__(self):
        return self.name

Step 6: Create Serializers
Create tasks/serializers.py:


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'created_at', 'task_type', 
                 'completed_at', 'status', 'assigned_users']

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['name', 'description', 'task_type']

class TaskAssignSerializer(serializers.Serializer):
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

Step 7: Create Views
Edit tasks/views.py:

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Task
from .serializers import (TaskSerializer, TaskCreateSerializer, 
                         TaskAssignSerializer, UserSerializer)

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Create Task': '/task-create/',
        'Assign Task': '/task-assign/<int:task_id>/',
        'User Tasks': '/user-tasks/<int:user_id>/',
    }
    return Response(api_urls)

@api_view(['POST'])
def taskCreate(request):
    if request.method == 'POST':
        serializer = TaskCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def taskAssign(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'POST':
        serializer = TaskAssignSerializer(data=request.data)
        if serializer.is_valid():
            user_ids = serializer.validated_data['user_ids']
            users = User.objects.filter(id__in=user_ids)
            task.assigned_users.add(*users)
            return Response({'status': 'users assigned'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def userTasks(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        tasks = Task.objects.filter(assigned_users__id=user_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

# Additional CRUD operations to match your example style
@api_view(['GET'])
def taskList(request):
    tasks = Task.objects.all().order_by('-id')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def taskDetail(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(task, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
def taskUpdate(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskSerializer(instance=task, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def taskDelete(request, pk):
    try:
        task = Task.objects.get(id=pk)
    except Task.DoesNotExist:
        return Response({'error': 'Task not found'}, status=status.HTTP_404_NOT_FOUND)
    
    task.delete()
    return Response({'message': 'Task deleted successfully'}, status=status.HTTP_200_OK)



Step 8: Configure URLs
Create tasks/urls.py:


from django.urls import path
from .views import (
    apiOverview, taskCreate, taskAssign, 
    userTasks, taskList, taskDetail,
    taskUpdate, taskDelete
)

urlpatterns = [
    path('', apiOverview, name='api-overview'),
    path('task-create/', taskCreate, name='task-create'),
    path('task-assign/<int:task_id>/', taskAssign, name='task-assign'),
    path('user-tasks/<int:user_id>/', userTasks, name='user-tasks'),
    path('task-list/', taskList, name='task-list'),
    path('task-detail/<int:pk>/', taskDetail, name='task-detail'),
    path('task-update/<int:pk>/', taskUpdate, name='task-update'),
    path('task-delete/<int:pk>/', taskDelete, name='task-delete'),
]

## project taskmanager urls.py
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('tasks.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


Step 9: Run Migrations
>python manage.py makemigrations
>python manage.py migrate

Step 10: Create Superuser
>python manage.py createsuperuser ## username :anil and password: anil .it will help to creation of jwt token and also login in django admin portal


Step 11: Run Development Server
>python manage.py runserver

Step 12: Test the API:

Geration of token curl:

curl --location 'http://127.0.0.1:8000/api/token/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "anil",
    "password": "anil"
}'

#tak create:
curl --location 'http://127.0.0.1:8000/api/task-create/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODQ3NjI1LCJpYXQiOjE3NDI4NDczMjUsImp0aSI6IjI3YjY3ODk3Nzc1YTQ1OGE5ZDllOGFlNDhiMTFlOGNiIiwidXNlcl9pZCI6MX0.hFzBozvnkrKHDp4hFOS4BcoN4J35CTlW46u2SeSb26g' \
--data '{
    "name": "Anil yadav Complete API project",
    "description": "Finish the task management API",
    "task_type": "W"
}'

#task list:

curl --location --request GET 'http://127.0.0.1:8000/api/task-list/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODQ3NjI1LCJpYXQiOjE3NDI4NDczMjUsImp0aSI6IjI3YjY3ODk3Nzc1YTQ1OGE5ZDllOGFlNDhiMTFlOGNiIiwidXNlcl9pZCI6MX0.hFzBozvnkrKHDp4hFOS4BcoN4J35CTlW46u2SeSb26g' \
--data '{
    "assigned_users": [1, 2]
}'

#assign task:

curl --location 'http://127.0.0.1:8000/api/task-assign/7/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODQ3NjI1LCJpYXQiOjE3NDI4NDczMjUsImp0aSI6IjI3YjY3ODk3Nzc1YTQ1OGE5ZDllOGFlNDhiMTFlOGNiIiwidXNlcl9pZCI6MX0.hFzBozvnkrKHDp4hFOS4BcoN4J35CTlW46u2SeSb26g' \
--data '{
    "user_ids": [1, 2]
}'

#deletion of key:
curl --location --request DELETE 'http://127.0.0.1:8000/api/task-delete/10/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQyODQ3NjI1LCJpYXQiOjE3NDI4NDczMjUsImp0aSI6IjI3YjY3ODk3Nzc1YTQ1OGE5ZDllOGFlNDhiMTFlOGNiIiwidXNlcl9pZCI6MX0.hFzBozvnkrKHDp4hFOS4BcoN4J35CTlW46u2SeSb26g' \
--data '{
    "assigned_users": [1, 2]
}'



## How to code deploy on Github
:Create a repository on github with public repo name : django_RestApi_project
* Below commit use to deploy the code on github account:
> git init
> git add .
> git commit -m "Initial commit"
>git branch -M main
> git remote set-url origin https://github.com/anilyd/django_RestApi_project.git
>git push https://<YOUR_TOKEN>@github.com/anilyd/django_RestApi_project.git main



