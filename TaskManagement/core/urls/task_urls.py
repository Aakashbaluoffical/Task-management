from django.urls import path
from core.views.task_views import TaskDetail,TaskListModification


urlpatterns = [
    path('',TaskDetail.as_view(),name='all_task'),
    path('<int:pk>',TaskListModification.as_view(),name='Modify_task'),

]