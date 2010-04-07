import urllib2
import os
import datetime
import string
import re
import unittest
import sys
import eyeD3

VOA_URL=r'http://www.unsv.com/'

def getFileNameFromLink(strLink):
    filename_re=r'[^/:]+.(mp3|pdf|lrc)'
    matched=re.search(filename_re, strLink)
    if matched:
        return matched.group(0)
    else:
        return r''

def genMp3DownLinkRe(date, filetype=r'mp3'):
    return r'http[^"]*'+date+r'[^"]*\.'+filetype

def genDateStr(rawStr):
    return string.replace(rawStr, r'-', r'')

def getLinks(str_today):
    mp3Re=genMp3DownLinkRe(str_today) #mp3 link re
    pdfRe=genMp3DownLinkRe(str_today, r'pdf')
    #lrcRe=genMp3DownLinkRe(str_today, r'lrc')
    print r'Reading VOA page...',
    response=urllib2.urlopen(VOA_URL)
    html=response.read()
    print r'Done.'
    print r'Trying to parse the page and get the right mp3/pdf links...',
    matchedMp3Links=re.findall(mp3Re, html)
    matchedPdfLinks=re.findall(pdfRe, html)
    #matchedLrcLinks=re.findall(lrcRe, html)
    print r'Done.'
    return matchedMp3Links,matchedPdfLinks

def genM3uFile(today, mp3files):
    print r'Generate M3U file...',
    m3ufileName=os.path.join(today, r'playlist.m3u')
    m3ufile=file(m3ufileName,'wb')
    for aMp3file in mp3files:
        m3ufile.write('.\%s\n'%aMp3file)
    m3ufile.close()
    print r'Done.'

def updateMp3FileTag(fileName, albumName):
    tag=eyeD3.Tag()
    if not tag.link(fileName):
        tag.header.setVersion(eyeD3.ID3_V2_3)

    tag.setArtist(r'VOANews.com')
    tag.setTitle(os.path.basename(fileName))
    tag.setAlbum(albumName)
    tag.update()

def genDefaultAlbumName(today):
    return r'VOA_SE_%s'%today

class ADVTest(unittest.TestCase):
    def test_genDateStr(self):
        self.assertEqual(r'20100313', genDateStr(r'2010-03-13'))
        self.assertEqual(r'20000923', genDateStr(r'2000-09-23'))
    def test_genLinkReMatch(self):
        re1=genMp3DownLinkRe(r'20100313')
        self.assertTrue(re.match(re1, r'http://lsdlfjsldfj/20100313kdsf.mp3'))
        self.assertTrue(re.match(re1, r'http://lsdlfklahsflhiwyroiyd...kshdf////dfj/asdfasdfasdf20100313kdasdfasdfsf.mp3"'))
        self.assertFalse(re.match(re1, r'asdfasdfhttp://lsdlfjsldfj/20100313kdsf.mp4'))
        self.assertFalse(re.match(re1, r'http:asdfasdfasdf//lsdlfjsldfj/20100313kdsf.mp5'))
        self.assertFalse(re.match(re1, r'http:asdfasdfasdf//lsdlfjsldfj/20100313kdsf.pd1'))
    def test_genLinkReSearch(self):
        re1=genMp3DownLinkRe(r'20100313')
        self.assertTrue(re.search(re1, r'jfl;sajf;lsajdf;ljwherljhlkjsdklsjdfkllhtt;s;ljf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;jfl;asjdfl;sajfdl;jsfljslf;j'))
        self.assertTrue(re.search(re1, r'l;jas;ljnnxknvlkaslhflaewuyr99375973498iuhhsldf"http://lsdlfjsldfj/20100313kdsf.mp3"las;dlfjasldjfl;sjfl;jsdlf;jsa;ljf;alf'))
        self.assertTrue(re.search(re1, r'jfl;slaljl;dfja;sldjfsf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;flajl;js;fdjas;ldjflsjfdlj'))
    def test_genLinkReSearch_ObjectCheck(self):
        re1=genMp3DownLinkRe(r'20100313')
        match=re.search(re1, r'jfl;sajf;lsajdf;ljwherljhlkjsdklsjdfkllhtt;s;ljf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;jfl;asjdfl;sajfdl;jsfljslf;j')
        self.assertEqual(match.group(0), r'http://lsdlfjsldfj/20100313kdsf.mp3')
        matchedLink=re.findall(re1, r'jfl;sajf;lsajdf;ljwherl"httplkljlsf20100313lslfjsfd.mp3"jhlkjsdklsjdfkllhtt;s;ljf"http://lsdlfjsldfj/20100313kdsf.mp3"asl;jfl;asjdfl;sajfdl;jsfljslf;j')
        self.assertEqual(len(matchedLink), 2)
        self.assertEqual(matchedLink[0], r'httplkljlsf20100313lslfjsfd.mp3')
        self.assertEqual(matchedLink[1], r'http://lsdlfjsldfj/20100313kdsf.mp3')
    def test_openLink(self):
        re1=genMp3DownLinkRe(genDateStr(str(datetime.date.today())))
        matchedLink=getLinks(re1)
        self.assertTrue(len(matchedLink)!=0)
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

    home_dir=os.path.expanduser('~')

    if not os.path.isdir(home_dir):
        print "Can't find the home directory. :("
        sys.exit(1)

    os.chdir(home_dir)

    if not os.path.isdir('VOA'):
        print r"Can't find the VOA directory, create one...",
        os.mkdir('VOA')
        print r'Done.'

    os.chdir('VOA')

    if not os.path.isdir(str_today):
        print r"Can't find the date directory, create one...",
        os.mkdir(str_today)
        print r'Done'

    [mp3Links, pdfLinks]=getLinks(str_today)

    linkSet=set()
    for link in mp3Links:
        linkSet.add(link)

    for link in pdfLinks:
        linkSet.add(link)

    print r'Found %d link, begin to download them...'%len(linkSet)

    mp3fileNames=[]
    for link in linkSet:
        print r'Handling link %s...'%link
        filename=getFileNameFromLink(link)

        if filename[-3:]=='mp3':
            mp3fileNames.append(filename)

        if not filename==r'':
            wholename=os.path.join(str_today, filename)

            if os.path.isfile(wholename):
                print '\tThe file has been downloaded. Skip this file.'
            else:
                print '\tDownloading the %s file...'%wholename[-3:],
                data=urllib2.urlopen(link).read()
                print 'Done'
                print '\tWriting data info file...',
                f=file(wholename, 'wb')
                f.write(data)
                print 'Done'
                f.close()

            if filename[-3:]=='mp3':
                print '\tModify MP3 tags...',
                updateMp3FileTag(os.path.join(os.path.abspath(os.path.join(home_dir, 'VOA')), wholename), genDefaultAlbumName(str(datetime.date.today())))
                print 'Done'



    genM3uFile(str_today, mp3fileNames)

    print 'All Finished. ^_^'

    # open that directory
    os.system(r'explorer %s'%os.path.abspath(os.path.abspath(os.path.join(home_dir, 'VOA', str_today))))
