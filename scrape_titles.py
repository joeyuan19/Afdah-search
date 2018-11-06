import urllib2
import sys
import sqlite3
import re
import datetime
from lxml import etree
from db import *

AF_DAH_DOMAIN = "https://afdah.org"

def today():
    return datetime.datetime.today().strftime("%m/%d/%Y")

def date(d):
    return datetime.datetime.strptime(d,"%m/%d/%Y")

def percent(n):
    if n == 0:
        return "0%"
    elif n < 0.0001:
        return "<0.01%"
    else:
        n = str(n)
        idx = n.find(".")
        if idx < 0:
            return n+"%"
        else:
            return n[:idx+3]+"%"

def drop():
    return execute(_drop)

def _drop(cur):
    try:
        cur.execute("""
        DROP TABLE movies;
        """)
        return True
    except sqlite3.OperationalError:
        return False

def init():
    return execute(_init)

def _init(cur):
    try:
        cur.execute("""
        CREATE TABLE movies (title, year, link, rating, time, categories, date_added, date_updated, date_removed, watched, primary key (title,year));
        """)
        return True
    except sqlite3.OperationalError:
        return False

def insert(title,link,year,rating,time,categories):
    return execute(_insert,title,link,year,rating,time,categories)

def _insert(cur,title,link,year,rating,time,categories):
    try:
        cur.execute("""
        INSERT INTO movies (title,link,year,rating,time,categories,date_added,date_updated,date_removed,watched) VALUES (?,?,?,?,?,?,?,?,?,?);
        """,(title,link,year,rating,time,categories,today(),today(),"",False))
        return 1
    except sqlite3.IntegrityError:
        try:
            cur.execute("""
            UPDATE movies
            SET link=?,
            rating=?,
            time=?,
            categories=?,
            date_updated=?,
            date_removed=?
            WHERE title=? AND year=?;
            """,(link,rating,time,categories,today(),"",title,year))
            return 2
        except sqlite3.OperationalError,e:
            write_err(e)
            return 0
    except Exception,e:
        write_err(e)
        return 0

def getall():
    return execute(_getall)

def _getall(cur):
    cur.execute("SELECT * FROM movies")
    return cur.fetchall()

def mark_removed(title,):
    return execute(_mark_removed)

def _mark_removed(cur):
    cur.execute("""
    UPDATE movies
    SET date_removed=?
    WHERE date_updated<>? AND date_removed<>?
    """,(today(),today(),""))

def get_text(elm):
    return ''.join(i for i in elm.itertext())

def scrape_page(page):
    node = etree.HTML(page)
    i,u,e,t = 0,0,0,0
    title,url,year,categories = '','','',''
    inserts = []
    for video in node.findall(r'.//div[@class="cell_container"]'):
        for link in video.findall(r'.//div[@class="video_title"]/h3/a'):
            if 'title' in link.attrib:
                title = get_text(link)
                url = link.attrib['href']
        for link in video.findall(r'.//div[@class="video_quality"]'):
            itr = link.itertext()
            year = ''
            for elm in itr:
                year += elm.strip()
            li = re.findall(r'Year:\s*(\d+)',year)
            if len(li) > 0:
                year = int(li[0])
            else:
                year = -1
        for link in video.findall(r'.//div[@class="video_rating"]'):
            rating = ''.join(i.strip() for i in link.itertext())
            li = re.findall(r'Rating:\s*(\d+.\d+)',rating)
            if len(li) > 0:
                rating = float(li[0])
            else:
                rating = -1
        for link in video.findall(r'.//span[@class="video_time"]'):
            time = ''.join(i.strip() for i in link.itertext())
            time = re.findall(r'((\d+):)?(\d+):(\d+)',time)
            if len(time) > 0:
                time = time[0]
                h,m,s = [(lambda x: int(el) if el.isdigit() else 0)(el) for el in time[1:]]
                time = h*60*60+m*60+s
            else:
                time = -1
        for link in video.findall(r'.//div'):
            categories = get_text(link)
            if categories.lower().startswith("genres:"):
                categories = categories[len("genres:"):]
                categories = ','.join(i.strip() for i in categories.split(','))
                break
            else:
                categories = ''
        r = insert(title,url,year,rating,time,categories)
        inserts.append((title,url,year,rating,time,categories))
        if r == 0:
            e += 1
        elif r == 1:
            i += 1
        elif r == 2:
            u += 1
        t += 1
    return i,u,e,t,inserts

if __name__ == '__main__':
    try:
        #drop()
        init()
    except sqlite3.OperationalError:
        pass # Table exists
    try:
        last = ''
        inserted = 0
        updated = 0
        errors = 0
        total = 0
        last_page = []
        new_page = []
        page = 1
        last = []
        new = ['']
        while last != new:
            last = new
            try:
                o = urllib2.build_opener()
                o.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0")]
                last_page = new_page
                new_page = ''.join(i for i in o.open(AF_DAH_DOMAIN+'/?page='+str(page)))
                i,u,e,t,new = scrape_page(new_page)
                inserted += i
                updated += u
                errors += e
                total += t
                print "Page",page
                print "\tInserted :\t",i,"\tRunning Total:",inserted
                print "\tUpdated  :\t",u,"\tRunning Total:",updated
                print "\tErrors   :\t",e,"\tRunning Total:",errors
                print "\tTotal    :\t",t,"\tRunning Total:",total
                page += 1
            except Exception,e:
                write_err(e)
        ftotal = float(total)
        print
        print "Final Totals:"
        print "\tInserted :",inserted,'\t',percent(100*(inserted/ftotal))
        print "\tUpdated  :",updated,'\t',percent(100*(updated/ftotal))
        print "\tErrors   :",errors,'\t',percent(100*(errors/ftotal))
        print "\tTotal    :",total,'\t',percent(100*(total/ftotal))
        
    except KeyboardInterrupt:
        print "Stopped scrape at page",i

