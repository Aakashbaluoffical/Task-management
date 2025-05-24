from django.db import models
from core.models.user_models import User



class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'),('inprogress','In Progress'), ('completed', 'Completed')],default='pending')

    assigned_to = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, blank=True)

    worked_hours = models.DecimalField(max_digits=5, decimal_places=2,null=True,blank=True)
    completion_report = models.TextField(null=True,blank=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'task_tbl'
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['assigned_to']),        #  Index for foreign key lookups
            models.Index(fields=['status']),             #  Useful if you filter by status
            models.Index(fields=['due_date', 'status']), #  Composite index (e.g. for dashboard sorting)
        ]
    
    def __str__(self):
        return self.title 
   
    
    
    