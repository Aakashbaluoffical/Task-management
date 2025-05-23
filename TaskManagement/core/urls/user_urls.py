from django.urls import path
from core.views.user_views import UserLoginView , UserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # path('login',TokenObtainPairView.as_view(),name='user_login'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh',TokenRefreshView.as_view(),name='user_login'),
    path('register',UserLoginView.as_view(),name='user_login'),


    path('',UserListView.as_view(),name='user_login'),

    
]