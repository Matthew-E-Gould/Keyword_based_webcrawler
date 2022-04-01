from bs4 import BeautifulSoup
import requests
import json

baseUrl = 'https://web.whatsapp.com/desktop/mac/files/WhatsApp.dmg'

#r = requests.get(baseUrl)
#print(r.status_code)
#print(r.content)

file = 'test.exe'
if file[-4:] == '.exe':
    print('exe detected')





