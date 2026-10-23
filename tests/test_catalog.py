"""Verify the public scraping contract against the actual deployment HTML."""
import json
from datetime import date
from pathlib import Path
import unittest
from urllib.parse import urlsplit

from scripts.scrape_products import FIELDS, ProductDataParser, extract_products

ROOT = Path(__file__).resolve().parents[1]


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / 'index.html').read_text()
        cls.products = extract_products(cls.html)

    def test_all_products_have_requested_fields(self):
        self.assertEqual(len(self.products), 8)
        for product in self.products:
            with self.subTest(product=product['title']):
                self.assertEqual(set(product), set(FIELDS))
                for field in ('source_platform', 'title', 'seller_id', 'seller_name'):
                    self.assertIsInstance(product[field], str)
                    self.assertTrue(product[field].strip())
                self.assertEqual(product['source_platform'], 'Lazora')
                self.assertEqual(product['currency'], 'SGD')
                self.assertIsInstance(product['price'], (int, float))
                self.assertGreater(product['price'], 0)
                self.assertGreaterEqual(product['rating'], 1)
                self.assertLessEqual(product['rating'], 5)
                self.assertIsInstance(product['review_count'], int)
                self.assertGreaterEqual(product['review_count'], len(product['review']))
                self.assertTrue(product['review'])
                since = date.fromisoformat(product['selling_since'])
                for review in product['review']:
                    self.assertEqual(set(review), {'text', 'rating', 'date'})
                    self.assertTrue(review['text'].strip())
                    self.assertGreaterEqual(review['rating'], 1)
                    self.assertLessEqual(review['rating'], 5)
                    self.assertGreaterEqual(date.fromisoformat(review['date']), since)

    def test_unique_product_urls_and_consistent_sellers(self):
        urls = [p['product_url'] for p in self.products]
        self.assertEqual(len(set(urls)), len(urls))
        sellers = {}
        for product in self.products:
            url = urlsplit(product['product_url'])
            self.assertEqual((url.scheme, url.netloc, url.path),
                             ('https', 'paegnium.github.io', '/dummysite3/'))
            self.assertRegex(url.fragment, r'^product-[1-8]$')
            seller = (product['seller_name'], product['selling_since'])
            self.assertEqual(sellers.setdefault(product['seller_id'], seller), seller)

    def test_catalogue_assets_exist(self):
        parser = ProductDataParser()
        parser.feed(self.html)
        for product in json.loads(''.join(parser.parts)):
            self.assertTrue((ROOT / 'assets' / product['image']).is_file())

    def test_missing_catalogue_is_an_error(self):
        with self.assertRaisesRegex(ValueError, 'No #product-data'):
            extract_products('<html><body>No catalogue</body></html>')


if __name__ == '__main__':
    unittest.main()
