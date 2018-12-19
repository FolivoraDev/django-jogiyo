from django.contrib import admin

# Register your models here.
from .models import Restaurant, Tag, Category, Food, SubChoice, Menu, Review, Order

admin.site.register(Restaurant)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Food)
admin.site.register(SubChoice)
admin.site.register(Menu)
admin.site.register(Order)
admin.site.register(Review)
