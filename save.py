import json

def setSave(point_image, mapa):
    data = getSave()
    data['levels']['level00'] = point_image
    data['mapa'] = mapa
    f = open('save.json', 'w')
    json.dump(data, f)
    f.close()
def getSave():
    f = open('save.json', 'r')
    data = json.load(f)
    f.close()
    return data
def getMission():
    f = open('missoes.json', 'r')
    data = json.load(f)
    f.close()
    return data

def setMission():
    f = open('missoes.json', 'r')
    data = json.load(f)
    f.close()
    return data