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

def pad(x,n):
    return ' '*(n-len(str(x)))+str(x)

if __name__ == '__main__':
    _N = 0
    if len(sys.argv) < 2:
        N = 10
    else:
        try:
            N = int(sys.argv[1])
        except:
            try:
                _N,N = map(int,sys.argv[1].split('-'))
            except:
                sys.exit()
    movies = getall()
    try:
        print "Top",N,"Movies"
        print_results(sorted(movies,key=lambda x: x[3])[::-1][_N:N])
    except KeyboardInterrupt:
        print "Quiting, bye!"
    except Exception,e:
        print traceback.format_exc()
