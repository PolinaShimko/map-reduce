import json
import time

#создаем список всех терминов 
all_terms = set()
for i in range(len(data)):  
    lst = data[i]['text'].split()
    [all_terms.add(term) for term in lst]


inv_index = {}
for term in all_terms:
    count = 0
    doc = []

    for i in range(len(data)):
        if term in data[i]['text'].split():
            count += 1
            doc.append(i)

    inv_index[term] = {
        'count': count,
        'document': doc
    }
