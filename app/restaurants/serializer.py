from django.db.models import Avg
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
    def update(self, instance, validated_data):
        instance.rating = (instance.rating_delivery + instance.rating_quantity + instance.rating_taste) / 3
        super().update(instance, validated_data)
        return instance

    class Meta:
        model = Review
        fields = (
            'id', 'comment', 'rating', 'rating_delivery', 'rating_quantity', 'rating_taste', 'review_images', 'time',
            'user', 'menu_summary', 'restaurant')

        extra_kwargs = {'restaurant': {'read_only': True},
                        'menu_summary': {'read_only': True},
                        'user': {'read_only': True}}


class ReviewUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    menu_summary = FoodSerializer(many=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return (obj.rating_delivery + obj.rating_quantity + obj.rating_taste) / 3

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
    rating_delivery_avg = serializers.SerializerMethodField()
    review_avg = serializers.SerializerMethodField()
    rating_quantity_avg = serializers.SerializerMethodField()
    rating_taste_avg = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    def get_rating_delivery_avg(self, obj):
        return obj.review_set.aggregate(Avg('rating_delivery'))['rating_delivery__avg']

    def get_rating_taste_avg(self, obj):
        return obj.review_set.aggregate(Avg('rating_taste'))['rating_taste__avg']

    def get_rating_quantity_avg(self, obj):
        return obj.review_set.aggregate(Avg('rating_quantity'))['rating_quantity__avg']

    def get_review_avg(self, obj):
        return obj.review_set.aggregate(Avg('rating'))['rating__avg']

    def get_review_count(self, obj):
        return obj.review_set.all().count()

    class Meta:
        model = Restaurant
        fields = (
            'id', 'name', 'logo_url', 'min_order_amount', 'review_count', 'owner_reply_count',
            'except_cash', 'payment_methods', 'discount_percent', 'additional_discount_per_menu', 'delivery_fee',
            'estimated_delivery_time', 'additional_discount_per_menu', 'tags', 'categories', 'begin', 'end',
            'company_name', 'company_number', 'country_origin', 'introduction_text', 'location', 'review_avg',
            'rating_delivery_avg',
            'rating_quantity_avg', 'rating_taste_avg')


class MenuSerializer(serializers.ModelSerializer):
    food = FoodSerializer(many=True)
    restaurant = RestaurantSerializer()

    class Meta:
        model = Menu
        fields = ('id', 'name', 'restaurant', 'food')


class MenuCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ('id', 'name', 'restaurant', 'food')
        extra_kwargs = {'restaurant': {'read_only': True}, }


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
