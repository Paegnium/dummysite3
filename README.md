# Lazora

A responsive shopping storefront inspired by the Lazada marketplace aesthetic, with a distinct brand, real product names, category browsing, search, sorting, product details, illustrative ratings/review previews, favourites and a persistent cart. Currency: SGD.

## Run locally

No installation or build step is needed. From the repository directory:

```sh
python3 -m http.server 8000 --bind 0.0.0.0
```

Open the site using your local development browser. All paths are relative, including local product images and fonts, so deployment works under a GitHub Pages repository subpath.

## Publish on GitHub Pages

1. Push this repository to `main`.
2. In the repository's **Settings → Pages**, select **GitHub Actions** as the build/deployment source.
3. The included `pages.yml` workflow deploys automatically on a push to `main`; it can also be run manually.

The site is ready for `https://paegnium.github.io/dummysite3/` once Pages deployment succeeds. No deployment has been performed by the local setup.

## Behaviour and scope

- Cart quantities and saved products persist through `localStorage` on the same browser. Storage failure gracefully keeps the current session usable.
- Search matches product names, brands and categories. Empty results have a reset action.
- Product dialogs include two illustrative review previews per product; these are not sourced customer endorsements. Ratings, review counts, prices, discounts and delivery terms are illustrative.
- Checkout summarizes the cart and clearly explains that online ordering is unavailable. No orders, payments or personal data are submitted.
- The newsletter form validates an email address locally, explains subscriptions are unavailable, and neither stores nor transmits addresses.
- There is no affiliation with Lazada or the featured product manufacturers.

## Assets

Product photography is bundled from the public example catalogue at [Fake Store API](https://github.com/keikaavousi/fake-store-api) (MIT project; notice retained in `assets/ASSET-NOTICES.txt`). Product trademarks and photography remain the property of their respective owners; review usage rights before commercial use.

The Poppins font is bundled from [DummyJSON](https://github.com/Ovi/DummyJSON); its SIL Open Font License is retained in `assets/OFL.txt`.
