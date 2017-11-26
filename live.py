#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 22:27:18 2017

@author: hakandemirel
"""

import requests
import subprocess 

f = open('livebak.m3u8', 'w')
f.write("#EXTM3U\n") 
f.close()

def linksolver( url ):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive',}
        req = requests.get(url, headers=headers)
        test = req.text
        lhs, rhs = test.split("source: \'",1)
        source , newrhs = rhs.split("\',\n",1)
        return source

def trlinksolver( url ):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive',}
        req = requests.get(url, headers=headers)
        test = req.text
        lhs, rhs = test.split("source: \'",1)
        source , newrhs = rhs.split("\',\n",1)
        return source    

def linksolver2( url ):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive',}
        req = requests.get(url, headers=headers)
        test = req.text
        left,right = test.split('/"'+">Video yay",1)
        new = left.split('/tr',-1)
        livetv= "http://livetv.sx/tr"+ new[-1]
        #http://livetv.sx/tr/eventinfo/556934_san_lorenzo_lanus/
        req = requests.get(livetv, headers=headers)
        #http://livetv.sx/tr/eventinfo/556934_san_lorenzo_lanus/
        test = req.text
        left,right=test.split('id="links_block"',1)
        nleft,nright=right.split('id="comblockabs"',1)
        source=nleft
        start_sep='href="//'
        end_sep='si=1">'
        result=[]
        tmp=source.split(start_sep)
        for par in tmp:
            if end_sep in par:
                result.append(par.split(end_sep)[0])
        for i in range(0,len(result)):
            result[i] = "http://" + result[i] + "si=1"
        req = requests.get(result[0], headers=headers)
        test = req.text
        print(result)
        return result
try:
    for i in range(1, 12):
        request = requests.get(linksolver("http://www.livinstream.org/live/?channel="+str(i)))
        if request.status_code == 200:
            print('Web site exists')
            print(i)
            with open("livebak.m3u8", "a") as myfile:
                myfile.write("#EXTINF:0,LIG TV "+str(i)+"\n")
                myfile.write(linksolver("http://www.livinstream.org/live/?channel="+str(i))+"\n")
        
        else:
            print('Web site does not exist') 
except:
    print('FEHLER')
    
def ecanlisolver( url ): 
    #url = "https://www.ecanlitvizle.net/show-tv-izle/"
    proc = subprocess.Popen(["streamlink --stream-url "+url+" best"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    out = out.decode("utf-8") 
    return out 

def ecanliget(url):
    url = "https://www.ecanlitvizle.net"
    link=[]
    name=[]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive',}
    req = requests.get(url, headers=headers)
    test = req.text
    lhs, newrhs = test.split('class="kanallar"',1)
    newrhs.count('<img src=')-1
    bis = newrhs.count('<img src=')-2
        
    for i in range(1, bis):
        print(str(i))
        newlhs , newrhs = newrhs.split('<a href="https://www.ecanlitvizle.net/',1)
        linkget , newrhs = newrhs.split('" title="',1)
        linkget = "https://www.ecanlitvizle.net/" + linkget
        print("From " + str(linkget))
        if linkget == "https://www.ecanlitvizle.net/cnn-turk-izle/":
            linkget = "https://www.youtube.com/watch?v=pB64y-jJFB4"
        if linkget == "https://www.ecanlitvizle.net/ntv-spor-hd-izle/":
            linkget = "https://www.youtube.com/watch?v=cTAeSSbupqY"
        if linkget == "https://www.ecanlitvizle.net/a-haber-izle/":
            linkget = "https://www.ahaber.com.tr/webtv/canli-yayin"
        nameget , nnewrhs = newrhs.split('">',1)
        print(nameget)
        link.append(linkget) 
        name.append(nameget)
        print("#EXTINF:0,"+str(nameget))
        test19 = ecanlisolver(linkget)
        with open("livebak.m3u8", "a") as myfile:
                    myfile.write("#EXTINF:0,"+str(nameget)+" \n")
                    #myfile.write("h"+test19+" \n")
                    myfile.write(test19)
        print(test19)

def tatasolver(url):
#    url = "https://www.tata.to/channel/13thstreet"
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive',}
    req = requests.get(url, headers=headers)
    test = req.text
    left , right = test.split('data-src="',1)
    link ,waste = right.split('"',1)
    req = requests.get(link, headers=headers)
    test = req.text
    m3ulink = link.replace("embed.html", "index.m3u8")
    req = requests.get(m3ulink, headers=headers)
    print(m3ulink)
    return m3ulink



def tataget(url):
#    url = "https://www.tata.to/channels"
    link=[]
    name=[]
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Connection':'keep-alive',}
    req = requests.get(url, headers=headers)
    newrhs = req.text
    bis = newrhs.count('https://www.tata.to/channel/') -13
    
    for i in range(1, bis+1):
        print(str(i))
        newlhs , newrhs = newrhs.split('https://www.tata.to/channel/',1)
        linkget , newrhs = newrhs.split('" class="',1)
        nameget = linkget
        linkget = "https://www.tata.to/channel/" + linkget
        print(linkget)
        #nameget , nnewrhs = newrhs.split('">',1)
        print(str(nameget.encode('utf8')))
        print(tatasolver(str(linkget)))
        link.append(linkget)
        name.append(nameget)
        with open("livebak.m3u8", "a") as myfile:
                    myfile.write("#EXTINF:0,"+str(nameget.encode('utf8'))+" \n")
                    myfile.write(tatasolver(str(linkget))+" \n")
                    
ecanliget("https://www.ecanlitvizle.net")
#tataget("https://www.tata.to/channels")
