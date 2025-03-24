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