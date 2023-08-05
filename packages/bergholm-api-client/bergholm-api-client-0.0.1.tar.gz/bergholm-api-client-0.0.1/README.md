# Bergholm API Client
Simple Client to fetch products from http://www.bergholm.com/

## Install package
``` pip install bergholm-api-client ```

## Usage
```
from bergholm.api import Client

client = Client()

client.get_all_cihb()
client.get_products_by_family_id(012)
client.get_models_by_family_id(345)
client.get_images_by_family_id(678)
client.get_information_by_model_id(910)
```
