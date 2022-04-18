from django.db import models
#import scrape

# Create your models here.
class Scrape(models.Model):
    Scrape_gender = models.CharField(max_length=50, default ='M/F')
    Scrape_age = models.CharField(max_length=50, default = '####')
    Scrape_weight = models.CharField(max_length=200, default = 'weight class')
    Scrape_height = models.CharField(max_length=50, default = "#'#")
    Scrape_pid = models.CharField(max_length=50, default = 'zzzzzzz')
    Scrape_url = models.CharField(max_length=500, default = 'www.www.www')
    Scrape_date = models.CharField(max_length=500, default = '00000000')
    Scrape_len = models.CharField(max_length=500, default = '(##) Years (##) Months')
    Scrape_coms = models.CharField(max_length=1500, default = "")
    Scrape_abstime = models.CharField(max_length= 10, default ="0000000000")
    def __str__(self):
        return (self.Scrape_pid)

#add abstime


