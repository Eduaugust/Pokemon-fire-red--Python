import json

txt = open('base_xp.txt', 'r')
json_file = open('base_xp.json', 'w')

dict_pokemons = dict()

for i in range(177):
    f = txt.readline().split()
    name = f[2]
    
    dict_pokemons[name] = f[-8]
json.dump(dict_pokemons, json_file)
json_file.close()
txt.close()