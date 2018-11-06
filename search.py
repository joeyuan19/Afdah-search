import sys,traceback,math
from lxml import etree
from argparse import ArgumentParser
from db import *
from helper import print_results, AF_DAH_DOMAIN


def is_common(word):
    common_words = [
        'the',
        'in',
        'the',
        'of',
        'that',
        'a',
        'and',
        'it',
        'for',
        'not'
        'on',
        'with',
        'as',
        'at',
        'this',
        'by',
        'they',
        'from',
        'we',
    ]
    return word in common_words

def getall():
    return execute(_getall)

def _getall(cur):
    cur.execute("""
    SELECT * FROM movies;
    """)
    return cur.fetchall()

def parse_args():
    p = ArgumentParser()
    p.add_argument("-f","--full-search",action="store_true",dest="full_search",
        help="include common words",default=False)
    p.add_argument("--sort",dest="sort_key",
        help="Sort by rating (highest to lowest)",default=False)
    p.add_argument("search_keys",help="Keys to search on.  "+
        "Common words like 'the, it, that' are filtered out by default...",
        default='',nargs='*')
    return p.parse_args()

if __name__ == '__main__':
    args = parse_args()
    s = [i.lower() for i in args.search_keys]
    
    if len(s) == 0:
        print "No search terms provided"
        sys.exit()
    
    if not args.full_search:
        s = [i for i in s if not is_common(i)]
        if len(s) == 0:
            print "Warning: Only common words provided, searching on all keys..."
            s = [i.lower() for i in args.search_keys]
    
    
    movies = getall()
    results = []
    try:
        for movie in movies:
            if args.full_search and len([i for i in s if i in movie[0].lower()]) > 0:
                results.append(movie)
            elif len([i for i in s if i in movie[0].lower()]) == len(s):
                results.append(movie)
        print "Found",len(results),"matches"
        if len(results) > 0:
            if args.sort_key == "rating":
                results = sorted(results,key=lambda x: x[3])[::-1]
            elif args.sort_key == "time":
                results = sorted(results,key=lambda x: x[4])[::-1]
            elif args.sort_key == "alpha":
                results = sorted(results,key=lambda x: x[0])
            print_results(results,s)
    except KeyboardInterrupt:
        print "Quiting, bye!"
    except Exception,e:
        print traceback.format_exc()
