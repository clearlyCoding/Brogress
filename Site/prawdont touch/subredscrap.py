from os.path import isfile
import praw
import math
#import pandas as pd
from time import sleep
import datetime
reddit = praw.Reddit(
    client_id='IKFVwCAgaXYJFg',
    client_secret='rR2nUs4Pu3-dENR5IzD3F5bgSceibw',
    user_agent='BrgScrp',
    username='developer_brog',
    password='developer')

class SubredditScraper():
    def __init__(self, sub, sort, lim, age_, gender_, height_):
        self.sub = sub
        self.sort = sort
        self.lim = lim
        self.age_ = age_
        self.gender_= gender_
        self.height_ = height_

    def scraper(self):
        postname=["","","","","","","","",""]
        countps= 0
        countMs = 0
        check = True
        f_count = 0
        arr = []
        if self.height_=='' or self.height_=='' or self.gender_=='':
            check = False
        for post in reddit.subreddit(self.sub).new(limit= self.lim):
            countps += 1
            print (countps, "/", self.lim)
            checkifsq_bracket = post.title.find('[')
            
            if checkifsq_bracket < 0:
                continue

            abstime = self.time_utc(post)[0]
            _dat_=self.time_utc(post)[1]
            count1 = 0
            cols = []
            postname = post.title.split("/")
            #check for three splits
            if len(postname)<=2:
                continue
                
            gndr = postname[0]           

            if len(postname) > 1:
                age = postname[1]
            else:
                continue

            deltatime=self.clean_time(postname[2])
            ft_ = self.clean_Height(postname[2]) 
            weight = self.clean_weight(post)
            pid = "https://old.reddit.com/r/brogress/comments/"+ post.id
            pics = post.url

            details = ""
            skipflag = False
            for coms in post.comments:
                if coms.author == post.author:
                    body_ = coms.body
                    details= details + "\n" + body_

            if skipflag:
                continue

            if ("gallery" in post.url 
                or "imgur" in post.url 
                or "youtube" in post.url
                or "comments" in post.url):
                continue

            if check:
                if age == self.age_ and ft_ == self.height_  and gndr  == self.gender_:
                    cols=[gndr,age,ft_,weight,pid,post.url,_dat_,deltatime,details,abstime]
                    arr.append(cols)

            else:
                cols=[gndr,age,ft_,weight,pid,post.url,_dat_,deltatime, details, abstime]
                arr.append(cols)

        return(arr)

    def clean_time(self, postname):
        #print(postname)
        deltatime=""
        _deltaLOCK = postname.find('(')
        deltaLOCK_ = postname.find(')')
        deltaLOCK=""
        if _deltaLOCK >0 and deltaLOCK_ >0 :
            deltaLOCK = postname[_deltaLOCK+1:deltaLOCK_]
        if (deltaLOCK.find('Years') >0 
            or deltaLOCK.find('month') >0
            or deltaLOCK.find('Year') >0
            or deltaLOCK.find('Months') >0
            or deltaLOCK.find('years') > 0
            or deltaLOCK.find('months') >0):
                deltatime =deltaLOCK
        else:
            deltatime=""
        return deltatime


    def clean_Height(self,postname):
        Height = postname.split("[")[0]
        ft_ = Height.replace('"','')
        ft_ = ft_.replace(chr(8221),'')
        ft_ = ft_.replace(" ","")
        if "cm" in ft_ :
            ft_=ft_.replace("cm","")
            cmCONV= (float(ft_)/2.54)
            ft_=str(math.trunc(cmCONV/12)) + "'" + str(math.trunc(cmCONV % 12))
        return ft_

    def clean_weight (self, post):
        wieghtc = post.title.split("[")
        weightclass = post.title.split("[")[1].split("]")
        weight = weightclass[0]
        if ('kg' in weight 
            or 'kgs' in weight):
            pof_TO = weight.find('to')
            if pof_TO < 0:
                pof_dash = weight.find('-')
            if pof_TO > 0:
                weight1 = weight[:pof_TO]
            else:
                weight1 = weight[:pof_dash]
            pof_kg = weight1.find('k')
            if pof_kg >0:
                weight1 = weight1[:pof_kg]
            weight1 = weight1.replace(" ","") 
            if pof_TO >0:
                weight2 = weight[pof_TO+2:]
            else:
                weight2 = weight[pof_dash+1:]
            pof_kg = weight2.find('k')
            weight2 = weight2[:pof_kg]
            weight2 = weight2.replace(" ","")
            weight1 = math.trunc(float(weight1)*2.20)
            weight2 = math.trunc(float(weight2)*2.20)
            weight = str(weight1) + "lbs to " + str(weight2) + "lbs"
        return weight

    def time_utc(self, post):
        abstime =str(datetime.datetime.fromtimestamp(post.created_utc))
        abstime = abstime.replace(" ","").replace(":","")
        abstime = abstime[-6:]
        date_ = str(datetime.date.fromtimestamp(post.created))
        return abstime, date_

# #import pandas as pd
# from time import sleep
# import praw
# reddit = praw.Reddit()

# class SubredditScraper():
#     def __init__(self, sub, sort, lim, age_, gender_, height_):
#         self.sub = sub
#         self.sort = sort
#         self.lim = lim
#         self.age_ = age_
#         self.gender_= gender_
#         self.height_ = height_
        
#     def scraper(self):
#         postname=["","","","",""]
#         countps= 0
#         countMs = 0
#         check = True
#         arr = []
#         if self.height_=='' or self.height_=='' or self.gender_=='':
#             check = False
#         for post in reddit.subreddit(self.sub).new(limit= self.lim):
#             count1 = 0
#             cols = []
#             postname = post.title.split("/")
#         from os.path import isfile
#             gndr = postname[0]
#             if len(postname) > 1:
#                 age = postname[1]
#             else:
#                 continue
#             Height = postname[2].split("[")[0]
#             ft_ = Height.replace('"','')
#             ft_ = ft_.replace(chr(8221),'')
#             ft_ = ft_.replace(" ","")
#             wieghtc = post.title.split("[")
#             weightclass = post.title.split("[")[1].split("]")
#             weight = weightclass[0]
#             pid = "https://old.reddit.com/r/brogress/comments/"+ post.id
#             pics = post.url
#             countps +=1
#             if check:
#                 if age == self.age_ and ft_ == self.height_  and gndr  == self.gender_:
#                     cols=[gndr,age,ft_,weight,pid,post.url]
#                     arr.append(cols)
#                     countps += 1
#             else:
#                 cols=[gndr,age,ft_,weight,pid,post.url]
#                 arr.append(cols)
#                 countps += 1            
#         return(arr)

            
       
