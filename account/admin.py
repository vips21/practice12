from django.contrib import admin
from .models import UserEmail, User, FileComments, UserFiles


admin.site.register(User)
admin.site.register(UserEmail)
admin.site.register(FileComments)
admin.site.register(UserFiles)
