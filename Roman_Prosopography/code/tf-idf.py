# Imports
import csv
from bs4 import BeautifulSoup as bs
import os
import numpy as np
import matplotlib.pyplot as plt
import math
content = []
csvList = []
combined_list = []
fileList = []
person_exceptions = [140, 1122, 1123, 1124, 1125, 10, 225, 151, 409, 901, 510, 924, 849, 513, 415, 673, 742, 779, 767, 768, 276, 128, 962, 963, 964, 686, 985, 552, 1002, 1032, 23, 296, 1044, 1045, 1046, 1047, 1048, 743, 698, 1108, 674]


for filename in os.listdir("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\data\\individual"):
    fileList.append(filename)

analyzed_file = 'plutarch_cicero.xml'

# Functions
def CountFrequency(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

# Code 1: Extract names and frequencies
with open("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\resources\\character_list.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count +=1
        csvList.append(row)

with open("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\data\\individual\\"+analyzed_file, "r") as file:
    content = file.readlines()
    content = "".join(content)
    document = bs(content, "lxml")

nameList = bs("")
results = document.find_all("persname")
for result in results:
    nameList.append(result)

for i in range(len(csvList)):
    if i+1 not in person_exceptions:
        x = nameList.find_all("persname", {"n": i+1})
        number_of_occurences = len(x)
        if number_of_occurences > 0:
            combined_list.append((csvList[i][0], (number_of_occurences/len(nameList)), i+1))

combined_list = sorted(combined_list, key=lambda x: x[1], reverse=True)

documents = []
for file in fileList:
    with open("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\data\\individual\\"+file, "r") as file:
        content = file.readlines()
        content = "".join(content)
        documents.append(bs(content, "lxml"))

corpus_nameList = bs("")
for document in documents:
    results = document.find_all("persname")
    for result in results:
        corpus_nameList.append(result)

corpus_combined_list = []
for entity in combined_list:
    x = corpus_nameList.find_all("persname", {"n": entity[2]})
    number_of_occurences = len(x)
    corpus_combined_list.append((entity[0], (number_of_occurences/len(corpus_nameList)), entity[2]))

super_list = []
for triple in combined_list:
    for corpus_triple in corpus_combined_list:
        if triple[2] == corpus_triple[2]:
            super_list.append((triple[0], round((triple[1] * math.log(1/corpus_triple[1])), 2), triple[2]))

super_list = sorted(super_list, key=lambda x: x[1], reverse=True)[0:10]

super_list
