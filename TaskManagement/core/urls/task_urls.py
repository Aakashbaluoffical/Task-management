from django.urls import path
from core.views.task_views import TaskDetail,TaskListModification ,TaskListReportView
from core.views import task_views

urlpatterns = [
    path('',TaskDetail.as_view(),name='all_task'),
    path('<int:pk>',TaskListModification.as_view(),name='Modify_task'),
    path('<int:pk>/report',TaskListReportView.as_view(),name='view_task_report'),

    

]