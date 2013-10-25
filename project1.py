#!/usr/bin/python3

import math,sys

######## CONSTANTS ########
D = 0.85    #damping

######## Data structure ########
# a Page is a class 
class Page:
    def __init__(self,name,inlink):
        self.inlink = inlink    # a list of PageName as String
        self.name = name        # PageName
        self.pr = 0             # Current PageRank
        self.newPR = 0          # New PageRank
        self.inPage = set()     # a set of Page that link to this
        self.outPage = set()    # a set of Page that this link to
    
######## FUNCTION ########
# PageRank 
# input: a dictionary of (PageName, Page) as PM
#        number of Pages as N
# effect: calculate the PageRank
def pageRank(PM,N):
    P = PM.values()     # a list of Page
    S = get_sinks(P)    # a set of sink Page
    Perp = []
    for p in P:
        p.pr = 1/N
    count = 0
    q1 = open('q1','w') #result file for question 1
    while(True):
        if count == 1 or count == 10 or count == 100:
            q1.write(str(count)+'\'s iteration\n')
            for item in CurrentPM(PM):
                q1.write("{} \n".format(item))
            q1.write("------------------------\n")
            
        #calculate perplexity
        H = 0
        for p in P:
            H += (p.pr*math.log(p.pr, 2))
        perp = 2**(-H)
        Perp.append(perp)
        # end of calculate perplexity
        
        sinkPR = 0
        for p in S:
            sinkPR += p.pr
        for p in P:
            p.newPR = (1-D)/N
            p.newPR += D*sinkPR/N
            for q in M(p):
                p.newPR += D*q.pr/L(q)
                
        #if ((isConverged(P) or checkPerp(Perp)) and count>100): 
        if(isConverged(P) or checkPerp(Perp)):
            print('ending PageRank, write Perplexity of each roundto file...')
            f = open('perplexity','w')
            f.write('Iter\tPerplexity\n')
            i= 1
            for item in Perp:
                f.write(str(i)+'\t'+str(item)+'\n')
                i+=1
            break   
        for p in P:
            p.pr = p.newPR
        count += 1
    q1.close()

def get_sinks(P):
    result = set()
    mp = {}
    for p in P:
        mp[p.name] = False
    for p in P:
        inPages = p.inlink
        for q in inPages:
            mp[q] = True
    for page in P:
        if mp[page.name] == False:
            result.add(page)
    return result

def isConverged(P):
    for p in P:
        if (p.pr != p.newPR):
            return False;
    return True

def Update(PM):
    for p in PM.values():
        for name in p.inlink:
            p.inPage.add(PM[name])
            PM[name].outPage.add(p)

def M(p):
    return p.inPage
        
def L(p):
    return len(p.outPage)

def CurrentPM(PM):
    lstOfPage = sorted( PM.values(), key = lambda x:x.name )
    result = []
    for p in lstOfPage:
        result.append("Page {0}:    {1}".format(p.name,round(p.pr,6)))
    return result
        
def checkPerp(Perp):
    if(len(Perp) < 4):return False
    else:
        lastFour = list(map(lambda x:math.floor(x),Perp[len(Perp)-4:]))
        for perp in lastFour:
            if(perp!=lastFour[3]): return False
        return True
    
######## MAIN ########
def main():
    P=[]        # a list of Page
    PM = {}     # a map from Page name to Page object
    #read a file line by line, each line's first word is the page name following by its inlink pages
    print('process the input file...')
    #f = open("wt2g_inlinks.txt")
    try:
        if len(sys.argv) > 1:
            f = open(sys.argv[1])
        else: 
            f = open('wt2g_inlinks.txt') 
#             f = open('input')
    except IOError as e:
        print(e)

    for line in f:
        # create a Page object and store in list P
        if(len(line)>0):
            lst = line.split()
            page = Page(lst[0],lst[1:])
            #print(page.get_name(),page.get_inlink())
            P.append(page) 
            
    # create a page map (pagename to Page) as PM from P
    for p in P: 
        PM[p.name] = p
    # update the outPage and inPage field
    Update(PM)
    
    print('calculating PageRank for each page...')
    pageRank(PM, len(P))
    
    print('sorting the pages by PR')
    sortByPR = sorted(P, key=lambda x: x.pr, reverse=True)
    print('write the first 50 page by PR into file: First50byPR')
    f2=open('First50byPR','w')
    i=1
    for p in sortByPR[:50]:
        f2.write(str(i)+'\t'+p.name+'\t'+str(p.pr)+'\n')    
        i+=1
        
    print('sorting the pages by in-link count')
    sortByIL = sorted(P, key=lambda x: len(x.inPage), reverse=True)
    print('write the first 50 page by in-link count into file: First50byIL')
    f2=open('First50byIL','w')
    i=1
    for p in sortByIL[:50]:
        f2.write(str(i)+'\t'+p.name+'\t'+str(len(p.inPage))+'\n')
        i+=1
        
    print('done')
    f.close()
    f2.close()

    
if __name__ == "__main__": main()
