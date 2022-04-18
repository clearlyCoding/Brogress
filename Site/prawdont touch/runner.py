

import subredscrap

s = subredscrap.SubredditScraper

tup=s("brogress", sort = "new", lim = 100, age_ = "", gender_="", height_="").scraper()


for elements in tup:
    print(elements)

