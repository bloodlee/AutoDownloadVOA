import urllib2
import os
import datetime
import string
import re
import unittest

VOA_URL=r'http://www.unsv.com/'

def getFileNameFromLink(strLink):
    filename_re=r'[^/:]+.mp3'
    matched=re.search(filename_re, strLink)
    if matched:
        return matched.group(0)
    else:
        return r''

def genMp3DownLinkRe(date):
    return r'http[^"]*'+date+r'[^"]*\.mp3'

def genDateStr(rawStr):
    return string.replace(rawStr, r'-', r'')

def getMp3Links(aRe):
    print r'Reading VOA page...',
    response=urllib2.urlopen(VOA_URL)
    html=response.read()
    print r'Done.'
    print r'Trying to parse the page and get the right mp3 links...',
    matchedLinks=re.findall(aRe, html)
    print r'Done.'
    return matchedLinks

class ADVTest(unittest.TestCase):
    def test_genDateStr(self):
        self.assertEqual(r'20100313', genDateStr(r'2010-03-13'))
        self.assertEqual(r'20000923', genDateStr(r'2000-09-23'))
    def test_genLinkReMatch(self):
        re1=genMp3DownLinkRe(r'20100313')
        self.assertTrue(re.match(re1, r'"http://lsdlfjsldfj/20100313kdsf.mp3"'))
        self.assertTrue(re.match(re1, r'"http://lsdlfklahsflhiwyroiyd...kshdf////dfj/asdfasdfasdf20100313kdasdfasdfsf.mp3"'))
        self.assertFalse(re.match(re1, r'asdfasdf"http://lsdlfjsldfj/20100313kdsf.mp4"'))
        self.assertFalse(re.match(re1, r'"http:asdfasdfasdf//lsdlfjsldfj/20100313kdsf.mp5"'))
    def test_genLinkReSearch(self):
        re1=genMp3DownLinkRe(r'20100313')
        self.assertTrue(re.search(re1, r'jfl;sajf;lsajdf;ljwherljhlkjsdklsjdfkllhtt;s;ljf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;jfl;asjdfl;sajfdl;jsfljslf;j'))
        self.assertTrue(re.search(re1, r'l;jas;ljnnxknvlkaslhflaewuyr99375973498iuhhsldf"http://lsdlfjsldfj/20100313kdsf.mp3"las;dlfjasldjfl;sjfl;jsdlf;jsa;ljf;alf'))
        self.assertTrue(re.search(re1, r'jfl;slaljl;dfja;sldjfsf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;flajl;js;fdjas;ldjflsjfdlj'))
    def test_genLinkReSearch_ObjectCheck(self):
        re1=genMp3DownLinkRe(r'20100313')
        match=re.search(re1, r'jfl;sajf;lsajdf;ljwherljhlkjsdklsjdfkllhtt;s;ljf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;jfl;asjdfl;sajfdl;jsfljslf;j')
        self.assertEqual(match.group(0), r'"http://lsdlfjsldfj/20100313kdsf.mp3"')
        matchedLink=re.findall(re1, r'jfl;sajf;lsajdf;ljwherl"httplkljlsf20100313lslfjsfd.mp3"jhlkjsdklsjdfkllhtt;s;ljf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;jfl;asjdfl;sajfdl;jsfljslf;j')
        self.assertEqual(len(matchedLink), 2)
        self.assertEqual(matchedLink[0], r'"httplkljlsf20100313lslfjsfd.mp3"')
        self.assertEqual(matchedLink[1], r'"http://lsdlfjsldfj/20100313kdsf.mp3"')
    def test_openLink(self):
        re1=genMp3DownLinkRe(genDateStr(str(datetime.date.today())))
        matchedLink=getMp3Links(re1)
        self.assertTrue(len(matchedLink)>=3)
    def test_parseOutFileName(self):
        link=r'"http://fjalsdjflsjdf;l/;asjflasjdf;ljasd/file.mp3'
        fileName=getFileNameFromLink(link)
        self.assertEqual(fileName, r'file.mp3')
        
        link=r'"http://fjalsdjflsjdf;l/;asjflasjdf;ljasd/fkasdfajslfja;sj;asflhalfhasd/aljsdile/.mp3'
        fileName=getFileNameFromLink(link)
        self.assertEqual(fileName, r'')
        
        link=r'"http://fjalsdjflsjdf;l/;asjflasjdf;ljasd/fkasdfajslfja;sj;asflhalfhasd/aljsdile/8168.mp3'
        fileName=getFileNameFromLink(link)
        self.assertEqual(fileName, r'8168.mp3')
        
if __name__ == '__main__':
    #Get today's data string
    str_today=genDateStr(str(datetime.date.today()))
    
    if not os.path.isdir(str_today):
        print r"Can't find the date directory, create one...",
        os.mkdir(str_today)
        print r'Done'
    
    link_re=genMp3DownLinkRe(str_today)
    mp3Links=getMp3Links(link_re)
    
    mp3LinksSet=set()
    for link in mp3Links:
        mp3LinksSet.add(link)
    
    print r'Found %d link, begin to download them...'%len(mp3LinksSet)
    
    for link in mp3LinksSet:
        print r'Handling link %s...'%link
        filename=getFileNameFromLink(link)
        if not filename==r'':            
            wholename=os.path.join(str_today, filename)
            
            if os.path.isfile(wholename):
                print '\tThe file has been downloaded. Skip this file.'
                continue
            
            print '\tDownloading the mp3 file...',
            data=urllib2.urlopen(link).read()
            print 'Done'
            print '\tWriting data info file...',
            f=file(wholename, 'wb')
            f.write(data)
            print 'Done'
            f.close()
    
    print 'All Finished. ^_^'
    
    # open that directory
    os.system(r'explorer %s'%os.path.abspath(str_today))
