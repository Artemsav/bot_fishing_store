data = {'data': [{'id': 'f73c387d-a08c-42e0-86b7-82e560042617', 'type': 'cart_item', 'product_id': 'c0f5cd03-fcdc-459e-88ca-6ac06e47e82e', 'name': 'Sea trout Murmansk chilled, 4-5kg Inarctica', 'description': 'Морская форель INARCTICA – выбор тех, что заботится о своем здоровье. Форель - это любимое блюдо в ресторанах и кафе во всем мире, но еще больше ее любят те, кто готовит дома. Существует множество простых и вкусных способов приготовления: от жарки и запекания до засола и копчения. Ни что не сравнится с великолепным вкусом и пользой охлажденного продукта. Охлажденная форель INARCTICA производится на фермах в Арктике в чистой ледяной воде, в окружении уникальной флоры и фауны. Артика – идеальная среда, созданная самой природой для выращивания морской форели.Продукция, изготовленная из аквакультурного атлантического лосося INARCTICA, не содержит усилителей вкуса, антибиотиков и ГМО.Продукция INARCTICA сертифицирована в СДС «Халяль». Сертификат подтверждает отсутствие добавок в продукте противоречащих стандартам «Халяль», а также что при переработке соблюдаются необходимые гигиенические требования.', 'sku': '1000010', 'slug': 'sea-trout-murmansk-chilled-4-5kg-inarctica', 'image': {'mime_type': 'image/jpeg', 'file_name': 'ru_pim_116851001001_01.jpg', 'href': 'https://files-eu.epusercontent.com/37bb2aa8-58ab-4973-ada9-2a187103036a/db8c95cd-3ff6-4176-a360-88097be72882.jpg'}, 'quantity': 3, 'manage_stock': True, 'unit_price': {'amount': 5000, 'currency': 'USD', 'includes_tax': True}, 'value': {'amount': 15000, 'currency': 'USD', 'includes_tax': True}, 'links': {'product': 'https://api.moltin.com/v2/products/c0f5cd03-fcdc-459e-88ca-6ac06e47e82e'}, 'meta': {'display_price': {'with_tax': {'unit': {'amount': 5000, 'currency': 'USD', 'formatted': '$50.00'}, 'value': {'amount': 15000, 'currency': 'USD', 'formatted': '$150.00'}}, 'without_tax': {'unit': {'amount': 5000, 'currency': 'USD', 'formatted': '$50.00'}, 'value': {'amount': 15000, 'currency': 'USD', 'formatted': '$150.00'}}, 'tax': {'unit': {'amount': 0, 'currency': 'USD', 'formatted': '$0.00'}, 'value': {'amount': 0, 'currency': 'USD', 'formatted': '$0.00'}}, 'discount': {'unit': {'amount': 0, 'currency': 'USD', 'formatted': '$0.00'}, 'value': {'amount': 0, 'currency': 'USD', 'formatted': '$0.00'}}}, 'timestamps': {'created_at': '2022-06-06T16:40:05Z', 'updated_at': '2022-06-06T16:41:17Z'}}, 'catalog_source': 'legacy'}], 'meta': {'display_price': {'with_tax': {'amount': 15000, 'currency': 'USD', 'formatted': '$150.00'}, 'without_tax': {'amount': 15000, 'currency': 'USD', 'formatted': '$150.00'}, 'tax': {'amount': 0, 'currency': 'USD', 'formatted': '$0.00'}, 'discount': {'amount': 0, 'currency': 'USD', 'formatted': '$0.00'}}, 'timestamps': {'created_at': '2022-06-06T16:40:05Z', 'updated_at': '2022-06-06T16:41:17Z', 'expires_at': '2022-06-13T16:41:17Z'}}}
products_list = []
card_total_price = 10000
for item in data.get('data'):
    item_name = item.get('name')
    item_quantity = item.get('quantity')
    item_price_per_item = item.get('meta').get('display_price').get('with_tax').get('unit').get('formatted')
    item_total_price = item.get('meta').get('display_price').get('with_tax').get('value').get('formatted')
    products_describtion = f'{item_name}\n{item_price_per_item} per kg\n{item_quantity}kg in cart for {item_total_price}\n\n'
    products_list.append(products_describtion)
all_products = ''.join(product for product in products_list)
card_message = f'{all_products}Total:{card_total_price}$'
print(card_message)