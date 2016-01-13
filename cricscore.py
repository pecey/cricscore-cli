# Uses http://cricscore-api.appspot.com/ for receiving data

import urllib2
import json
import time
import optparse

def getScore(matchId, summary="", modTime="",lastScore=""):
    url = "http://cricscore-api.appspot.com/csa?id="
    headers = {'If-Modified-Since':modTime}
    req = urllib2.Request(url+str(matchId),headers=headers)
    html = urllib2.urlopen(req)

    if html.code == 200:
        data = json.load(html)
        summary = data[0]['de']
        modTime = html.headers['last-modified']
        if summary==lastScore:
            pass
        else:
            print summary
            
        lastScore=summary
        return (lastScore, modTime)
    elif html.code == 304:
        pass
    else:
        print "The website returned "+str(html.code)

def getMatchListing(index=""):
    counter=1
    url = "http://cricscore-api.appspot.com/csa"
    html = urllib2.urlopen(url)
    if html.code == 200:
        data = json.load(html)
        print "Fetching Match List : \n"
        if not index:
            for element in data:
                print "["+str(counter)+"]"+element['t1']+" vs "+element['t2']
                counter=counter+1
            counter = input("Select match index to view current score : ")
        else:
            counter=int(index)
        return data[counter-1]['id']
    else:
        print "The website returned "+str(html.code)



def main():
    parser = optparse.OptionParser(usage = "")
    parser.add_option("-i", "--index", action="store", dest="index", default=None, help="Match index. Retrieved from match listing")
    parser.add_option("-t", "--time", action="store", dest="interval", default=30, help="Seconds after which to fetch scores")
    (options,args) = parser.parse_args()

    # Storing values in local arguments
    index = options.index
    interval = options.interval

    index = getMatchListing(index=index)
    modTime = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(0))
    while True:
        (lastScore,modTime)=getScore(index,modTime=modTime,lastScore=0)
        time.sleep(60)


if __name__ == "__main__":
    main()