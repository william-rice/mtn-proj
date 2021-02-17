# mtn-proj

`mp-bot.py` uses Selenium to navigate through mountain project's site, downloading route data from various areas as csv files and storing them in the folder `csv-routes`.

`union-csvs.ipynb` opens that folder, reads in all the csv data,  combines that data into one frame, and writes the combined result out into the file `scraped.csv` (so named because this data was scraped from the site using `mp-bot.py`).

`request-routes.ipynb` opens `scraped.csv` to read off the route IDs from the URL column, queries the Mountain Project API for more data on those routes, and stores the responses as json files in the `json-routes` folder.

`combine_routes.ipynb` merges the scraped data with the queried data for a more complete dataset, writing the result to the `merged.csv` file.

`exploratory.ipynb` runs exploratory data analyses on the full dataset, and contains visualizations for a subset (three climbing areas) of the route data.

---

Update: Unfortunately, the Mountain Project Data API is no longer available, so this project is now discontinued.

A few visualizations with the data I was able to pull before the API went down remain visible [here](https://nbviewer.jupyter.org/github/william-rice/mtn-proj/blob/main/exploratory.ipynb).
