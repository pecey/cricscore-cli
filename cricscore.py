# Uses http://cricscore-api.appspot.com/ for receiving data

import urllib2
import json
import time
import optparse

def getScore(matchId, summary="", modTime="",lastScore=""):
    url = "http://cricscore-api.appspot.com/csa?id="
    if not modTime:
        headers = {'If-Modified-Since':modTime}
        req = urllib2.Request(url+str(matchId),headers=headers)
    else:
         req = urllib2.Request(url+str(matchId))
    html = urllib2.urlopen(req)
    if html.code == 200:
        data = json.load(html)
        summary = data[0]['de']
        if summary==lastScore:
            pass
        else:
            print summary
            lastScore=summary
        timestamp = time.time()
        modTime = time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime(timestamp))
    else:
        pass
    time.sleep(1)
    getScore(matchId, summary,modTime, lastScore)


def getMatchListing():
    print "Fetching Match List : \n"
    index=1
    url = "http://cricscore-api.appspot.com/csa"
    html = urllib2.urlopen(url)
    if html.code == 200:
        data = json.load(html)
        for element in data:
            print "["+str(index)+"]"+element['t1']+" vs "+element['t2']
            index=index+1
        index = input("Select match index to view current score : ")
        getScore(data[index-1]['id'],lastScore=" ")
    else:
        print "The website returned "+str(html.code)



def main():
    getMatchListing()


if __name__ == "__main__":
    main()