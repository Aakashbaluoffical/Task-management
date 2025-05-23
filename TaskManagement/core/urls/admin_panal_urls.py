from django.urls import path 
from core.views.admin_views import AdminPanal
from core.views.data_insertion_views import insert_data


urlpatterns = [
    path('admin/',AdminPanal.as_view(),name = "custom_admin"),
    path('upload/<str:table_name>',insert_data, name='file upload'),

]