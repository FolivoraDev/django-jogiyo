from rest_framework import serializers

from members.serializer import UserSerializer
from .models import Restaurant, Tag, Category, Menu, Food, SubChoice, Review, Payment, Order


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
        fields = ('id', 'image', 'name', 'price')


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Review
        fields = (
            'id', 'comment', 'rating', 'rating_delivery', 'rating_quantity', 'rating_taste', 'review_images', 'time',
            'user')


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'name')


class RestaurantSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    categories = CategorySerializer(many=True)
    payment_methods = PaymentSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'logo_url', 'review_avg', 'min_order_amount', 'review_count', 'owner_reply_count',
            'except_cash', 'payment_methods', 'discount_percent', 'additional_discount_per_menu', 'delivery_fee',
            'estimated_delivery_time', 'additional_discount_per_menu', 'tags', 'categories', 'begin', 'end',
            'company_name', 'company_number', 'country_origin', 'introduction_text')


class MenuSerializer(serializers.ModelSerializer):
    # food = serializers.SlugRelatedField(many=True, slug_field='name', queryset=Food.objects.all())
    # restaurant = serializers.SlugRelatedField(slug_field='name', queryset=Restaurant.objects.all())
    food = FoodSerializer(many=True)
    restaurant = RestaurantSerializer()

    class Meta:
        model = Menu
        fields = ('id', 'restaurant', 'name', 'food')


class RestaurantDetailSerializer(serializers.ModelSerializer):
    menu_set = MenuSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'menu_set',)


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    food = FoodSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'food', 'time', 'address', 'request')
