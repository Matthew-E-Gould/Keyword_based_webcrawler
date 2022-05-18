from bs4 import BeautifulSoup
import requests
import json

def readFromJSONFile(path, filename):
    filePathNameWExt = './' + path + '/' + filename + '.json'
    # encoding="utf-8" fixes an issue with accents on characters ... I think
    with open(filePathNameWExt, 'r', encoding="utf-8") as fp:
        loadedJson = json.load(fp)
        return loadedJson


fileContent = readFromJSONFile('outputs', '1651174083 - data')


