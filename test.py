from bs4 import BeautifulSoup
import requests
import json

print('RUNNING TEST.PY <<<<<<<<<<<<<<')

# def readFromJSONFile(path, filename):
#     filePathNameWExt = './' + path + '/' + filename + '.json'
#     # encoding="utf-8" fixes an issue with accents on characters ... I think
#     with open(filePathNameWExt, 'r', encoding="utf-8") as fp:
#         loadedJson = json.load(fp)
#         return loadedJson
#
#
# fileContent = readFromJSONFile('outputs', '1651174083 - data')

# testString = 'werpyderpy'
# print(testString.split('#'))

stringly = 'abcdabcd'
strList = ['a','b','c','d','a','b','c','d']
print(strList.index('b'))
print(strList.index('e'))

print(len( stringly.split('e') ))