# Create your views here.
import json
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from django.core import files
from django.http import HttpResponse

from restaurants.models import Restaurant


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
        estimated_delivery_time = restaurant['estimated_delivery_time']
        additional_discount_per_menu = restaurant['additional_discount_per_menu']
        tags = restaurant['tags']

        base_url = 'https://www.yogiyo.co.kr/'
        photo_url = base_url + logo_url

        new_rest = Restaurant.objects.create(
            name=name,
            review_avg=review_avg[0],
            min_order_amount=min_order_amount,
            review_count=review_count,
            estimated_delivery_time=estimated_delivery_time,
            additional_discount_per_menu=additional_discount_per_menu,
            tags=tags,
        )

        url = photo_url
        resp = requests.get(url)
        if resp.status_code != requests.codes.ok:
            return

        fp = BytesIO()
        fp.write(resp.content)
        file_name = url.split("/")[-1]  # There's probably a better way of doing this but this is just a quick example
        new_rest.logo_url.save(file_name, files.File(fp))

    return HttpResponse('asda')
