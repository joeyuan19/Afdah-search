import sys,traceback,math,datetime
from lxml import etree
from argparse import ArgumentParser
from db import *
from helper import print_results, AF_DAH_DOMAIN

def today():
    return datetime.datetime.today().strftime("%m/%d/%Y")

def date(d):
    return datetime.datetime.strptime(d,"%m/%d/%Y")

def getall():
    return execute(_getall)

def _getall(cur):
    cur.execute("""
    SELECT * FROM movies WHERE date_added=? AND date_removed=?;
    """,(today(),""))
    return cur.fetchall()

if __name__ == '__main__':
    movies = getall()
    try:
        print "Recently Added Movies"
        if len(movies) > 0:
            print_results(sorted(movies,key=lambda x: x[1])[::-1])
        else:
            print "None added today"
    except KeyboardInterrupt:
        print "Quiting, bye!"
    except Exception,e:
        print traceback.format_exc()
