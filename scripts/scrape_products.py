"""Extract Lazora product records from the initial HTML, without a browser."""
import argparse
import json
from html.parser import HTMLParser
from urllib.request import Request, urlopen

FIELDS = (
    'source_platform', 'title', 'price', 'currency', 'seller_id',
    'seller_name', 'selling_since', 'rating', 'review_count', 'review', 'product_url',
)


class ProductDataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_catalog = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'script' and attributes.get('id') == 'product-data':
            self.in_catalog = True

    def handle_data(self, data):
        if self.in_catalog:
            self.parts.append(data)

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_catalog = False


def extract_products(html):
    parser = ProductDataParser()
    parser.feed(html)
    if not parser.parts:
        raise ValueError('No #product-data JSON catalogue found in HTML')
    records = json.loads(''.join(parser.parts))
    return [
        {**{field: product[field] for field in FIELDS},
         'review': [{field: review[field] for field in ('text', 'rating', 'date')}
                    for review in product['review']]}
        for product in records
    ]


if __name__ == '__main__':
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument('url', help='Storefront URL, including repository path')
    args = cli.parse_args()
    request = Request(args.url, headers={'User-Agent': 'LazoraCatalogueReader/1.0'})
    with urlopen(request, timeout=30) as response:
        html = response.read().decode('utf-8')
    print(json.dumps(extract_products(html), ensure_ascii=False, indent=2))
