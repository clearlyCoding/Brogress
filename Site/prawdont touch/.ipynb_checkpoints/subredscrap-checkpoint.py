from os.path import isfile
import praw
#import pandas as pd
from time import sleep
reddit = praw.Reddit()

class SubredditScraper():
    def __init__(self, sub, sort, lim, age_, gender_, height_):
        self.sub = sub
        self.sort = sort
        self.lim = lim
        self.age_ = age_
        self.gender_= gender_
        self.height_ = height_
        
    def scraper(self):
        postname=["","","","",""]
        countps= 0
        countMs = 0
        check = True
        arr = []
        if self.height_=='' or self.height_=='' or self.gender_=='':
            check = False
        for post in reddit.subreddit(self.sub).new(limit= self.lim):
            count1 = 0
            cols = []
            postname = post.title.split("/")
            gndr = postname[0]
            age = postname[1] if len(postname) > 1 else continue
            Height = postname[2].split("[")[0] > 2 else continue
            ft_ = Height.replace('"','')
            ft_ = ft_.replace(chr(8221),'')
            ft_ = ft_.replace(" ","")
            wieghtc = post.title.split("[")
            weightclass = post.title.split("[")[1].split("]")
            weight = weightclass[0]
            pid = "https://old.reddit.com/r/brogress/comments/"+ post.id
            pics = post.url
            countps +=1
            if check:
                if age == self.age_ and ft_ == self.height_  and gndr  == self.gender_:
                    cols=[gndr,age,ft_,weight,pid,post.url]
                    arr.append(cols)
                    countps += 1
            else:
                cols=[gndr,age,ft_,weight,pid,post.url]
                arr.append(cols)
                countps += 1            
        print(arr)

            
       