import json

txt = open('pokemon.txt', 'r')
json_file = open('pokemon.json', 'w')

dict_pokemons = dict()
for i in range(151):
    f = txt.readline().split()
    name = f[0]
    
    object = {"Type": [f[1], f[2]], "HP": f[3], "Attack": f[4], "Defense": f[5], "SAtack": f[6], "SDefense": f[7], "Speed": f[8]}
    dict_pokemons[name] = object
json.dump(dict_pokemons, json_file)
json_file.close()
txt.close()