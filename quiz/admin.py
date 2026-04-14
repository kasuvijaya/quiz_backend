
from django.contrib import admin


from .models import User,Question,Result

admin.site.register(User)
admin.site.register(Question)
admin.site.register(Result)
