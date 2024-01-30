import os
import json

path = os.path.abspath(os.path.dirname(__file__))
documents = []

with open(path + "/structure.json", 'r', encoding='utf-8') as file:
    documents = dict(json.loads(file.read())[0])

for category, document in documents.items():
    print(category)
    print("--------------------")
    for doc in document:
        print("1111111111111111111111111")
        print(doc['title'])
        print("1111111111111111111111111")
    print("++++++++++++++++")