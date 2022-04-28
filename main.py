from bs4 import BeautifulSoup
import requests
import json
import time


def writeToJSONFile(path, filename, filedata):
    filePathNameWExt = './' + path + '/' + filename + '.json'
    with open(filePathNameWExt, 'w', encoding="utf-8") as fp:  # encoding="utf-8" fixes an issue with accents on characters ... I think
        json.dump(filedata, fp, ensure_ascii=False)


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

# get site to start from
print("Enter base url you'd like to trawl:")
baseSite = input()
urlsToAccess.append(baseSite)
print("Enter keyword " + str(len(keywords)) + " that you'd like to search for :")
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

# ignore URL params (removes anything after first '?')
removeUrlParams = False
print("Do you want to ignore URL params? (anything after a '?' in the URL) [Y/y/N/n]")
quesResponse = input().lower()
if quesResponse == 'y':
    removeUrlParams = True

# cleanup of response content to be visible content only
onlyVisibleContent = False
print("Do you want to only check keywords against visible content? (will run slower) [Y/y/N/n]")
quesResponse = input().lower()
if quesResponse == 'y':
    onlyVisibleContent = True

# wildcard choice stuff here (TBI)

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

                # filter out things (pre full URL)
                if len(href) > 4:

                    isUri = href[0] == '/' or href[0] == '.'
                    isWWW = href[:3] == 'www'
                    isHTTP = href[:4] == 'http'

                    # check href is URL and not URI
                    hrefURL = href
                    if href[0] == '/' or href[0] == '.':
                        if url[-1] == '/' and href[0] == '/':
                            hrefURL = url[:-1] + href  # stop // from being in fixed urls
                        elif url[-1] != '/' and href[0] != '/':
                            hrefURL = url + '/' + href  # stops URIs not having an appropriate /
                        else:
                            hrefURL = url + href

                    if removeUrlParams:
                        tempHrefURL = hrefURL
                        hrefURL = tempHrefURL.split('?')[0]

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
            }

            # save array to file
            writeToJSONFile('outputs', filename, data)

        except:
            print('exception occurred')

        print(len(urlsToAccess))

print('done!')

