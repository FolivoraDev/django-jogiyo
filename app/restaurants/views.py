# Create your views here.
import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from django.contrib.gis.geos import Point
from django.core import files
from django.http import HttpResponse

from members.models import User
from restaurants.models import Restaurant, Tag, Category, Menu, Food, SubChoice, Payment, Review


def crawler(request):
    headers = {
        'X-ApiKey': 'iphoneap',
        'X-ApiSecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
        'X-MOD-SBB-CTYPE': 'xhr',
    }

    # ?items=20&lat=37.4980608&lng=127.11526400000001&order=rank&page=0&search=&zip_code=138169
    params = {
        'items': '20',
        'lat': '37.54299521245206',
        'lng': '127.0414897665702',
        'order': 'rank',
        'page': '0',
        'zip_code': '133110',
    }

    for i in range(0, 10):

        try:
            params['page'] = str(i)

            print(params)

            response = requests.get(
                'https://www.yogiyo.co.kr/api/v1/restaurants-geo/', headers=headers, params=params)

            html_source = response.text

            bs = BeautifulSoup(html_source, "html.parser")

            restaurant_list = json.loads(bs.text).get('restaurants', None)

            for restaurant in restaurant_list:
                name = restaurant['name']
                logo_url = restaurant['logo_url']
                review_avg = restaurant['review_avg'],
                min_order_amount = restaurant['min_order_amount']
                review_count = restaurant['review_count']
                owner_reply_count = restaurant['owner_reply_count']
                estimated_delivery_time = restaurant['estimated_delivery_time']
                discount_percent = restaurant['discount_percent']
                additional_discount_per_menu = restaurant['additional_discount_per_menu']
                payment_methods = restaurant['payment_methods']
                tags = restaurant['tags']
                categories = restaurant['categories']
                begin = restaurant['begin']
                end = restaurant['end']
                lat = restaurant['lat']
                lng = restaurant['lng']
                delivery_fee = restaurant['delivery_fee']

                point = Point(lng, lat)

                next_id = restaurant['id']

                base_url = 'https://www.yogiyo.co.kr/'
                photo_url = base_url + logo_url

                if Restaurant.objects.filter(name=name).exists():
                    continue

                new_rest = Restaurant.objects.create(
                    name=name,
                    owner_reply_count=owner_reply_count,
                    review_avg=review_avg[0],
                    min_order_amount=min_order_amount,
                    review_count=review_count,
                    discount_percent=discount_percent,
                    estimated_delivery_time=estimated_delivery_time,
                    additional_discount_per_menu=additional_discount_per_menu,
                    begin=begin,
                    end=end,
                    location=point,
                    delivery_fee=delivery_fee
                )

                for i in payment_methods:
                    payment_method = Payment.objects.get_or_create(name=i)[0]
                    new_rest.payment_methods.add(payment_method)

                for i in tags:
                    tag = Tag.objects.get_or_create(name=i)[0]
                    new_rest.tags.add(tag)

                for i in categories:
                    category = Category.objects.get_or_create(name=i)[0]
                    new_rest.categories.add(category)

                url = photo_url
                resp = requests.get(url)
                if resp.status_code != requests.codes.ok:
                    return

                fp = BytesIO()
                fp.write(resp.content)
                file_name = url.split("/")[
                    -1]  # There's probably a better way of doing this but this is just a quick example
                new_rest.logo_url.save(file_name, files.File(fp))

                params = {
                    'add_photo_menu': 'android',
                    'add_one_dish_menu': 'true',
                }
                response = requests.get(
                    'https://www.yogiyo.co.kr/api/v1/restaurants/%d/info/' % next_id, headers=headers, params=params)

                html_source = response.text

                bs = BeautifulSoup(html_source, "html.parser")

                item_list = json.loads(bs.text)

                new_rest.company_name = item_list['crmdata']['company_name']
                new_rest.company_number = item_list['crmdata']['company_number']
                new_rest.country_origin = item_list['country_origin']

                new_rest.save()

                params = {
                    'add_photo_menu': 'android',
                    'add_one_dish_menu': 'true',
                    'count': '10',
                }

                response = requests.get(
                    'https://www.yogiyo.co.kr/api/v1/reviews/%d/' % next_id, headers=headers, params=params)

                html_source = response.text

                bs = BeautifulSoup(html_source, "html.parser")

                item_list = json.loads(bs.text)[:10]

                for k in item_list[:5]:
                    if new_rest.review_set.all().count() > 5:
                        continue

                    comment = k['comment']
                    rating = k.get('rating', 0)
                    rating_delivery = k['rating_delivery']
                    rating_quantity = k['rating_quantity']
                    rating_taste = k['rating_taste']
                    user = User.objects.first()
                    Review.objects.create(comment=comment, rating=rating, rating_delivery=rating_delivery,
                                          rating_quantity=rating_quantity, rating_taste=rating_taste, user=user,
                                          restaurant=new_rest)

                response = requests.get(
                    'https://www.yogiyo.co.kr/api/v1/restaurants/%d/menu/' % next_id, headers=headers, params=params)

                html_source = response.text

                bs = BeautifulSoup(html_source, "html.parser")

                item_list = json.loads(bs.text)[:5]

                for item in item_list[:5]:
                    real_item = item['items']
                    menu_name = item['name']

                    new_menu = Menu.objects.get_or_create(name=menu_name, restaurant=new_rest)[0]

                    for i in real_item[:5]:
                        f_name = i['name']
                        f_image = i.get('image')
                        f_price = i['price']

                        if Food.objects.filter(name=f_name).exists():
                            f_food = Food.objects.get(name=f_name)
                        else:
                            f_food = Food.objects.create(name=f_name, price=f_price)

                            if f_image:
                                f_food.image = new_rest.logo_url
                                f_food.save()
                                photo_url_2 = base_url + f_image

                                url = photo_url_2
                                resp = requests.get(url)
                                if resp.status_code != requests.codes.ok:
                                    return

                                fp = BytesIO()
                                fp.write(resp.content)
                                file_name = url.split("/")[-1]
                                f_food.image.save(file_name, files.File(fp))

                        new_menu.food.add(f_food)

                        sub = i.get('subchoices')

                        for j in sub[:5]:
                            subchoices_name = j.get('name')
                            new_sub = SubChoice.objects.get_or_create(name=subchoices_name)[0]

                            foodsub = j.get('subchoices')
                            for k in foodsub[:5]:
                                food_name = k.get('name')
                                food_price = k.get('price')

                                if Food.objects.filter(name=food_name).exists():
                                    inside_food = Food.objects.get(name=food_name)
                                else:
                                    inside_food = Food.objects.create(name=food_name, price=food_price)

                                new_sub.food.add(inside_food)
        except Exception as e:

            print(e)

    return HttpResponse('asda')


def detail_crawler(request):
    # ll = []
    # rest = Restaurant.objects.get(id='175')
    #
    # for i in rest.menu_set.all():
    #     ll += i.food.all()
    #
    # for i in rest.review_set.all():
    #     i.menu_summary.add(random.choice(ll))
    #     print(random.choice(ll))

    aa = Menu.objects.filter(name='Photo Menu Items')

    for i in aa:
        i.save()


    # us = [i for i in User.objects.all()[1:]]
    #
    # for i in Review.objects.all():
    #     i.user = random.choice(us)
    #     i.save()

    # print(request.method)
    # print(request.content_type)
    #
    # name = ['Hyunjun', 'Soyoung', 'Jihye', 'Jihoon', 'Eunkyung', 'Yuup', 'Donghwan', 'Donghyun']
    #
    # for i in name:
    #     User.objects.create_user(username=i, password='123')

    return HttpResponse('success')
