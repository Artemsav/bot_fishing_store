from ast import Str
import requests
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


def add_product_to_card(card_id: Str, product_id: Str, access_token: Str, quantity: int):
    url = f'https://api.moltin.com/v2/carts/{card_id}/items'
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


def get_card(card_id: Str, access_token: Str):
    url = f'https://api.moltin.com/v2/carts/{card_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_card_items(card_id: Str, access_token: Str):
    url = f'https://api.moltin.com/v2/carts/{card_id}/items'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
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


def remove_cart_item(card_id: Str, product_id: Str, access_token: Str):
    url = f'https://api.moltin.com/v2/carts/{card_id}/items/{product_id}'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.delete(url, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    pass
