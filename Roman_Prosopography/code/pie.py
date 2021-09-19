# Imports
import csv
from bs4 import BeautifulSoup as bs
import os
import numpy as np
import matplotlib.pyplot as plt
content = []
csvList = []
combined_list = []
# fileList = ['appian.xml', 'eutropius.xml', 'periochae.xml', 'plutarch_cicero.xml', 'plutarch_gaiusgracchus.xml', 'plutarch_lucullus.xml', 'plutarch_marius.xml', 'plutarch_sertorius.xml', 'plutarch_sulla.xml', 'plutarch_tiberiusgracchus.xml', 'plutarch_pompey.xml', 'plutarch_caesar.xml', 'plutarch_crassus.xml', 'plutarch_cato.xml', 'plutarch_brutus.xml', 'plutarch_antony.xml', 'nepos_atticus.xml', 'sallust_catiline.xml']
# person_exceptions = [140, 1122, 1123, 1124, 1125, 10, 225, 151, 409, 901, 510, 924, 849, 513, 415, 673, 742, 779, 767, 768, 276, 128, 962, 963, 964, 686, 985, 552, 1002, 1032, 23, 296, 1044, 1045, 1046, 1047, 1048, 743, 698, 1108, 674]

person_exceptions = []
# for filename in os.listdir("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\data\\individual"):
#     fileList.append(filename)

fileList = ['plutarch_cicero.xml']

# Functions
def CountFrequency(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

def Convert(tup, di):
    di = dict(tup)
    return di

# Code 1: Extract names and frequencies
with open("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\resources\\character_list.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count +=1
        csvList.append(row)

documents = []
for file in fileList:
    with open("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\data\\individual\\"+file, "r") as file:
        content = file.readlines()
        content = "".join(content)
        documents.append(bs(content, "lxml"))

nameList = bs("")
for document in documents:
    results = document.find_all("persname")
    for result in results:
        nameList.append(result)

for i in range(len(csvList)):
    x = nameList.find_all("persname", {"n": i+1})
    number_of_occurences = len(x)
    if number_of_occurences > 0:
        combined_list.append((csvList[i][0], number_of_occurences, i+1))
    # if number_of_occurences == 0:
    #     print(csvList[i][0], csvList[i][1])

combined_list = sorted(combined_list, key=lambda x: x[1], reverse=True)[0:4]

pretty_list = []
for item in combined_list:
    if item[2] not in person_exceptions:
        pretty_list.append((item[0], round(100*(item[1] / len(nameList)), 2)))

labels = []
for item in pretty_list:
    labels.append(item[0])

sizes = []
for item in pretty_list:
    sizes.append(item[1])

x = 0
for size in sizes:
    x = x + size

labels.append("Others")
sizes.append(round(100-x, 2))

labels = tuple(labels)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Mention Frequency: Life of Antony")
plt.show()
