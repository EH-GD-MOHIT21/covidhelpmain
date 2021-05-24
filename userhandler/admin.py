from django.contrib import admin

# Register your models here.

from .models import userpersonal
from pagesholder.models import publicaccessdata as pad
admin.site.register(userpersonal)
admin.site.register(pad)

admin.site.site_header = "CovidHelper.com"
admin.site.site_title = "Welcome to Admin Panel CovidHelper.com"
admin.site.index_title = "CovidHelper.com Hosted @ heroku"