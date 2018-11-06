import math

AF_DAH_DOMAIN = "https://afdah.org"

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def hms(seconds):
    h = seconds/(60*60)
    m = seconds%(60*60)/60
    s = seconds%60
    h = str(h)
    m = str(m)
    s = str(s)
    return h+":"+m+":"+s

def pad(x,n):
    return ' '*max(0,(n-len(str(x))))+str(x)

def to_string(n,result,indent,search=None):
    if search is None:
        search = []
    return _to_string(n,result[0],result[2],result[3],result[1],result[4],result[5].split(','),indent,search)

def surround(s,terms):
    indexes = []
    ls = s.lower()
    for term in terms:
        lterm = term.lower()
        idx = ls.find(lterm)
        while idx >= 0:
            indexes.append((idx,idx+len(lterm)))
            idx = ls.find(lterm,idx+len(lterm))
    c = True
    while c:
        c = False
        i = 0
        while i < len(indexes)-1:
            if indexes[i][1] >= indexes[i+1][0]:
                tmp = (indexes[i][0],indexes[i+1][1])
                indexes.pop(i+1)
                indexes.pop(i)
                indexes.insert(i,tmp)
                c = True
            i += 1
    out = list(s)
    for r in indexes[::-1]:
        out.insert(r[1],color.END)
        out.insert(r[0],color.UNDERLINE)
        out.insert(r[0],color.BOLD)
    return ''.join(out)

def _to_string(n,title,href,rating,year,time,categories,indent,search=[]):
    p = []
    for term in title.split():
        if term.lower() in search:
            p.append(color.UNDERLINE+color.BOLD+term+color.END)
        else:
            partials = [i for i in search if i in term.lower()]
            if len(partials) > 0:
                p.append(surround(term,partials))
            else:
                p.append(term)
    out = ""
    out += color.YELLOW+pad(n,indent-1)+'.'+color.END + " "
    out += color.CYAN+'Title:'+color.END+" "+' '.join(i for i in p) + "\n"
    out += ' '*indent+" "+color.CYAN+"Year:"+color.END+" "+str(year)+'  '+color.CYAN+"Rating:"+color.END+" "
    if rating < 0:
        out += "N/A "
    elif rating < 3:
        out += color.RED+str(rating)+color.END+" "
    elif rating < 6:
        out += color.YELLOW+str(rating)+color.END+" "
    else:
        out += color.GREEN+str(rating)+color.END+" " 
    out += " "
    out += color.CYAN+'Length:'+color.END+" "
    out += hms(time)+"\n"
    out += ' '*indent+" "+color.CYAN+'Categories:'+color.END+" "+','.join(i for i in categories)+"\n"
    out += ' '*indent+" "+color.CYAN+'URL:'+color.END+" "
    out += AF_DAH_DOMAIN+href+"\n"
    return out

def print_results(results,search=None):
    if len(results) > 0:
        if search is None:
            search = []
        idt = int(math.log10(len(results)))+2
        i = 1
        for result in results:
            print to_string(i,result,idt,search)
            i += 1
    else:
        print "No Results"


