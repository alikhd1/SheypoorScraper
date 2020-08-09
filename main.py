# When i wroting this code god and i know how it woks. but now, only god knows how it works, so dont touch anything :)
# this was my code now its your problem.

from bs4 import BeautifulSoup
import random
import requests
import re
import wget


def urls():
    Url = []
    for number in range(1, 11):
        url = f'https://www.sheypoor.com/%D8%A7%DB%8C%D8%B1%D8%A7%D9%86/%D9%88%D8%B3%D8%A7%DB%8C%D9%84-%D9%86%D9%82%D9%84%DB%8C%D9%87/%D8%AE%D9%88%D8%AF%D8%B1%D9%88?f=1596902687.5000&p={number}'
        Url.append(url)
    return Url


def randomUserAgents():
    urls = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"]
    return random.choice(urls)


# send request and make a beautiful soup of html page
def souping(url):
    header = {'User-Agent': randomUserAgents()}
    response = requests.get(url, headers=header)
    rp = 'response code:, response.status_code'
    return BeautifulSoup(response.text, 'lxml')


# extract every ads links from page
def getlinks(url):
    source = souping(url)
    adUrls = []
    soup = source
    for arti in soup.findAll('article'):
        a = arti.find('a').attrs['href']
        adUrls.append(a)
    return adUrls


# collect page links and store them is list [[page1URL], [page2URL], [page3URL], ...] and send them to getlink func
def getMultiplePageLinks():
    print('getting links')
    links = []
    for url in urls():
        links.append(getlinks(url))
    return links


# extract every image links from page
def getImageLinks(url):
    soup = souping(url)
    imageUrls = []
    img = []
    for arti in soup.findAll("div", {"id": "item-images"}):
        img = arti
    if img != []:
        rex = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(img))
        for imagelink in rex:
            imageUrls.append(imagelink)
    return imageUrls


# collect list of image return their img links in list
def imgLinkCollector(adList):
    counter = 0
    linkToDownload = []
    for link in adList:
        # print('link', link)
        counter += 1
        linkToDownload.append(getImageLinks(link))
    return linkToDownload


def imageDownloader():
    print('download starting...')
    counter = 0
    pageNumber = 0
    for list in getMultiplePageLinks():
        pageNumber += 1
        links = imgLinkCollector(list)
        print('Start downloading page ', pageNumber)
        for imglist in links:
            lenoflist = len(imglist)
            for imglink in imglist:
                # print('poop', imglink, type(imglink))
                wget.download(imglink)
                counter += 1
                print(f'downloaded {counter} of {lenoflist} images')
            counter = 0
        print('done with page ', pageNumber)


imageDownloader()
print('job successfully done!')
