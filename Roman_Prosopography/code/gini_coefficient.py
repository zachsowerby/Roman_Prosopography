# Imports
import csv
from bs4 import BeautifulSoup as bs
import os
content = []
csvList = []
combined_list = []
fileList = ['appian.xml', 'eutropius.xml', 'periochae.xml', 'plutarch_cicero.xml', 'plutarch_gaiusgracchus.xml', 'plutarch_lucullus.xml', 'plutarch_marius.xml', 'plutarch_sertorius.xml', 'plutarch_sulla.xml', 'plutarch_tiberiusgracchus.xml', 'plutarch_pompey.xml', 'plutarch_caesar.xml', 'plutarch_crassus.xml', 'plutarch_cato.xml', 'plutarch_brutus.xml', 'plutarch_antony.xml', 'nepos_atticus.xml', 'sallust_catiline.xml']
person_exceptions = [140, 1122, 1123, 1124, 1125, 10, 225, 151, 409, 901, 510, 924, 849, 513, 415, 673, 742, 779, 767, 768, 276, 128, 962, 963, 964, 686, 985, 552, 1002, 1032, 23, 296, 1044, 1045, 1046, 1047, 1048, 743, 698, 1108, 674]

# for filename in os.listdir("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\data\\individual"):
#     fileList.append(filename)

# person_exceptions = []
# fileList = ['nepos_atticus.xml']

# Functions
def CountFrequency(my_list):
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1
    return dict(sorted(freq.items(), key=lambda item: item[1], reverse=True))

# Variables
l = 0 # frequency cutoff

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

new_list = sorted(combined_list, key=lambda x: x[1], reverse=True)

final_list = []
for item in new_list:
    if item[1] >= l and item[2] not in person_exceptions:
        final_list.append(item[2])

A = (len(final_list) * new_list[0][1]) / 2

B = 0
for x in range(0,len(final_list)):
    y = ((i + 1)*(new_list[0][1])) / len(final_list)
    Y = new_list[x][1]
    B = B + (y-Y)

G = A/B
G = G*100
G
