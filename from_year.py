import sys,traceback
from lxml import etree
from argparse import ArgumentParser
from db import *
from helper import print_results, AF_DAH_DOMAIN

def getall():
    return execute(_getall)

def _getall(cur):
    cur.execute("SELECT * FROM movies")
    return cur.fetchall()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        Y = 2015
        op = "="
    else:
        Y = sys.argv[1]
        if Y.startswith(">="):
            op = ">="
        elif Y.startswith("<="):
            op = "<="
        elif Y.startswith(">"):
            op = ">"
        elif Y.startswith("<"):
            op = "<"
        else:
            op = "="
        Y = Y.strip(op)
        Y = int(Y)
    movies = getall()
    try:
        print "Movies made",
        if op == ">=":
            movies = [i for i in movies if i[1] >= Y]
            print "after or in",
        elif op == "<=":
            movies = [i for i in movies if i[1] <= Y]
            print "before or in",
        elif op == ">":
            movies = [i for i in movies if i[1] > Y]
            print "after",
        elif op == "<":
            movies = [i for i in movies if i[1] < Y]
            print "before",
        else:
            movies = [i for i in movies if i[1] == Y]
            print "in",
        print Y
        print_results(movies)
    except KeyboardInterrupt:
        print "Quiting, bye!"
    except Exception,e:
        print traceback.format_exc()
