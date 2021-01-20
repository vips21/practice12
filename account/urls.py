from django.urls import path
from django.contrib.auth import views as auth_views
from .views import sign_up, home, login_view, upload_file, \
    file_comment, user_email

urlpatterns = [
    path('', login_view, name='login_view'),
    path('sign_up', sign_up, name='sign_up'),
    path('home', home, name='home'),
    path('upload_file', upload_file, name='upload_file'),
    path('user_email', user_email, name='user_email'),
    path('file_comment/<int:file_id>', file_comment, name='file_comment'),
]