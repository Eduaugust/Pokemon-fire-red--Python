import json

txt = open('relation_types.txt', 'r')
json_file = open('relation_types.json', 'w')
name_defend = txt.readline().split()
dict_result = dict()
for item in name_defend:
    dict_result[item] = dict()
for i in range(18):
    f = txt.readline().split()
    type = f[0]
    for i in range(len(name_defend)):
        dict_result[name_defend[i]][type] = float(f[i+1])
json.dump(dict_result, json_file)
json_file.close()
txt.close()