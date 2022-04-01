from bs4 import BeautifulSoup
import requests
import json


def writeToJSONFile(path, filename, filedata):
    filePathNameWExt = './' + path + '/' + filename + '.json'
    with open(filePathNameWExt, 'w') as fp:
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

# wildcard choice stuff here (TBI)

for url in urlsToAccess:

    if url[-4:] != '.exe':

        print('reading '+url)
        try:
            req = requests.get(url, timeout=5)

            # check for keyword
            for keyword in keywords:
                if keyword in str(req.content).lower():
                    keywordUrls.append(url)
                    print('Found Keyword!')

            # check for further links
            soup = BeautifulSoup(req.content, features="html.parser")
            tags = soup.find_all('a', href=True)
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
                            hrefURL = url[:-1] + href  # stop // from being added to urls
                        elif url[-1] != '/' and href[0] != '/':
                            hrefURL = url + '/' + href  # stops URIs not having an approprite /
                        else:
                            hrefURL = url + href

                    uniqueLink = hrefURL not in urlsToAccess and hrefURL not in accessedUrls
                    # implement filters
                    if uniqueLink and (isUri or isWWW or isHTTP):
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

        except:
            print('exception occurred')

        print(len(urlsToAccess))

print('done!')