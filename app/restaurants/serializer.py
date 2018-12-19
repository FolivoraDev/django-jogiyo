import datetime

from django.utils import timezone
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


class ReviewCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        attrs['menu_summary'] = []

        if attrs['user'].is_anonymous:
            raise serializers.ValidationError('비회원입니다 헤더에 토큰을 넣어주세요')

        date_from = datetime.datetime.now(timezone.utc) - datetime.timedelta(days=1)

        if attrs['user'].order_set.exists():
            attrs['menu_summary'] = [i for i in
                                     attrs['user'].order_set.filter(
                                         restaurant__id=attrs['restaurant'].id,
                                         time__gte=date_from).order_by('-time').first().food.all().values_list(
                                         'id', flat=True)]
        return attrs

    class Meta:
        model = Review
        fields = (
            'id', 'comment', 'rating', 'rating_delivery', 'rating_quantity', 'rating_taste', 'review_images', 'time',
            'user', 'menu_summary', 'restaurant')


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    menu_summary = FoodSerializer(many=True)

    class Meta:
        model = Review
        fields = (
            'id', 'comment', 'rating', 'rating_delivery', 'rating_quantity', 'rating_taste', 'review_images', 'time',
            'user', 'menu_summary', 'restaurant')


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
            'company_name', 'company_number', 'country_origin', 'introduction_text', 'location')


class MenuSerializer(serializers.ModelSerializer):
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


class OrderCreateSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate(self, attrs):
        attrs['user'] = self.context['request'].user
        return attrs

    class Meta:
        model = Order
        fields = ('id', 'restaurant', 'user', 'food', 'time', 'address', 'request')


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    food = FoodSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'food', 'time', 'address', 'request')
