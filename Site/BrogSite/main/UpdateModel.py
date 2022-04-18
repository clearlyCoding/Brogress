# from django.conf import settings
# settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
#     TEMPLATE_DIRS=('/home/web-apps/myapp', '/home/web-apps/base'))

#from models import Scrape
from . import scrape
from . import models
# Create your views here.

def homepage(request):
    s = scrape.SubredditScraper
    tup=s("brogress", sort = "new", lim = 100, age_ = "", gender_="", height_="").scraper()
    for elements in tup:
        post_ = models.Scrape()
        post_.Scrape_gender = elements[0]
        post_.Scrape_age = elements[1]
        post_.Scrape_weight =elements[3]
        post_.Scrape_height =elements[2]
        post_.Scrape_pid = elements[4]
        post_.Scrape_url = elements [5]
        post_.save()
        break