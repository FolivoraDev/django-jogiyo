from django.contrib import admin

# Register your models here.
from .models import Restaurant, Tag, Category, Food, SubChoice, Menu

admin.site.register(Restaurant)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(SubChoice)
admin.site.register(Menu)
