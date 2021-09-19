# Imports
import csv
from bs4 import BeautifulSoup as bs
import os
content = []
csvList = []
combined_list = []

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
l = 11 # frequency cutoff
n = 15 # search size
k = 1 # final noise cleanup

# Code 1: Extract names and frequencies
with open("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\resources\\character_list.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        line_count +=1
        csvList.append(row)

with open("C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\data\\combined.xml", "r") as file:
    content = file.readlines()
    content = "".join(content)
    results = bs(content, "lxml")

for i in range(len(csvList)):
    x = results.find_all("persname", {"n": i+1})
    number_of_occurences = len(x)
    if number_of_occurences > 0:
        combined_list.append((csvList[i][0], number_of_occurences, i+1))

new_list = sorted(combined_list, key=lambda x: x[1], reverse=True)

pretty_list = []
final_list = []

for item in new_list:
    if item[1] >= l:
        pretty_list.append((str(new_list.index(item)+1) +".", item))
        final_list.append(item[2])

w = 100 / len(results.find_all("persname"))

for item in pretty_list:
    print(item[0] + "\t" + item[1][0] + "\t\t\t" + str(item[1][1]) + " (" + str(round(w*item[1][1],2)) + "%)")

# Code 2: Find proximal names. Only needs final_list and results
listy = []
splits = []
documents = results.find_all("document")
for child in documents[0].children:
    splits.append(child)

for identifier in final_list:
    id = str(identifier)
    proximal_names = []
    a = 0
    z = 0
    for split in splits:
        if isinstance(split, str):
            pass
        elif split.attrs["n"] == str(id):
            names_and_context_before = []
            tuples_before = []
            if splits.index(split,z) > (2*n):
                x = splits[splits.index(split,z)-(2*n):splits.index(split,z)]
            else:
                x = splits[:splits.index(split,z)]
            z = splits.index(split,z) + 1
            names_and_context_before.append(x)
            v = 0
            for item in names_and_context_before[0]:
                if isinstance(item, str):
                    pass
                else:
                    tuples_before.append((item, names_and_context_before[0][names_and_context_before[0].index(item,v)+1]))
                    v = names_and_context_before[0].index(item,v) + 1
            tuples_before.reverse()
            total_words_before = 0
            counter_before = 0
            for tuple in tuples_before:
                word_count = len(tuple[1].strip(".,!?:;0123456789").split()) + len(tuple[0])
                if n >= total_words_before + word_count:
                    total_words_before += word_count
                    counter_before += 1
                else:
                    break
            tuples_before2 = tuples_before[:counter_before]
            for item in tuples_before2:
                if item[0].attrs["n"] != id and int(item[0].attrs["n"]) in final_list:
                    proximal_names.append(item[0].attrs["n"])
            names_and_context_after = []
            tuples_after = []
            if len(splits) - splits.index(split,a) > 1+(2*n):
                y = splits[splits.index(split,a)+1:splits.index(split,a)+(2*n)+1]
            else:
                y = splits[splits.index(split,a):]
            a = splits.index(split,a) + 1
            names_and_context_after.append(y)
            b = 0
            for item in names_and_context_after[0]:
                if isinstance(item, str):
                    pass
                else:
                    tuples_after.append((item, names_and_context_after[0][names_and_context_after[0].index(item,b)-1]))
                    b = names_and_context_after[0].index(item,b) + 1
            total_words_after = 0
            counter_after = 0
            for tuple in tuples_after:
                word_count = len(tuple[1].strip(".,!?:;0123456789").split()) + len(tuple[0])
                if n >= total_words_after + word_count:
                    total_words_after += word_count
                    counter_after += 1
                else:
                    break
            tuples_after2 = tuples_after[:counter_after]
            for item in tuples_after2:
                if item[0].attrs["n"] != id and int(item[0].attrs["n"]) in final_list:
                    proximal_names.append(item[0].attrs["n"])
    listy.append((id, CountFrequency(proximal_names)))

# Code 3: transform data and write to file for networking_1. Only needs listy
data_for_csv1 = []
for item in listy:
    for relation in item[1]:
        data_for_csv1.append((str(item[0]) + "," + str(relation) + "," + str(item[1][relation])).split(","))

data_for_csv2 = []
for relation1 in data_for_csv1:
    for relation2 in data_for_csv1:
        if relation1[0] != relation2[1] and relation1[1] != relation2[0]:
            if relation2 not in data_for_csv2:
                data_for_csv2.append(relation2)

data_for_csv3 = []
for relation in data_for_csv2:
    if int(relation[2]) > k:
        data_for_csv3.append(relation)

for relation in data_for_csv3:
    for item in csvList:
        if relation[0] == item[1]:
            relation[0] = item[0]
        if relation[1] == item[1]:
            relation[1] = item[0]

with open('C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\resources\\edges.csv', mode='w') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(('Source','Target','Weight'))
    for relation in data_for_csv3:
        writer.writerow(relation)

print(len(data_for_csv3))

# Code 4: transform data and write to file for networking_2
data_for_txt = []
for item in data_for_csv3:
    for iteration in range(0,int(item[2])):
        data_for_txt.append(item[0].replace(" ","") + " " + item[1].replace(" ",""))

with open('C:\\Users\\Zachary\\Desktop\\Roman_Prosopography\\resources\\edges2.txt', mode='w') as file:
    for item in data_for_txt:
        file.writelines(item+'\n')
