import sys,traceback,math
from lxml import etree
from argparse import ArgumentParser
from db import *
from helper import print_results, AF_DAH_DOMAIN

def getall():
    return execute(_getall)

def _getall(cur):
    cur.execute("""
    SELECT * FROM movies;
    """)
    return cur.fetchall()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        N = 10
    else:
        N = int(sys.argv[1])
    movies = getall()
    try:
        print N,"Longest Movies"
        print_results(sorted(movies,key=lambda x: x[4])[::-1][:N])
    except KeyboardInterrupt:
        print "Quiting, bye!"
    except Exception,e:
        print traceback.format_exc()
