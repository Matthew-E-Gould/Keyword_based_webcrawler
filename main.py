from bs4 import BeautifulSoup
import requests
import json

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp, ensure_ascii=False)

# init
initialLinks = ['https://telephone-exchange.co.uk/sitemap.html','https://telephone-exchange.co.uk/sitemap2.html','https://telephone-exchange.co.uk/sitemap3.html','https://telephone-exchange.co.uk/sitemap4.html','https://telephone-exchange.co.uk/sitemap5.html','https://telephone-exchange.co.uk/sitemap6.html','https://telephone-exchange.co.uk/sitemap7.html','https://telephone-exchange.co.uk/sitemap8.html','https://telephone-exchange.co.uk/sitemap9.html','https://telephone-exchange.co.uk/sitemap10.html','https://telephone-exchange.co.uk/sitemap11.html']
preUrl = 'https://telephone-exchange.co.uk'
ADDRESS_ELEMENT_CONDITION = 'Located at'
problemLocationLinks = []
data = []

# time to scapre
for initialLink in initialLinks:
    print('reading '+initialLink) # output
    r = requests.get(initialLink)
    soup = BeautifulSoup(r.content, features="html.parser")
    lsbb = soup.find('div', class_="left_section_box_body")
    links = lsbb.find_all('a')
    for link in links:
        fullLocationLink = preUrl + link['href']
        print('-reading '+fullLocationLink)
        r = requests.get(fullLocationLink)
        soup = BeautifulSoup(r.content, features="html.parser")
        lsbbLocation = soup.find('div', class_="left_section_box_body")
        p_tags = soup.find_all('p')
        p_tags_iterator = -1
        for p_tag in p_tags:
            p_tags_iterator += 1
            content = p_tag.encode_contents()
            if(ADDRESS_ELEMENT_CONDITION in content):
                break

        if (p_tags_iterator > 0):
            name = soup.find('div', class_="left_section_box_top").encode_contents() # exchange name
            addr = p_tags[p_tags_iterator].encode_contents() # exchange address

            addrArrayPre = addr.split('<br/>')
            addrArrayPost = []
            first = True
            for addrPre in addrArrayPre:
                if first:
                    first = False
                else:
                    addrArrayPost.append(addrPre.replace("\n", "").replace(",", "").replace(".", ""))

            embedLinks = lsbbLocation.find_all('iframe')
            googleMapsEmbed = embedLinks[0]['src']
            bingMapsEmbed = embedLinks[1]['src']
            data.append({
                'url': fullLocationLink,
                'name': name,
                'address': addrArrayPost,
                'googleMaps': googleMapsEmbed,
                'bingMaps': bingMapsEmbed,
            })
        else:
            print('--issue with the page '+fullLocationLink)
            problemLocationLinks.append(fullLocationLink)

print("writing data to file...")
writeToJSONFile('./', 'data', data)
writeToJSONFile('./', 'fails', problemLocationLinks)
print("=========================================")
print("Program complete, Press enter to close :)")
raw_input()
