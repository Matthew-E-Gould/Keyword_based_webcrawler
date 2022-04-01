from bs4 import BeautifulSoup
import requests
import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)

# const
donePhrase = "-noMoreKeys"

# init
baseSite = ""
keywords = []
urlsToAccess = []
accessedUrls = []
externalUrls = []
keywordUrls = []
allowPreWildcards = False
allowPostWildcards = False
allowExplorationOfExternalLinks = False
externalSearchDepth = 0
keywordCount = 0

# get site to start from
print("Enter base url you'd like to trawl:")
baseSite = input()
urlsToAccess.append(baseSite)
print("Enter keyword " + str(keywordCount+1) + " that you'd like to search for :")
keywords.append(input())
keywordCount += 1
inp = ""

# getting keywords to look for
while(inp != donePhrase):
    print("Enter keyword " + str(keywordCount+1) + " that you'd like to search for (type '"+ donePhrase +"' when you've entered them all):")
    inp = input()
    keywordCount += 1

# wildcard choice stuff here (TBI)

for url in urlsToAccess:
    print('reading '+url)
    req = requests.get(url)

    # check for keyword
    for keyword in keywords:
        if keyword in str(req.content):
            keywordUrls.append(url)
            print('Found Keyword!')

    # check for further links
    soup = BeautifulSoup(req.content, features="html.parser")
    tags = soup.find_all('a', href=True)
    for tag in tags:
        href = tag['href']

        # filter out things (pre full URL)
        if len(href) > 0:
            notTag = href[0] != '#'
            notTel = False
            if len(href) >= 4 and href[:4] != 'tel:':
                notTel = True
            elif len(href) < 4:
                notTel = True
            notMailTo = False
            if len(href) >= 7 and href[:7] != 'mailto:':
                notMailTo = True
            elif len(href) < 7:
                notMailTo = True
            # check href is URL and not URI
            hrefURL = href
            if href[0] == '/':
                hrefURL = url + href

            uniqueLink = hrefURL not in urlsToAccess and hrefURL not in accessedUrls
            # implement filters
            if notTag and notTel and notMailTo and uniqueLink:
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
    writeToJSONFile('./', 'data', data)

print('done!')