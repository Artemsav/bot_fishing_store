from ast import Str
import requests
from dotenv import load_dotenv
import os
from pathlib import Path


def get_all_products(access_token: Str):
    url = 'https://api.moltin.com/v2/products'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_product(product_id: Str, access_token: Str):
    url = f'https://api.moltin.com/v2/products/{product_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def add_product_to_card(product_id: Str, access_token: Str, quantity: int):
    url = 'https://api.moltin.com/v2/carts/:reference/items'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    json_data = {
        'data': {
            'id': product_id,
            'type': 'cart_item',
            'quantity': quantity,
        },
    }
    response = requests.post(url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


def get_image(image_id: Str, access_token: Str):
    url = f'https://api.moltin.com/v2/files/{image_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    file_url = response.json().get('data').get('link').get('href')
    response = requests.get(file_url)
    response.raise_for_status()
    _, image_name = os.path.split(file_url)
    path = os.path.join(os.getcwd(), 'store_images')
    Path(path).mkdir(parents=True, exist_ok=True)
    named_path = os.path.join(path, image_name)
    with open(named_path, 'wb') as file:
        file.write(response.content)
    return named_path


if __name__ == '__main__':
    load_dotenv()
    products = {
        'gutted-carp-with-head': 'f8a358d9-bc59-4f6b-839b-e9ae6b880453',
        'gutted-cod-headless-chilled': '7a569aa3-140f-4969-8d42-6a405f243709',
        'sea-trout-murmansk-chilled-4-5kg-inarctica': 'c0f5cd03-fcdc-459e-88ca-6ac06e47e82e'
    }
    elastickpath_access_token = os.getenv('ELASTICPATH_ACCESS_TOKEN')
    #print(get_all_products(elastickpath_access_token))
    '''print(
        add_product_to_card(
            product_id=products.get('gutted-cod-headless-chilled'),
            access_token=elastickpath_access_token,
            quantity=1
            )
        )'''
    print(get_product('c0f5cd03-fcdc-459e-88ca-6ac06e47e82e', elastickpath_access_token))
    print(get_image('db8c95cd-3ff6-4176-a360-88097be72882', elastickpath_access_token))