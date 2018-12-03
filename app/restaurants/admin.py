from django.contrib import admin

# Register your models here.
from .models import Restaurant, Tag, Category

admin.site.register(Restaurant)
admin.site.register(Tag)
admin.site.register(Category)
