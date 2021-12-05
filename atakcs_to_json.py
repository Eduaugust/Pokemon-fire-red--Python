import json

txt = open('atacks.txt', 'r')
json_file = open('atacks.json', 'w')
f = txt.readline().split()
f = [0]

dict_pokemons = dict()

while int(f[0]) < 826:
    f = txt.readline().split()
    name = f[1:-7]
    name = ' '.join(name)
    
    object = {"Type": f[-7], "Category": f[-6], "Contest": f[-5], "PP": f[-4], "Power": f[-3], "Accuracy": f[-2], "Gen": f[-1]}
    dict_pokemons[name] = object
json.dump(dict_pokemons, json_file)
json_file.close()
txt.close()