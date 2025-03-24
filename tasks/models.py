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