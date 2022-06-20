from bs4 import BeautifulSoup
import requests
import json
import time
import sys


# to do list:
# 1: resolve issues around urls appending data when it's going back a couple of links before (../../../urlstuffhere)
# 2: remove stuff after '#' if they want to remove stuff after '?'
# 3: make other option to set baseURL to query against
# 4: make O-O
# 5: make UI
# 6: make clear way to view links with what keywords

def writeToJSONFile(path, filename, filedata):
    filePathNameWExt = './' + path + '/' + filename + '.json'
    # encoding="utf-8" fixes an issue with accents on characters ... I think
    with open(filePathNameWExt, 'w', encoding="utf-8") as fp:
        json.dump(filedata, fp, ensure_ascii=False)


def readFromJSONFile(path, filename):
    filePathNameWExt = './' + path + '/' + filename + '.json'
    # encoding="utf-8" fixes an issue with accents on characters ... I think
    with open(filePathNameWExt, 'r', encoding="utf-8") as fp:
        loadedJson = json.load(fp)
        return loadedJson

# const
donePhrase = ""

# init
baseSite = ""
keywords = []
urlsToAccess = []
accessedUrls = []
externalUrls = []
keywordUrls = []
blockList = []
allowPreWildcards = False
allowPostWildcards = False
allowExplorationOfExternalLinks = False
externalSearchDepth = 0
filename = str(int(time.time())) + " - data"

# ask user if they want to load last session
freshScrape = True
fileToLoad = ''
jsonContent = {}
print("Do you want to load a file? (From outputs folder) [Y/y/N/n]")
quesResponse = input().lower()
if quesResponse == 'y':
    freshScrape = False
    print("Enter the filename you want to load, without the '.json' (CaSe SeNsAtIvE):")
    fileToLoad = input()
    try:
        jsonContent = readFromJSONFile('outputs', fileToLoad)
    except:
        print('Error loading file, resuming as a fresh scrape.')
        freshScrape = True

    if not freshScrape:

        baseSite = jsonContent['baseSite']
        keywords = jsonContent['keywords']
        urlsToAccess = jsonContent['urlsToAccess']
        accessedUrls = jsonContent['accessedUrls']
        externalUrls = jsonContent['externalUrls']
        keywordUrls = jsonContent['keywordUrls']

        searchOtherSites = jsonContent['settings']['searchOtherSites']
        removeUrlParams = jsonContent['settings']['removeUrlParams']
        onlyVisibleContent = jsonContent['settings']['onlyVisibleContent']


if freshScrape:
    # get site to start from
    print("Enter base url you'd like to trawl:")
    baseSite = input()
    urlsToAccess.append(baseSite)
    print("Enter keyword " + str(len(keywords)) + " that you'd like to search for:")
    inp = input().lower()
    keywords.append(inp)

    # getting keywords to look for
    while(inp != donePhrase):
        print("Enter keyword " + str(len(keywords)) + " that you'd like to search for (type '" + donePhrase + "' when you've entered them all):")
        inp = input().lower()
        if inp != donePhrase and inp not in keywords:
            keywords.append(inp)

    # stay on same site
    askQuestion = False
    searchOtherSites = True
    baseUrl = ''
    baseSiteArr = baseSite.split('/')
    if 'http' in baseSiteArr[0] and ':' in baseSiteArr[0] and len(baseSiteArr) > 3:
        if '.' in baseSiteArr[2]:
            baseUrl = baseSiteArr[0] + '//' + baseSiteArr[2]
            askQuestion = True
    elif '.' in baseSiteArr[0]:
        baseUrl = baseSiteArr[0]
        askQuestion = True

    if askQuestion:
        print("Do you want to stay on the same site? (" + baseUrl + ") [Y/y/N/n]")
        quesResponse = input().lower()
        if quesResponse == 'y':
            searchOtherSites = False
            # wildcard choice stuff here [TBI]

    # ignore URL params (removes anything after first '?' or '#')
    removeUrlParams = False
    print("Do you want to ignore URL params? (anything after a '?' or '#' in the URL) [Y/y/N/n]")
    quesResponse = input().lower()
    if quesResponse == 'y':
        removeUrlParams = True

    # cleanup of response content to be visible content only
    onlyVisibleContent = False
    print("Do you want to only check keywords against visible content? (will run slower) [Y/y/N/n]")
    quesResponse = input().lower()
    if quesResponse == 'y':
        onlyVisibleContent = True

# RUN
for url in urlsToAccess:

    if url[-4:] != '.exe':

        print('reading '+url)
        try:
            req = requests.get(url, timeout=5)
            soup = rawSoup = BeautifulSoup(req.content, features="html.parser")

            # query only visible content
            if onlyVisibleContent:
                soup = rawSoup.get_text()

            # check for keyword
            for keyword in keywords:
                if keyword in str(soup).lower():
                    keywordUrls.append(url)
                    print('Found Keyword!')

            # look for more links
            tags = rawSoup.find_all('a', href=True)
            for tag in tags:
                href = tag['href']
                # print('recognised href: ' + href)

                # filter out things (pre full URL)
                if len(href) > 4:

                    isUri = href[0] == '/' or href[0] == '.'
                    isWWW = href[:3] == 'www'
                    isHTTP = href[:4] == 'http'

                    # check href is URL and not URI
                    hrefURL = href
                    if href[0] == '/':
                        hrefURL = baseUrl + href
                    elif href[0] == '.' and url[-1] == '/':
                        hrefURL = url + href
                    elif href[0] == '.' and url[-1] != '/':
                        hrefURL = url + '/' + href

                    # sorting out extra '/..' to avoid visiting same urls
                    quickBreak = False  # dev
                    forceStop = False
                    splitUrl = hrefURL.split('/')
                    while '..' in splitUrl and not forceStop:
                        quickBreak = True  # dev
                        print(splitUrl)  # dev

                        backIndex = splitUrl.index('..')

                        if backIndex > 1:
                            splitUrl.pop(backIndex)
                            splitUrl.pop(backIndex-1)
                        else:
                            forceStop = True
                    hrefURL = '/'.join(splitUrl)
                    # print(hrefURL)

                    if quickBreak:  # dev
                        sys.exit('dev exit')  # dev



                    # removing stuff after # or ? if user wants it to
                    if removeUrlParams:
                        tempHrefURL = hrefURL
                        secondTempHrefURL = tempHrefURL.split('?')[0]
                        hrefURL = secondTempHrefURL.split('#')[0]

                    # check to see if we've accessed this URL before (should be last check)
                    uniqueLink = hrefURL not in urlsToAccess and hrefURL not in accessedUrls

                    # Check if we should store URL to be searched later
                    if uniqueLink and (isUri or isWWW or isHTTP) and (searchOtherSites or baseUrl in hrefURL):
                        print('found link: '+hrefURL)
                        urlsToAccess.append(hrefURL)

            urlsToAccess.remove(url)
            accessedUrls.append(url)

            data = {
                'baseSite': baseSite,
                'keywords': keywords,
                'urlsToAccess': urlsToAccess,
                'accessedUrls': accessedUrls,
                'externalUrls': externalUrls,
                'keywordUrls': keywordUrls,
                'settings': {
                    'searchOtherSites': searchOtherSites,
                    'removeUrlParams': removeUrlParams,
                    'onlyVisibleContent': onlyVisibleContent,
                }
            }

            # save array to file
            writeToJSONFile('outputs', filename, data)

        except:
            print('exception occurred')

        print(len(urlsToAccess))

print('done!')

