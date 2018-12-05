from rest_framework import serializers

from .models import Restaurant, Tag, Category, Menu, Food, SubChoice


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


class SubChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubChoice
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ('id', 'name', 'price')


class MenuSerializer(serializers.ModelSerializer):
    food = FoodSerializer(many=True)

    class Meta:
        model = Menu
        fields = ('id', 'name', 'food')


class RestaurantSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    categories = CategorySerializer(many=True)

    menu_set = MenuSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'logo_url', 'review_avg', 'min_order_amount', 'review_count', 'payment',
                  'estimated_delivery_time', 'additional_discount_per_menu', 'tags', 'categories')
        fields += ('menu_set',)
