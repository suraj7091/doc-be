from django.urls import path
from .views import LoginAPI, UserRoles, user_detail

urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path('user_profile/', UserRoles.as_view(), name='user_info'),
    path('user_detail/<int:pk>/', user_detail)
]