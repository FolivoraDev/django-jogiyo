# from selenium import webdriver
#
# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# # Chrome의 경우 | 아까 받은 chromedriver의 위치를 지정해준다.
# driver = webdriver.Chrome('/home/folivoradev/Downloads/chromedriver')
# # PhantomJS의 경우 | 아까 받은 PhantomJS의 위치를 지정해준다.
# # driver = webdriver.PhantomJS('/home/folivoradev/Downloads/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
#
# driver.get('https://www.yogiyo.co.kr/mobile/#/')
#
# # address_input
# # button_search_address
#
# driver.find_element_by_name('address_input').clear()
# driver.find_element_by_name('address_input').send_keys('구로구')
#
# driver.find_element_by_id('button_search_address').click()
# driver.implicitly_wait(3)
# #class="dropdown-menu ng-scope am-flip-x bottom-left"
# a = driver.find_element_by_css_selector('.dropdown-menu.ng-scope.am-flip-x.bottom-left')
#
# print(a.text)
#
# # driver.close()

import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from django.contrib.gis.geos import Point
from django.core import files

from members.models import User
from restaurants.models import Restaurant, Tag, Category, Menu, Food, SubChoice, Payment, Review

response = requests.get(
    'https://ko.wikipedia.org/wiki/%EC%84%9C%EC%9A%B8%ED%8A%B9%EB%B3%84%EC%8B%9C%EC%9D%98_%ED%96%89%EC%A0%95_%EA%B5%AC%EC%97%AD')

html_source = response.text
bs = BeautifulSoup(html_source, "html.parser")
a = bs.select('#toc > ul > li.toclevel-1.tocsection-2 > ul > li > a > span.toctext')

seoul_list = [i.text for i in a]

headers = {
    'X-ApiKey': 'iphoneap',
    'X-ApiSecret': 'fe5183cc3dea12bd0ce299cf110a75a2',
    'X-MOD-SBB-CTYPE': 'xhr',
}

for gu in seoul_list:
    lparams = {
        "district": gu,
    }

    response = requests.get('https://www.yogiyo.co.kr/api/v1/districts/', headers=headers, params=lparams)
    html_source = response.text
    bs = BeautifulSoup(html_source, "html.parser")
    ku = json.loads(html_source)[0]

    params = {
        'items': '20',
        'lat': ku['coordinate']['lat'],
        'lng': ku['coordinate']['lng'],
        'order': 'rank',
        'page': '0',
        'zip_code': ku['zipcode'],
    }
    for i in range(0, 1):
        try:
            params['page'] = str(i)

            response = requests.get(
                'https://www.yogiyo.co.kr/api/v1/restaurants-geo/', headers=headers, params=params)

            html_source = response.text

            bs = BeautifulSoup(html_source, "html.parser")

            restaurant_list = json.loads(bs.text).get('restaurants', None)

            for restaurant in restaurant_list:
                name = restaurant['name']
                print(name)
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

                for j in payment_methods:
                    payment_method = Payment.objects.get_or_create(name=i)[0]
                    new_rest.payment_methods.add(payment_method)

                for j in tags:
                    tag = Tag.objects.get_or_create(name=i)[0]
                    new_rest.tags.add(tag)

                for j in categories:
                    category = Category.objects.get_or_create(name=i)[0]
                    new_rest.categories.add(category)

                url = photo_url
                resp = requests.get(url)
                # if resp.status_code != requests.codes.ok:

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

                    for q in real_item[:5]:
                        f_name = q['name']
                        f_image = q.get('image')
                        f_price = q['price']

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

                                fp = BytesIO()
                                fp.write(resp.content)
                                file_name = url.split("/")[-1]
                                f_food.image.save(file_name, files.File(fp))

                        new_menu.food.add(f_food)

                        sub = q.get('subchoices')

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
