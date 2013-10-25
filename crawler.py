import urlparse
import urllib2
import time
import httplib
import robotparser
import StringIO
from bs4 import BeautifulSoup

# Constant
start_seed = "http://www.ccs.neu.edu/"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers = {'User-Agent':user_agent,}
domain = "www.ccs.neu.edu"
robotUrl = "http://www.ccs.neu.edu/robots.txt"
#


# Function definition
def extend(link):
    result = []
    try:
        request = urllib2.Request(link,None,headers)
        response = urllib2.urlopen(request)
        data = response.read()
        soup = BeautifulSoup(data)
        for tag in soup.findAll('a',href = True):
            tag['href'] = urlparse.urljoin(start_seed,tag['href'])
            if start_seed in tag['href']:
                result.append(tag['href'])
    except:
        print "error: ", link
    return result

def getType(head):
    for e in head:
        if (e[0] == 'content-type'):
            return e[1]

def isHtml(lnk):
    try:
        conn = httplib.HTTPConnection(domain)
        linkObject = urlparse.urlparse(lnk)
        conn.request("HEAD",linkObject.path)
        res = conn.getresponse()
        head = res.getheaders()
        fileType =  getType(head)
    
        if 'text/html' in fileType:
            return True
        else:
            return False
    except:
        return False

def isPDF(lnk):
    try:
        conn = httplib.HTTPConnection(domain)
        linkObject = urlparse.urlparse(lnk)
        conn.request("HEAD",linkObject.path)
        res = conn.getresponse()
        head = res.getheaders()
        fileType =  getType(head)
        
        if 'application/pdf' in fileType:
            return True
        else:
            return False
    except:
        return False

def parseRobot(url):
    request = urllib2.Request(url,None,headers)
    response = urllib2.urlopen(request)
    data = response.read()
    buf = StringIO.StringIO(data)
    result = []

    for line in buf.readlines():
        array = line.split()
        if len(array)!=0 and "Disallow:" in array[0]:
            result.append(array[1])
    return result

# return true if the url is allowed to crawl
def isAllowed(url, restrict):
    for elem in restrict:
        if elem in url:
            return False
        else:
            return True

def print_PDF(visited):
    no = 0
    for l in visited:
        no = no + 1
        if ".pdf" in l:
            print no, l

# End of Fun def


# Main
def main():
    restrict = parseRobot(robotUrl)
    urls = [start_seed]
    visited = [start_seed]
    pdf = []
    c = 0  # visit order
    while (len(urls) > 0) and c<100:
        link = urls.pop(0)
        if not isAllowed(link, restrict):
            continue
        c = c+1
        print c, link
        time.sleep(5) # delays for 5 seconds
        if isHtml(link):
            extend_links = extend(link)
            for lnk in extend_links:
                if lnk not in visited:
                    urls.append(lnk)
                    visited.append(lnk)
        elif isPDF(link):
            pdf.append(link)
    #print_PDF(visited)

main()


