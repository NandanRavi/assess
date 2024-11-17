from django.urls import path
from .views import RegisterUser, LoginUser, UserView, LogoutUserView

urlpatterns = [
    path("home/", UserView.as_view(), name="home"),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]
