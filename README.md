# mtn-proj

mp-bot.py will use Selenium to navigate through mountain project's site, downloading routes from various areas.

mp-request.py will pull the route-IDs from the downloaded data in order to query the site's API (which offers limited complimentary data). It will then augment the scraped data with the queried data.

exploratory.ipynb is a Jupyter Notebook for running exploratory data analyses on the full dataset.

The remaining files are for building data visualizations to be hosted on GitHub pages.

Possible additions may include building new app features (like a route recommender) from the data.
