# Create your views here.
import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
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
        'lat': '37.4980608',
        'lng': '127.11526400000001',
        'order': 'rank',
        'page': '0',
        'zip_code': '138169',
    }

    response = requests.get(
        'https://www.yogiyo.co.kr/api/v1/restaurants-geo/', headers=headers, params=params)

    html_source = response.text

    bs = BeautifulSoup(html_source, "html.parser")

    restaurant_list = json.loads(bs.text)['restaurants']

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

        next_id = restaurant['id']

        base_url = 'https://www.yogiyo.co.kr/'
        photo_url = base_url + logo_url

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
        file_name = url.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
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

        item_list = json.loads(bs.text)

        for i in item_list:
            comment = i['comment']
            rating = i['rating']
            rating_delivery = i['rating_delivery']
            rating_quantity = i['rating_quantity']
            rating_taste = i['rating_taste']
            user = User.objects.first()
            Review.objects.create(comment=comment, rating=rating, rating_delivery=rating_delivery,
                                  rating_quantity=rating_quantity, rating_taste=rating_taste, user=user,
                                  restaurant=new_rest)

        response = requests.get(
            'https://www.yogiyo.co.kr/api/v1/restaurants/%d/menu/' % next_id, headers=headers, params=params)

        html_source = response.text

        bs = BeautifulSoup(html_source, "html.parser")

        item_list = json.loads(bs.text)

        for item in item_list:
            real_item = item['items']
            menu_name = item['name']

            new_menu = Menu.objects.get_or_create(name=menu_name, restaurant=new_rest)[0]

            for i in real_item:
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
                        # photo_url_2 = base_url + f_image
                        #
                        # url = photo_url_2
                        # resp = requests.get(url)
                        # if resp.status_code != requests.codes.ok:
                        #     return
                        #
                        # fp = BytesIO()
                        # fp.write(resp.content)
                        # file_name = url.split("/")[-1]
                        # f_food.image.save(file_name, files.File(fp))

                new_menu.food.add(f_food)

                sub = i.get('subchoices')

                for j in sub:
                    subchoices_name = j.get('name')
                    new_sub = SubChoice.objects.get_or_create(name=subchoices_name)[0]

                    foodsub = j.get('subchoices')
                    for k in foodsub:
                        food_name = k.get('name')
                        food_price = k.get('price')

                        if Food.objects.filter(name=food_name).exists():
                            inside_food = Food.objects.get(name=food_name)
                        else:
                            inside_food = Food.objects.create(name=food_name, price=food_price)

                        new_sub.food.add(inside_food)

    return HttpResponse('asda')


def detail_crawler(request):
    a = Restaurant.objects.first()
    print(a.id)
    return HttpResponse(a.id)
