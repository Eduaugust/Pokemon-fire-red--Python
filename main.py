from graphics import *
import time
from pathlib import Path
from keyboard import *
from save import *
import json
import random

def intro():
    text = Text(Point(*half_screen), "© 2021 Pokemon\n© 2021-2026 Furg\n© Eduardo Augusto\n© 149182")
    text.setFill('white')
    text.draw(win)
    win.getMouse()
    text.undraw()
    gif_intro = [Image(Point(*half_screen), 'src/Intro/'+str(i)+'.png') for i in range(1, 188)]
    frame = 0
    while frame < 155:
        gif_intro[frame].draw(win)
        if win.checkMouse() != None:
            pass
        frame = (frame + 1) % len(gif_intro)
        gif_intro[frame].undraw()
        time.sleep(0.1)
    gif_intro[frame].draw(win)
    ativo = gif_intro[frame]
    while win.checkMouse() == None:
        gif_intro[frame].undraw()
        frame = (frame + 1) % len(gif_intro)
        if frame < 155:
            frame = 155
        gif_intro[frame].draw(win)
        ativo = gif_intro[frame]
        time.sleep(0.1)
    ativo.undraw()
    i = 1

    #Limpando tela
    Image(Point(0,0), 'src/tela_preta.png').draw(win)

def tutorial():
    def pokeball(closepen):
        pokeball = Image(Point(*half_screen),'src/tutorial/pokeball_hand_'+closepen+'.png').draw(win)
        return pokeball
    

        
    character_positions = Point(half_screen[0], half_screen[1] - 20)
    background = Image(Point(*half_screen), 'src/tutorial/apresentation.png').draw(win)
    prof = Image(character_positions, 'src/tutorial/prof.png').draw(win)
    p1 = Image(character_positions, 'src/player1/big.png')
    enemy = Image(character_positions, 'src/rival/big.png')
    texts = [
        'Olá!'.ljust(31)+'\nÉ um prazer conhece-lo'.ljust(31),
        'Bem-vindo ao mundo de Pokémon'.ljust(31),
        'Meu nome é OAK.'.ljust(31),
        'As pessoas me conhecem como\n'.ljust(31)+'PROFESSOR'.ljust(31),
        'Esse mundo...'.ljust(31),
        '...é habitado por criaturas\n'.ljust(31)+ 'chamadas POKÉMONS.'.ljust(31),
        'Para algumas pessoas, Pokémons\n'.ljust(31)+ 'são pets.'.ljust(31),
        'Outros usam eles para batalhar'.ljust(31),
        'Para mim...'.ljust(31),
        'Eu os estudo como profissão.'.ljust(31),
        'Vamos falar sobre você. '.ljust(31),
        'Vamos começar pelo seu nome,\n'.ljust(31)+'qual é o seu?'.ljust(31),
        'Esse é o meu neto'.ljust(31),
        'Voces são rivals desde\n'.ljust(31)+'que eram bebes'.ljust(31),
        'Erm... qual era o nome dele?'.ljust(31),
        '...Er, era Garry?'.ljust(31),
        'Eu lembro agora! é isso mesmo\n'.ljust(31) + 'seu nome é Garry.'.ljust(31),
        'Sua própria lenda do Pokémon\n'.ljust(31)+ 'está prestes a começar'.ljust(31),
        'Um mundo de sonhos e aventuras  \n'.ljust(31)+ 'aguarda, vamos lá!'.ljust(31),
        ]
    for t in range(len(texts)):
        text_down(texts[t])
        if t == 3:
            open_ball = pokeball('close')
        if t == 4:
            open_ball.undraw()
            close_ball = pokeball('open')
        if t == 8:
            close_ball.undraw()
        if t == 11:
            name = entry_input()
            prof.undraw()
            p1.draw(win)
            text_down('Então você se chama {0}'.format(name).ljust(31),)
        if t == 12:
            p1.undraw()
            enemy.draw(win)
        if t == 16:
            enemy.undraw()
            p1.draw(win)
    p1.undraw()
    background.undraw()
    data = getSave()
    data['name'] = name
    data['first'] = 0
    f = open('save.json', 'w')
    json.dump(data, f)
    f.close()     

def entry_input():
        input = Entry(Point(*half_screen), 13)
        input.draw(win)
        key = win.checkKey()
        while win.checkKey() != "Return":
            key = win.checkKey()
        text = input.getText()
        input.undraw()
        return text

def text_down(p):
    image_box = Image(Point(*half_screen), 'src/text_template.png').draw(win)
    t = Text(Point(half_screen[0], half_screen[1]*2 - 37), p)
    t.setTextColor(color_rgb(23, 23, 23))
    t.setSize(13)
    t.setFace("courier")
    t.draw(win)
    win.getMouse()
    image_box.undraw()
    t.undraw()

def mapa(pasta, map_points):
        mapas = dict()
        pathlist = Path(pasta).glob('**/*.png')       
        for path in pathlist:
            if not path.name[2:4] in mapas:
                mapas[path.name[2:4]] = dict()
            mapas[path.name[2:4]][path.name[17:-4]] = path.name
        
        for map_nivel in mapas: # {'00' : {...}}
            for caminho in mapas[map_nivel]: # {'Barrar_w': str(), 'Arbustos': str()...}
                mapas[map_nivel][caminho] = Image(Point(*map_points), pasta + mapas[map_nivel][caminho])
        
        return mapas

def draw_map(mapa, x, y):
    global name_mapas
    for i in name_mapas:
        mapa[0][mapa[1]][i].draw(win)
        mapa[0][mapa[1]][i].move(x, y)
    
def undraw_map(mapa, name_maps, nivel):
    for i in name_maps:
        mapa[nivel][i].undraw()

def character_animation(win, direcao, frame, character, ativo, is_move):
    ativo.undraw()
    if is_move:
        frame = (frame + 1) % len(character[direcao])
    else:
        frame = 0
    character[direcao][frame].draw(win)
    ativo = character[direcao][frame]
    return frame, character, ativo

def check_colision(mapas, x, y):
    colisao = mapas.getAnchor()
    width, height = int(mapas.getWidth()), int(mapas.getHeight() / 2)
    colisao_x, colisao_y = int(colisao.getX()), int(colisao.getY())
    if mapas.getPixel(int(width - colisao_x + x) , int( y + height - colisao_y) ) != [0, 0, 0]:
        return True 
    else:
        return False

def move(framerate, direcao, mapas, x, y):
    if is_pressed('b'):
        velocidade = 110 * framerate * 2
    else:
        velocidade = 110 * framerate
    is_move = True
    if is_pressed('a'):
        if not check_colision(mapas["Colision"], -velocidade + x, 0 + y):                         
            for item in  mapas:
                    mapas[item].move(velocidade, 0)
        direcao = 'a'
    elif is_pressed('w'):
        if not check_colision(mapas["Colision"], 0 + x,y+ -velocidade ) and not check_colision(mapas["Barrar_w"], x+0,y+ -velocidade): 
            for item in  mapas:
                mapas[item].move(0, velocidade)
        direcao = 'w'
    elif is_pressed('s'):
        if not check_colision(mapas["Colision"], 0+x,y+ velocidade ):  
            for item in  mapas:
                mapas[item].move(0,-velocidade)
        direcao = 's'
    elif is_pressed('d'):
        if not check_colision(mapas["Colision"], velocidade+x,y+ 0): 
            for item in  mapas:
                mapas[item].move(-velocidade, 0)
        direcao = 'd'
    else:
        is_move = False
    if check_colision(mapas["Arbustos"], 0 + x,y):
        wild_pokemon()
    return direcao, is_move, mapas

def wild_pokemon():
    if random.randrange(0, 101) == 1:
        if mapa_ativo == dict_mapas:
            pokemons_inimigo = get_pokemon_inimigo_by_name('route 01')
            num = random.randrange(0, 1)
            level = random.randrange(2,5)
            pokemon = pokemons_inimigo[num]
            pokemon['Level'] = level
            battle_main([pokemon], 'Selvagem')

def check_mission_change():
    global mission_change, missoes_data
    if mission_change:
        data = getMission()
        mission_change = False
        missoes_data = data

def check_local_mission():
    for num_missao in missoes_data:
        if not missoes_data[num_missao]['complete']:
            local_missao = missoes_data[num_missao]['localization'].split(', ')
            mapa_centro = mapa_ativo[0][mapa_ativo[1]]['Arbustos'].getAnchor()
            if mapa_ativo == dict_mapas:
                if abs(float(local_missao[0]) - mapa_centro.getX()) <= 20 and abs(float(local_missao[1]) - mapa_centro.getY()) <= 3:
                    if num_missao == '01':
                        warning_first()
                        missoes_data[num_missao]['complete'] = 1
                    elif num_missao == '02':
                        warning_message() 
            elif mapa_ativo == pallet_interior['lab-00']:
                if abs(float(local_missao[0]) - mapa_centro.getX()) <= 2 and abs(float(local_missao[1]) - mapa_centro.getY()) <= 4:
                    if num_missao == '09':
                            missao9()         
                            missoes_data[num_missao]['complete'] = 1
                    if num_missao == '03':
                            starter_pokemon_text()         
                            missoes_data[num_missao]['complete'] = 1
                    elif missoes_data['03']['complete'] and not missoes_data['04']['complete']:
                        choice = ''
                        if is_pressed('SPACE'):
                            charmander = {"Name":"Charmander", "XP": 125, "Attacks":["Growl", "Scratch"], "Life": 100, "Level": 5}
                            bulbasaur = {"Name":"Bulbasaur", "XP": 125, "Attacks":["Growl", "Tackle"], "Life": 100, "Level": 5}
                            squirtle = {"Name":"Squirtle", "XP": 125, "Attacks":["Tackle", "Tail Whip"], "Life": 100, "Level": 5}

                            if num_missao == '04':
                                    choice = starter_pokemon_choice(0)      
                                    if choice == 's': 
                                        # coloca na mochila
                                        set_pokemon_in_bag('1', bulbasaur)
                                        # coloca na mochila do garry
                                        file = open('inimigos.json', 'r')
                                        data = json.load(file)
                                        file.close()
                                        data['Garry 01'] = [charmander]
                                        f = open('inimigos.json', 'w')
                                        json.dump(data, f)
                                        f.close()
                            if num_missao == '05':
                                    choice = starter_pokemon_choice(1)         
                                    if choice == 's': 
                                        # coloca na mochila
                                        set_pokemon_in_bag('1', squirtle)
                                        # coloca na mochila do garry
                                        file = open('inimigos.json', 'r')
                                        data = json.load(file)
                                        file.close()
                                        data['Garry 01'] = [bulbasaur]
                                        f = open('inimigos.json', 'w')
                                        json.dump(data, f)
                                        f.close()
                            if num_missao == '06':
                                    choice = starter_pokemon_choice(2)         
                                    if choice == 's': 
                                        # coloca na mochila
                                        set_pokemon_in_bag('1', charmander)
                                        # coloca na mochila do garry
                                        file = open('inimigos.json', 'r')
                                        data = json.load(file)
                                        file.close()
                                        data['Garry 01'] = [squirtle]
                                        f = open('inimigos.json', 'w')
                                        json.dump(data, f)
                                        f.close()
                        if choice == 's':
                            missoes_data['01']['complete'] = 1  
                            missoes_data['02']['complete'] = 1                
                            missoes_data['04']['complete'] = 1   
                            missoes_data['05']['complete'] = 1   
                            missoes_data['06']['complete'] = 1   
                elif num_missao=='07' and missoes_data['04']['complete'] and not missoes_data['07']['complete']:
                    if abs(float(local_missao[0]) - mapa_centro.getX()) <= 100 and abs(float(local_missao[1]) - mapa_centro.getY()) <= 2 :
                        missao7()
                        missoes_data['07']['complete'] = 1   
            elif mapa_ativo == viridian['loja-02']:
                if num_missao == '08' and abs(float(local_missao[0]) - mapa_centro.getX()) <= 20 and abs(float(local_missao[1]) - mapa_centro.getY()) <= 3:
                        missao08()
                        missoes_data[num_missao]['complete'] = 1
                elif num_missao == '10' and is_pressed('SPACE') and abs(float(local_missao[0]) - mapa_centro.getX()) <= 4 and abs(float(local_missao[1]) - mapa_centro.getY()) <= 6:
                    open_market()
            elif mapa_ativo == viridian['cura-01']:
                if num_missao == '11' and is_pressed('SPACE') and abs(float(local_missao[0]) - mapa_centro.getX()) <= 4 and abs(float(local_missao[1]) - mapa_centro.getY()) <= 3:
                    text_cura()
                    cura()

def cura():
    data = get_json_data('bag.json')
    for item in data:
        if item != 'itens' and item != 'money':
            data[item]['Life'] = 100
    f = open('bag.json', 'w')
    json.dump(data, f)
    f.close()

def text_cura():
    text_down('Olá! Bem vindo ao centro POKÉMON!'.ljust(31) + '\na saúde perfeita!'.ljust(31))
    text_down('Vou deixar seus POKÉMON com'.ljust(31) + '\na saúde perfeita!'.ljust(31))
    text_down('Levarei eles por '.ljust(31) + '\nalguns segundos.'.ljust(31))
    text_down('Obrigada por esperar!'.ljust(31) + '\nCuramos eles totalmente!'.ljust(31))
    text_down('Espero ve-lo novamente!'.ljust(31) + '\n'.ljust(31))

def missao9():
    texts = [
        "OAK: Oh {0}!".format(start['name']).ljust(31) + '\nComo está meu velho Pokémon?'.ljust(31),
        'Bem, parece está crescendo'.ljust(31) + '\ncada vez mais ligado a você.'.ljust(31),
        'Você parece ser um ótimo '.ljust(31) + '\nTREINADOR POKÉMON.'.ljust(31),
        'O que?'.ljust(31) + '\nVocê tem algo para mim?'.ljust(31),
        "{0} entregou OAK's PARCEL".format(start['name']).ljust(31),
        'Ah! Isto é uma Pokébola'.ljust(31) + '\npersonalizada!'.ljust(31),
        'Obrigado!'.ljust(31) + '\n'.ljust(31),
    ]
    for item in texts:
        text_down(item)
    rival = Image(Point(half_screen[0]-15, half_screen[1]), 'src/rival/w.png').draw(win)
    text_down('Garry: Vovô!'.ljust(31) + '\n'.ljust(31))
    text_down('Garry: Quase esqueci!'.ljust(31) + '\nPorque me chamou?'.ljust(31) )
    text_down('OAK: Quero que vocês'.ljust(31) + '\nconheçam vários pokémons!'.ljust(31) )
    text_down('OAK entregou 5 Pókebolas'.ljust(31) + '\n'.ljust(31) )
    set_item_in_bag('pokeballs', 5)
    text_down('Vocês poderam captura-los agora'.ljust(31) + '\n'.ljust(31) )
    text_down('Quando um Pokémon selvagem'.ljust(31) + '\naparecer é facil!'.ljust(31) )
    text_down('Basta jogar uma Poké bola'.ljust(31) + '\npara tentar pega-lo!'.ljust(31) )
    text_down('Um Pokémon selvagem pode'.ljust(31) + '\nescapar, é preciso ter sorte!'.ljust(31) )
    text_down('Quero fazer um guia com'.ljust(31) + '\ntodos os Pokémons'.ljust(31) )
    text_down('Mas minha Pokédex ainda'.ljust(31) + '\nnão está pronta...'.ljust(31) )
    text_down('Garry: Pokédex?'.ljust(31) + '\n'.ljust(31) )
    text_down('OAK: Bom... Deixe isso para lá'.ljust(31) + '\nAinda preciso desenvolve-la'.ljust(31) )
    text_down('Garry: Certo, vovô!'.ljust(31) + '\nDeixe tudo comigo!'.ljust(31))
    rival.undraw()
    rival = Image(Point(half_screen[0]-15, half_screen[1]), 'src/rival/d.png').draw(win)
    text_down('{0} odeio dizer isso, mas'.format(start['name']).ljust(31) + '\nvocê não será necessário!'.ljust(31))
    text_down('Vou pedir um MAPA DA CIDADE a'.ljust(31) + '\nminha irmã!'.ljust(31))
    text_down('Vou falar para ela não te dar,'.ljust(31) + '\n{0}! Hahaha!'.format(start['name']).ljust(31))
    text_down('Depois dessa nem se preocupe'.ljust(31) + '\nem tentar me seguir.'.ljust(31))
    rival.undraw()

def starter_pokemon_choice(choice):
    arr = ['Bulbasaur', 'Squirtle', 'Charmander']
    texts = ['Nossa! Bulbasaur! Grama!'.ljust(31) + '\nÉ super fácil treina-lo'.ljust(31), 'Hm! Squirtle, água!'.ljust(31) + '\nÉ ligeiramente fácil treina-lo'.ljust(31), 'Ah! Charmander! Fogo!'.ljust(31) + '\nDeve-se treina-lo com paciencia'.ljust(31)]
    pokemon = arr[choice]
    rect = Rectangle(Point(half_screen[0]-25, half_screen[1]-25), Point(half_screen[0]+25, half_screen[1]+25))
    rect.setFill('white')
    rect.setOutline('blue4')
    rect.draw(win)
    img = Image(Point(*half_screen), 'src/battle/front/{}.png'.format(pokemon)).draw(win)
    text_down(texts[choice])
    text_down('Então, {0}, você'.format(start['name']).ljust(31) +  '\nquer ficar com {0}?'.format(pokemon).ljust(31))
    text_down("Clique com o mouse, depois".ljust(31) +  "\n em 's' ou 'n'".ljust(31) )
    choice = win.checkKey()
    while choice != 's' and choice != 'n':
        choice = win.checkKey()
    img.undraw()
    rect.undraw()
    return choice

def missao08():
    texts = [
        "Hey, você vem de Pallet Town?".ljust(31),
        "Você conhece o OAK, certo?".ljust(31),
        "Tenho algo para ele.".ljust(31),
        "Posso pedir que leve algo a ele?".ljust(31),
        "{0} Recebeu OAK's PARCEL".format(start['name']).ljust(31) + '\ndo vendedor.'.ljust(31),
        "Obriagdo! Diga que mando".format(start['name']).ljust(31) + '\num abraço a ele'.ljust(31)
    ]
    for t in texts:
        text_down(t)
# Mudar mapas
def check_local_change_maps():
    global mapa_ativo
    localizacao = mapa_ativo[0][mapa_ativo[1]]['Arbustos'].getAnchor() 
    x, y = localizacao.getX(), localizacao.getY()
    if is_pressed('l'):
        print(x, y)
    # Mundo aberto pallet
    if mapa_ativo == dict_mapas:
        if x >= 108 and x <= 122 and y >= -282 and y <= -280:
            change_map(pallet_interior['lab-00'], 0, -90)
        elif x <= 282.49999999999994 and x >= 269.66666666666674 and y <= -184 and y >= -186:
            change_map(pallet_interior['house1-02'], 37, -49)
        elif x <= 217.49999999999994 and x >= 145.66666666666674 and y >= 622:
            change_map(viridian['exterior-00'], 0, 0)
    # Laboratório em pallet
    elif mapa_ativo == pallet_interior['lab-00']:
        if y < 25:
            change_map(dict_mapas, 0, 0)
    # Casa do personagem
    elif mapa_ativo == pallet_interior['house1-02']:
        if x < 229 and y < 59 and x > 209:
            change_map(dict_mapas, 0, -5)
    # Mundo aberto Virdian City
    elif mapa_ativo == viridian['exterior-00']:
        if y <= -188.66666666666669:
            change_map(dict_mapas, 0, 0)
        elif x >= 140 and x <= 155 and y >= 18 and y <= 22:
            change_map(viridian['cura-01'], 0, 0)
        elif x >= -23 and x <= -5 and y >= 130 and y <= 140:
            change_map(viridian['loja-02'], 0, -45)
    # Cura 01 virdian
    elif mapa_ativo == viridian['cura-01']:
        if y < 57:
            change_map(viridian['exterior-00'], 0, 0)
    # Loja 02 virdian
    elif mapa_ativo == viridian['loja-02']:
        if y < 67:
            change_map(viridian['exterior-00'], 0, 0)

def starter_pokemon_text():
    rival = Image(Point(half_screen[0]-15, half_screen[1]), 'src/rival/w.png').draw(win)
    text_down('Garry: Vovô!'.ljust(31) + '\nEstou farto de esperar'.ljust(31))
    text_down('OAK: Garry?'.ljust(31) + '\nDeixe-me pensar...'.ljust(31))
    text_down('Oh, sim, eu disse para você vir.'.ljust(31) + '\nEspere!'.ljust(31))
    text_down(str('Aqui, {0}'.format(start['name']) + '.').ljust(31))
    text_down('Tem três pokemons aqui.'.ljust(31))
    text_down('Haha!'.ljust(31))
    text_down('Os Pókemons estão dentro'.ljust(31) + '\ndas pokebolas'.ljust(31))
    text_down('Quando jovem, eu era um incrível'.ljust(31) + '\nTREINADOR Pókemon!'.ljust(31))
    text_down('Mas agora, agora só tenho'.ljust(31) + '\nesses três.'.ljust(31))
    text_down('Você pode escolher um.'.ljust(31) + '\nVá! Escolha!'.ljust(31))
    text_down('Garry: Hey! Vovô! Não é justo!'.ljust(31) + '\nE eu?'.ljust(31))
    text_down('OAK: Calma, Garry.'.ljust(31) + '\nDepois é a sua vez!'.ljust(31))
    rival.undraw()

def warning_first():
    prof = Image(Point(half_screen[0], half_screen[1] - 25), 'src/prof/s.png').draw(win)
    text_down('OAK: Hey! Espere!'.ljust(31) + '\nNão saia!'.ljust(31))
    text_down('OAK: Não é seguro! Pókemon '.ljust(31) + '\nselvagens vivem na grama alta!'.ljust(31))
    text_down('Você precisa de um Pókemon'.ljust(31) + '\npara te protege!'.ljust(31))
    text_down('Já sei! Venha ao meu laboratório!'.ljust(31))
    prof.undraw()

def warning_message():
    text_down('Vá ao laboratório'.ljust(31))

def get_name_map():
    if mapa_ativo == dict_mapas:
        return 'dict_mapas'
    elif mapa_ativo == pallet_interior['lab']:
        return "pallet_interior['lab']"
    elif mapa_ativo == pallet_interior['house2']['01']:
        return "pallet_interior['house2']['01']"
    elif mapa_ativo == pallet_interior['house1']['02']:
        return "pallet_interior['house1']['02']"

def get_nivel(xp):
    return int(xp**(1/3))

def text_battle(p):
    t = Text(Point(half_screen[0], half_screen[1]*2 - 37), p)
    t.setTextColor(color_rgb(255,255,255))
    t.setSize(12)
    t.setFace("courier")
    t.draw(win)
    return t

def get_pokemon_stats(name, nivel):
    file = open('pokemon.json', 'r')
    data = json.load(file)
    for item in data[name]:
        if type(data[name][item]) == str:
            data[name][item] = float(data[name][item])
    data[name]['HP'] += nivel * (data[name]['HP'])* 1/50
    data[name]["Attack"] += nivel * data[name]['Attack']* 1/50
    data[name]["Defense"] += nivel * data[name]['Defense']* 1/50
    data[name]["SAtack"] += nivel * data[name]['SAtack']* 1/50
    data[name]['SDefense'] += nivel * data[name]['SDefense']* 1/50
    data[name]['Speed'] += nivel * data[name]['Speed']* 1/50
    return data[name]

def get_json_data(file):
    f = open(file,'r')
    return json.load(f)

def calc_xp_gain(wild, base, level_win):
    a = 1 if wild else 1.5 
    b = int(base)
    L = int(level_win)
    xp = int(a * b * L // 7)
    return xp

def calc_damage(info_atack, info_defense, data_atack, category_status_jogador, category_status_inimigo):
    

    #Dados do pokemon atacante

    pokemon_name_atack = get_pokemon_stats(info_atack['Name_pokemon'], info_atack['Level'])

    #Dados do pokemon que está defendendo
    pokemon_name_defense = get_pokemon_stats(info_defense['Name'], info_defense['Level'])

    # fraquezas de acordo com o tipo de pokemon
    relation_types = get_json_data('relation_types.json')

    # Tipos de ataque ou defesa de acordo com o tipo do pokemon que está atacando
    Physical = ['Bug', 'Flying', 'Fighting', 'Ghost', 'Normal', 'Poison', 'Steel', 'Ground', 'Rock']
    Special = ['Psychic', 'Fire', 'Grass', 'Water', 'Electric', 'Ice', 'Dark', 'Dragon']
    if data_atack['Type'] in Special:
        A = (pokemon_name_atack['SAttack']) * category_status_jogador['SAttack']
        D = pokemon_name_defense['SDefense'] * category_status_inimigo['SAttack']
    else:
        A = pokemon_name_atack['Attack'] * category_status_jogador['Attack']
        D = pokemon_name_defense['Defense'] * category_status_inimigo['Defense']

    # Dado aleatório de dano
    aleatorio = random.randrange(217, 256) / 255

    # Nivel do atacante
    level = info_atack['Level']
    # Poder do ataque
    power = float(data_atack['Power'])

    # agua contra fogo tem 2x mais de dano...
    if pokemon_name_defense['Type'][1] == '-':
        Type = relation_types[data_atack['Type']][pokemon_name_defense['Type'][0]]
    else:
        Type = relation_types[data_atack['Type']][pokemon_name_defense['Type'][0]] * relation_types[data_atack['Type']][pokemon_name_defense['Type'][1]]
    Accuracy = int(data_atack['Accuracy']) * category_status_jogador['Accuracy']
    Test_Accuracy = random.randrange(0, 101)
    if  Test_Accuracy <= Accuracy:
        #Fórmula do dano
        damage = 2*level/5
        damage += 2
        damage *= power * aleatorio * Type * (A/D)/50
    else:
        damage = 0

    return damage

def montar_arena(stats_npc, stats_p1):
    bg_battle.draw(win)
    # Pokemon do player 1
    pokemon_p1_image = Image(Point(85, 146), "src/battle/back/"+stats_p1["Name"]+".png").draw(win)
    nivel_p1 = Text(Point(290, 136), get_nivel(stats_p1["XP"]))
    nivel_p1.setSize(8)
    nivel_p1.draw(win)
    name_p1_image = Text(Point(235, 136), stats_p1["Name"])
    name_p1_image.setSize(8)
    name_p1_image.draw(win)
    life_p1 = Text(Point(260,148), str(int(stats_p1['Life']))+'/'+str(int(stats_p1['MaxLife'])) )
    life_p1.setSize(8)
    life_p1.draw(win)
    t = text_battle("Vai! "+stats_p1["Name"]+'!'.ljust(19))
    win.getMouse()
    t.undraw()

    pokemon_npc_image = Image(Point(260, 70), "src/battle/front/"+stats_npc["Name"]+".png").draw(win)
    nivel_npc = Text(Point(110, 38),stats_npc["Level"])
    nivel_npc.setSize(8)
    nivel_npc.draw(win)
    name_npc_image = Text(Point(60, 38), stats_npc["Name"])
    name_npc_image.setSize(8)
    name_npc_image.draw(win)
    
    life_npc = Text(Point(95,48), str(int(stats_npc['Life']))+'/'+str(int(stats_npc['HP'])) )
    life_npc.setSize(8)
    life_npc.draw(win)
    t = text_battle( str(stats_npc["Npc_name"]).ljust(31) + str("\n"+stats_npc["Name"]).ljust(32))
    win.getMouse()
    t.undraw()
    return {'p1':life_p1,  'npc':life_npc}, [pokemon_npc_image, bg_battle,pokemon_p1_image, nivel_p1, name_p1_image, life_p1, nivel_npc, name_npc_image, life_npc]

def undraw_array(arr):
    for img in arr:
        try:
            img.undraw()
        except:
            pass

def get_pokemon_inimigo_by_name(name):
    file = open('inimigos.json', 'r')
    data = json.load(file)
    return data[name]

def get_pokemon_in_bag(id):
    file = open('bag.json', 'r')
    data = json.load(file)
    return data[id]

def set_item_in_bag(item, qnt):
    file = open('bag.json', 'r')
    data = json.load(file)
    data['itens'][item] += qnt
    f = open('bag.json', 'w')
    json.dump(data, f)
    f.close()

def set_pokemon_in_bag(id, info):
    # formato do info:
    # {'id':'1', 'data':{"Name":"Venusaur", "XP": 1, "Attacks":["Growl", "Tackle", "Karate Chop", "Whirlwind"], "Life": 60, "Level": 1}}
    file = open('bag.json', 'r')
    data = json.load(file)
    data[id] = info
    f = open('bag.json', 'w')
    json.dump(data, f)
    f.close()

def fight_run(stats_p1):
    t = text_battle(str('O que ' + stats_p1['Name']).ljust(30) + str('\nirá fazer?').ljust(31))
    fightrun_image = Image(Point(*half_screen), 'src/battle/fightrun.png').draw(win)
    choice = ''
    while choice == '':
        mouse = win.checkMouse()
        if mouse != None:
            x = mouse.getX()
            y = mouse.getY()
            if x >= 241 and x <= 266 and y >= 194 and y <= 200:
                t.undraw()
                fightrun_image.undraw()
                choice = 'fight'
            if x >= 296.0 and x <= 316.0 and y >= 209.0 and y <= 217.0:
                t.undraw()
                fightrun_image.undraw()
                choice = 'run'
            if x >= 296.0 and x <= 311.0 and y >= 190.0 and y <= 203.0:
                t.undraw()
                fightrun_image.undraw()
                choice = 'bag'
            if x >= 238.0 and x <= 280.0 and y >= 208.0 and y <= 218.0:
                t.undraw()
                fightrun_image.undraw()
                choice = 'pokemon'
    return choice

def choice_atack_num(stats_p1):
    # Escreve o ataque na tela
    Attacks = stats_p1['Attacks']
    len_attacks = len(Attacks)
    aar_attack = []
    if len_attacks >= 1:
        aar_attack.append(Text(Point(55, 190), Attacks[0]))
        aar_attack[0].setFill('white')
        aar_attack[0].draw(win)
    if len_attacks >= 2:
        aar_attack.append(Text(Point(190, 190), Attacks[1]))
        aar_attack[1].setFill('white')
        aar_attack[1].draw(win)
    if len_attacks >= 3:
        aar_attack.append(Text(Point(55, 218), Attacks[2]))
        aar_attack[2].setFill('white')
        aar_attack[2].draw(win)
    if len_attacks >= 4:
        aar_attack.append(Text(Point(190, 218), Attacks[3]))
        aar_attack[3].setFill('white')
        aar_attack[3].draw(win)

    # Escolha do ataque
    choice = ''
    while choice == '':
        mouse = win.checkMouse()
        if mouse != None:
            x = mouse.getX()
            y = mouse.getY()
            if x >= 15.0 and x <= 123.0 and y >= 182 and y <= 197:
                choice = 0
            if x >= 13.0 and x <= 105.0 and y >= 209.0 and y <= 224.0:
                 choice = 2
            if x >= 136 and x <= 225.0 and y >= 182.0 and  y <= 196.0:
                 choice = 1
            if x >= 141.0 and x <= 235.0 and y >= 210.0 and y <= 227.0:
                 choice = 3
    for item in aar_attack:
        item.undraw()
    return choice

def more_pokemons():
    pass

def select_open_pokemon():
    bag_bg = Image(Point(*half_screen), 'src/battle/poke/base.png').draw(win)
    # Dados
    data = get_json_data('bag.json')
    arr_poke_all = []
    arr_poke_page = []
    arr_desmontar_page = []
    index = 0
    # Todos pokemons
    for item in data:
        if item != 'itens' and item != 'money':
            arr_poke_all.append(item)
    # Escrever dados na tela 
    def draw_pokemons():
        arr_poke_page = []
        arr_desmontar_page = []
        for i in range(6):
            try:
                poke = Text(Point(223.0, 56.0 + 16*i),'{0} {1}% L:{2}'.format(data[arr_poke_all[index + i]]['Name'], data[arr_poke_all[index + i]]['Life'], get_nivel(data[arr_poke_all[index + i]]['XP']))).draw(win)
                poke.setTextColor(color_rgb(23, 23, 23))
                poke.setSize(9)
                poke.setFace("courier")
                arr_poke_page.append(index + i)
                arr_desmontar_page.append(poke)
            except:
                break
        return arr_desmontar_page, arr_poke_page
    arr_desmontar_page, arr_poke_page = draw_pokemons()
    # Ações
    choice = ''
    choice_boolean = False
    while choice != 'sair':
        mouse = win.checkMouse()
        if mouse != None:
            x = mouse.getX()
            y = mouse.getY()
            for i in range(6):
                if x >= 160 and x <= 238 and y >= 53 + i*16 and y <= 62 + i*16:
                    select_1 = arr_poke_all[index + i]
                    undraw_array(arr_desmontar_page)
                    bag_bg.undraw()
                    return int(select_1)
            if x >= 274.0 and x <= 290.0 and y >= 156.0 and y <= 171.0:
                choice = 'sair'
                undraw_array(arr_desmontar_page)
                bag_bg.undraw()

                return 'repeat'

def open_pokemon():
    bag_bg = Image(Point(*half_screen), 'src/bag_pokemon/base.png').draw(win)
    itens_open = []
    select_1, select_2 = None, None
    # Dados
    data = get_json_data('bag.json')
    arr_poke_all = []
    arr_poke_page = []
    arr_desmontar_page = []
    index = 0
    # Todos pokemons
    for item in data:
        if item != 'itens' and item != 'money':
            arr_poke_all.append(item)
    # Escrever dados na tela 
    def draw_pokemons():
        arr_poke_page = []
        arr_desmontar_page = []
        for i in range(6):
            try:
                poke = Text(Point(223.0, 56.0 + 16*i),'{0} {1}% L:{2}'.format(data[arr_poke_all[index + i]]['Name'], data[arr_poke_all[index + i]]['Life'], get_nivel(data[arr_poke_all[index + i]]['XP']))).draw(win)
                poke.setTextColor(color_rgb(23, 23, 23))
                poke.setSize(9)
                poke.setFace("courier")
                arr_poke_page.append(index + i)
                arr_desmontar_page.append(poke)
            except:
                break
        return arr_desmontar_page, arr_poke_page
    arr_desmontar_page, arr_poke_page = draw_pokemons()
    # Ações
    choice = ''
    choice_boolean = False
    while choice != 'sair':
        mouse = win.checkMouse()
        if mouse != None:
            x = mouse.getX()
            y = mouse.getY()
            # print(x, y)
            for i in range(6):
                if x >= 160 and x <= 238 and y >= 53 + i*16 and y <= 62 + i*16:
                    if select_1 == None:
                        select_1 = arr_poke_all[index + i]
                        t = text_down("Primeiro pokémon selecionado" + str(index + i).ljust(31))
                    else: 
                        select_2 = arr_poke_all[index + i]
                        data = get_json_data('bag.json')
                        data[select_1], data[select_2] = data[select_2], data[select_1]
                        f = open('bag.json', 'w')
                        json.dump(data, f)
                        f.close()
                        t = text_down("Pokémons trocados!".ljust(31))
                        choice = 'sair'
                        undraw_array(arr_desmontar_page)
                        open_pokemon()


            if x >= 226.0 and x <= 238.0 and y >= 155.0 and y <= 169.0:
                if index > 0:
                    undraw_array(arr_desmontar_page)
                    index -= 1
                    arr_desmontar_page, arr_poke_page = draw_pokemons()
                    choice = 'back'
            if x >= 253.0 and x <= 261.0 and y >= 156.0 and y <= 168.0:
                if len(arr_poke_all) > index + 1 * 6:
                    undraw_array(arr_desmontar_page)
                    index += 1
                    arr_desmontar_page, arr_poke_page = draw_pokemons()
                    choice = 'next'
            if x >= 274.0 and x <= 290.0 and y >= 156.0 and y <= 171.0:
                choice = 'sair'
                undraw_array(arr_desmontar_page)

    bag_bg.undraw()

def config_text(t):
    t.setTextColor(color_rgb(23, 23, 23))
    t.setSize(13)
    t.setFace("courier")
    t.draw(win)
    return t

def choice_market_qtd(choice, value, data, money):
    print('oxiiiiiii')
    text_down("Qual quantidade que quer comprar?".ljust(31))
    while True:
        try:
            x = int(entry_input())
            custo = value*x
            if money - custo < 0:
                text_down("Você não tem dinheiro suficiente".ljust(31))
                break
            else:
                text_down("Você comprou".ljust(31) + "\n{0} por {1} moedas".format(choice, custo).ljust(31))
                data += x
                money -= custo   
                break                
        except:
            text_down("Insira um inteiro.".ljust(31))
    return data, money

def open_market():
    bag_bg = Image(Point(*half_screen), 'src/market/base.png').draw(win)
    itens_open = []
    # Dados
    data = get_json_data('bag.json')
    # Custo
    pokeballs = 200
    potions = 150
    antidotos = 100
    values = {"pokeballs": 200, "potions": 150, "antidotos": 100}
    # Escrever dados na tela 
    num_pokeballs = Text(Point(272.0, 56.0), '${0}'.format(pokeballs))
    num_pokeballs = config_text(num_pokeballs)
    num_potions = Text(Point(272.0, 72.0), '${0}'.format(potions))
    num_potions = config_text(num_potions)
    num_antidotos = Text(Point(272.0, 89.0), '${0}'.format(antidotos))
    num_antidotos = config_text(num_antidotos)
    num_arr = [num_pokeballs, num_antidotos, num_potions]
    # Ações
    choice = ''
    choice_boolean = False
    while choice != 'sair':
        mouse = win.checkMouse()
        if mouse != None:
            x = mouse.getX()
            y = mouse.getY()
            # print(x, y)
            if x >= 160 and x <= 238 and y >= 53 and y <= 62:
                if choice != 'pokeballs':
                    undraw_array(itens_open)
                    pokeball_descrip = Image(Point(*half_screen), 'src/bag/pokeball.png').draw(win)
                    itens_open.append(pokeball_descrip)
                else:
                    choice_boolean = True
                choice = 'pokeballs'
            elif x >= 160 and x <= 208 and y >= 68 and y <= 75:
                if choice != 'potions':
                    undraw_array(itens_open)
                    potion_descrip = Image(Point(*half_screen), 'src/bag/poçao.png').draw(win)
                    itens_open.append(potion_descrip)
                else:
                    choice_boolean = True
                choice = 'potions'
            elif x >= 160 and x <= 238 and y >= 68 and y <= 92:
                if choice != 'antidotos':
                    undraw_array(itens_open)
                    antidoto_descrip = Image(Point(*half_screen), 'src/bag/antidoto.png').draw(win)
                    itens_open.append(antidoto_descrip)
                else:
                    choice_boolean = True
                choice = 'antidotos'
            elif x >= 160 and x <= 198 and y >= 99 and y <= 107:
                undraw_array(itens_open)
                undraw_array(num_arr)
                choice = 'sair'
            if choice_boolean:
                choice_boolean = False
                data['itens'][choice], data['money'] = choice_market_qtd(choice, values[choice], data['itens'][choice], data['money'])
                print(data)
                f = open('bag.json', 'w')
                json.dump(data, f)
                f.close()
                undraw_array(itens_open)
                undraw_array(num_arr)
                choice = 'sair'
                open_market()
    bag_bg.undraw()
           
def open_bag(is_battle):
    bag_bg = Image(Point(*half_screen), 'src/bag/base.png').draw(win)
    itens_open = []
    # Dados
    data = get_json_data('bag.json')
    pokeballs = data['itens']['pokeballs']
    potions = data['itens']['potions']
    antidotos = data['itens']['antidotos']
    money = data['money']
    # Escrever dados na tela 
    num_money = Text(Point(265.0, 89+ 16*3), '${0}'.format(money))
    num_money = config_text(num_money)
    num_pokeballs = Text(Point(272.0, 56.0), 'X{0}'.format(pokeballs))
    num_pokeballs = config_text(num_pokeballs)
    num_potions = Text(Point(272.0, 72.0), 'X{0}'.format(potions))
    num_potions = config_text(num_potions)
    num_antidotos = Text(Point(272.0, 89.0), 'X{0}'.format(antidotos))
    num_antidotos = config_text(num_antidotos)
    num_arr = [num_pokeballs, num_antidotos, num_potions, num_money]
    # Ações
    choice = ''
    while choice != 'sair':

        mouse = win.checkMouse()
        if mouse != None:
            x = mouse.getX()
            y = mouse.getY()
            # print(x, y)
            if x >= 160 and x <= 238 and y >= 53 and y <= 62:
                if choice != 'pokeball':
                    undraw_array(itens_open)
                    pokeball_descrip = Image(Point(*half_screen), 'src/bag/pokeball.png').draw(win)
                    itens_open.append(pokeball_descrip)
                choice = 'pokeball'
            elif x >= 160 and x <= 208 and y >= 68 and y <= 75:
                if choice != 'potion':
                    undraw_array(itens_open)
                    potion_descrip = Image(Point(*half_screen), 'src/bag/poçao.png').draw(win)
                    itens_open.append(potion_descrip)
                choice = 'potion'
            elif x >= 160 and x <= 238 and y >= 68 and y <= 92:
                if choice != 'antidoto':
                    undraw_array(itens_open)
                    antidoto_descrip = Image(Point(*half_screen), 'src/bag/antidoto.png').draw(win)
                    itens_open.append(antidoto_descrip)
                choice = 'antidoto'
            elif x >= 160 and x <= 198 and y >= 99 and y <= 107:
                undraw_array(itens_open)
                undraw_array(num_arr)
                choice = 'sair'
            if is_battle and choice != '':
                undraw_array(itens_open)
                undraw_array(num_arr)
                bag_bg.undraw()
                return choice, pokeballs, potions, antidotos
    bag_bg.undraw()

def change_map(new_map, x, y):
    global win, mapa_ativo, maps_already_loaded
    if not new_map in maps_already_loaded:
        maps_already_loaded.append(new_map)
    else:
        x, y = 0, 0
    win.close()
    win = GraphWin("Plataform Game", *screen, False)
    win.setBackground('black')
    mapa_ativo = new_map
    draw_map(mapa_ativo, x, y)

def status_atacks_effects(stats_jogador, stats_inimigo, name_attack, name_jogador, name_inimigo):
    t = text_battle(str(name_jogador + ' usuou ' + name_attack.lower()).ljust(33))
    win.getMouse()
    t.undraw()
    if name_attack == 'Growl':
        stats_inimigo["Attack"] *= 0.9
        t = text_battle(str('O ataque de {0} diminuiu').format(name_inimigo).ljust(33))
        win.getMouse()
        t.undraw()
    elif name_attack == 'Growth':
        stats_jogador["Attack"] *= 1.1
        t = text_battle(str('O ataque de {0} aumentou').format(name_jogador).ljust(33))
        win.getMouse()
        t.undraw()
    elif name_attack == 'Leech Seed':
        roubado = stats_jogador['Life'] * 1/8
        stats_jogador['Life'] += roubado
        stats_inimigo['Life'] -= roubado
        t = text_battle(str('{0} roubou {1} de vida').format(name_jogador, roubado).ljust(33))
        win.getMouse()
        t.undraw()
    elif name_attack == 'Tail Whip' or name_attack == 'Leer':
        stats_inimigo['Defense'] *= 0.9
        t = text_battle(str('Defesa de {0} diminuida').format(name_inimigo).ljust(33))
        win.getMouse()
        t.undraw()
    elif name_attack == 'Withdraw':
        stats_inimigo['Defense'] *= 1.1
        t = text_battle(str('Defesa de {0} aumentada').format(name_jogador).ljust(33))
        win.getMouse()
        t.undraw()
    return stats_jogador, stats_inimigo

def missao7():
    global mapa_anterior, mapa_ativo
    rival = Image(Point(half_screen[0]-15, half_screen[1]), 'src/rival/d.png').draw(win)
    text_down('Garry: Espere, {0}!'.format(start['name']).ljust(31) + '\nVamos testar nossos Pókemon!'.ljust(31))
    text_down('Venha!'.ljust(31) + '\nVou usa-lo'.ljust(31))
    rival.undraw()
    pokemons_inimigo = get_pokemon_inimigo_by_name('Garry 01')
    mapa_anterior = mapa_ativo
    battle_main(pokemons_inimigo, 'Garry lançou')
    cura()

def battle_main(stats_npc_arr, npc_name):
    global battle_montar
    id_pokemon = []
    stats_p1_arr = []
    category_status_p1 = []
    category_status_npc = []
    for i in range(6):
        try:
            print('oxi')
            id_pokemon.append(str(i + 1))
            p1_pokemon = get_pokemon_in_bag(str(i + 1))
            data_p1 = get_pokemon_stats(p1_pokemon["Name"], p1_pokemon["Level"])
            p1_pokemon["Life"] = data_p1["HP"] * p1_pokemon["Life"] // 100
            p1_pokemon["MaxLife"] = data_p1["HP"]
            stats_p1_arr.append(p1_pokemon)
            print(id_pokemon, p1_pokemon, i)
            category_status_p1.append({"Attack": 1, "Defense": 1, "SAtack": 1, "SDefense": 1, "Speed": 1, "Accuracy": 1, "Poison": 0, "Vampire": 0})
            category_status_npc.append({"Attack": 1, "Defense": 1, "SAtack": 1, "SDefense": 1, "Speed": 1, "Accuracy": 1, "Poison": 0, "Vampire": 0})
        except KeyError:
            pass
    choice_pokemon_p1 = 0
    choice_pokemon_npc = 0
    stats_p1 = stats_p1_arr[choice_pokemon_p1]
    stats_npc = stats_npc_arr[choice_pokemon_npc]
    data_npc = get_pokemon_stats(stats_npc["Name"], stats_npc["Level"])
    stats_npc["Life"] = data_npc["HP"]
    stats_npc['HP'] = data_npc['HP']
    stats_npc["Npc_name"] = npc_name
    if battle_montar:
        life, arr_desmontar = montar_arena(stats_npc, stats_p1)
        battle_montar = False
        while True:
            choice= fight_run(stats_p1) 
            if choice == "bag":
                choice, pokeballs, potions, antidotos  = open_bag(True)
                if choice == 'sair':
                    choice = 'repeat'
                elif choice == 'pokeball':
                    if npc_name != 'Selvagem':
                        t = text_battle('Você não pode jogar uma PokéBall'.ljust(31) + '\nem um Pokémon de outro jogador'.ljust(31))
                        win.getMouse()
                        t.undraw()
                    elif pokeballs >= 1:
                        set_item_in_bag('pokeballs', -1)
                        chance = random.randrange(0,101)
                        t = text_battle('{0} lançou uma Poké Ball '.format(start['name']).ljust(31))
                        win.getMouse()
                        t.undraw()
                        arr_desmontar[0].undraw()
                        pokeball_gif = [Image(Point(260, 70), 'src/battle/pokeball/'+str(i)+'.png') for i in range(1, 29)]
                        frame = 0
                        for i in range(28):
                            pokeball_gif[frame].draw(win)
                            if win.checkMouse() != None:
                                pass
                            frame = (frame + 1) % len(pokeball_gif)
                            pokeball_gif[frame].undraw()
                            time.sleep(0.1)
                        for i in range(28):
                                try:
                                    frame = (frame + 1) % len(pokeball_gif)
                                    pokeball_gif[frame].undraw()
                                except:
                                    pass
                        if chance <= 40:
                            #Consegue capturar
                            t = text_battle('Gotcha!'.ljust(31) + '\n{0} capturado!'.format(stats_npc['Name']).ljust(31))
                            win.getMouse()
                            t.undraw()
                            frame = 0
                            i = 1
                            while True:
                                try:
                                    get_pokemon_in_bag(str(i + 1))
                                    i += 1
                                except:
                                    break
                            set_pokemon_in_bag(i + 1, {"Name": stats_npc['Name'], "Level":stats_npc['Level'], "XP": stats_npc['Level']**3, "Attacks": stats_npc['Attacks'], "Life": 100})
                            
                            break                        
                        else:
                            #Errou a captura
                            arr_desmontar[0].draw(win)
                            t = text_battle('{0} Escapou!'.format(stats_npc['Name']).ljust(31))
                            win.getMouse()
                            t.undraw()                            
                    else:
                        t = text_battle('Sem Pokébolas'.ljust(31))
                        win.getMouse()
                        t.undraw()
                        choice = 'repeat'
                elif choice == 'potion':
                    if potions >= 1:
                        set_item_in_bag('potions', -1)
                        stats_p1["Life"] += 20
                        if stats_p1["Life"] > p1_pokemon["MaxLife"]:
                            stats_p1["Life"] = p1_pokemon["MaxLife"]
                        life['p1'].setText( str(int(stats_p1['Life']))+'/'+str(int(stats_p1['MaxLife']))) 
                        t = text_battle('{0} foi curado em 20 de vida'.format(stats_p1["Name"]).ljust(31))
                        win.getMouse()
                        t.undraw()
                    else:
                        t = text_battle('Sem potions'.ljust(31))
                        win.getMouse()
                        t.undraw()
                        choice = 'repeat'
                elif choice == 'antidoto':
                    if antidotos >= 1:
                        category_status_p1[choice_pokemon_npc]['Poison'] = 0
                        t = text_battle('{0} não está mais envenenado'.format(stats_p1["Name"]).ljust(31))
                        win.getMouse()
                        t.undraw()
                        set_item_in_bag('antidotos', -1)
                    else:
                        t = text_battle('Sem antidotos'.ljust(31))
                        win.getMouse()
                        t.undraw()
                        choice = 'repeat'
            elif choice == "pokemon":
                choice = select_open_pokemon()  
                if choice != 'repeat':
                    undraw_array(arr_desmontar[2:6])
                    choice_pokemon_p1 = choice - 1
                    stats_p1 = stats_p1_arr[choice_pokemon_p1]
                    print(choice,  stats_p1_arr[choice_pokemon_p1], stats_p1_arr)
                    pokemon_p1_image = Image(Point(85, 146), "src/battle/back/"+stats_p1["Name"]+".png").draw(win)
                    nivel_p1 = Text(Point(290, 136), get_nivel(stats_p1["XP"]))
                    nivel_p1.setSize(8)
                    nivel_p1.draw(win)
                    name_p1_image = Text(Point(235, 136), stats_p1["Name"])
                    name_p1_image.setSize(8)
                    name_p1_image.draw(win)
                    life_p1 = Text(Point(260,148), str(int(stats_p1['Life']))+'/'+str(int(stats_p1['MaxLife'])) )
                    life_p1.setSize(8)
                    life_p1.draw(win)
                    t = text_battle("Vai! "+stats_p1["Name"]+'!'.ljust(19))
                    win.getMouse()
                    t.undraw()
                    arr_desmontar[2:6] = [pokemon_p1_image, nivel_p1, name_p1_image, life_p1]
            elif choice == 'fight':
                    # Player atacando o Inimigo
                choice_attack_num = choice_atack_num(stats_p1) # get qual ataque que foi escolhido
                level_p1 = get_nivel(stats_p1["XP"]) # Nivel do p1
                name_attack = stats_p1["Attacks"][choice_attack_num] # Nome do ataque escolhido
                name_pokemon_p1 = stats_p1["Name"] # Nome do pokemon do p1
                # Dados do ataque
                data_atack = get_json_data('atacks.json')
                data_atack = data_atack[name_attack]
                # Tipo de ataque - status ou fisico ou especial
                if data_atack['Category'] == 'Status':
                    category_status_p1[choice_pokemon_p1], category_status_npc[choice_pokemon_npc] = status_atacks_effects(category_status_p1[choice_pokemon_p1], category_status_npc[choice_pokemon_npc], name_attack, stats_p1["Name"], stats_npc["Name"])
                else:
                            # calculo do dano
                    damage = calc_damage({"Name": name_attack, "Level": level_p1, "Name_pokemon": name_pokemon_p1}, {"Name": stats_npc["Name"], "Level": stats_npc["Level"]}, data_atack, category_status_p1[choice_pokemon_p1], category_status_npc[choice_pokemon_npc])
                    stats_npc["Life"] = stats_npc["Life"] - damage # faz a vida atual menos o dano 
                    if stats_npc["Life"] < 0:
                        stats_npc["Life"] = 0
                    life['npc'].setText(str(int(stats_npc['Life']))+'/'+str(int(data_npc['HP'])) ) # coloca na tela
                    t = text_battle(str(name_pokemon_p1 + ' usuou ' + name_attack.lower()).ljust(33))
                    win.getMouse()
                    t.undraw()
                        #  ---- Se jogador vencer -----
                if stats_npc['Life'] == 0: 
                    base_xp = get_json_data('base_xp.json')
                    xp_gain = calc_xp_gain(True, base_xp[stats_npc['Name']], get_nivel(stats_p1["XP"]))
                    t = text_battle(str(name_pokemon_p1 + ' ganhou ' + str(xp_gain) + 'XP').ljust(33))
                    win.getMouse()
                    t.undraw()
                    level_anterior = int(stats_p1["XP"]**(1/3))
                    stats_p1["XP"] += xp_gain
                    if level_anterior != int(stats_p1["XP"]**(1/3)):
                        t = text_battle(str(name_pokemon_p1 + ' subiu para o nível ' + str(int(stats_p1["XP"]**(1/3)))).ljust(33))
                        win.getMouse()
                        t.undraw()
                    stats_p1["Life"] = 100*stats_p1["Life"] /stats_p1["MaxLife"] 
                    set_pokemon_in_bag(id_pokemon[choice_pokemon_p1], stats_p1)
                    if npc_name != 'Selvagem':
                        data = get_json_data('bag')
                        moedas = data['money']
                        moedas += xp_gain*1.15
                        t = text_battle(str(str(moedas)+ ' de moedas foram adicionadas a bolsa').ljust(33))
                        f = open('bag.json', 'w')
                        json.dump(data, f)
                        f.close()                    
                    break
            elif choice == "run":
                break
            if choice != 'repeat':
                # ----VEZ DO INIMIGO-----
                choice_attack_num = random.randrange(0, len(stats_npc['Attacks'])) # get qual ataque que foi escolhido
                name_attack = stats_npc["Attacks"][choice_attack_num] # Nome do ataque escolhido
                name_pokemon_npc = stats_npc["Name"] # Nome do pokemon do p1
                # Dados do ataque
                data_atack = get_json_data('atacks.json')
                data_atack = data_atack[name_attack]
                if data_atack['Category'] == 'Status':
                    category_status_npc[choice_pokemon_npc], category_status_p1[choice_pokemon_p1] = status_atacks_effects(category_status_npc[choice_pokemon_npc], category_status_p1[choice_pokemon_p1], name_attack, stats_npc['Name'], stats_p1['Name'])
                else:
                                    # calculo do dano
                    damage = calc_damage({"Name": name_attack, "Level": stats_npc['Level'], "Name_pokemon": name_pokemon_npc}, {"Name": stats_p1["Name"], "Level": get_nivel(stats_p1["XP"])}, data_atack, category_status_npc[choice_pokemon_npc], category_status_p1[choice_pokemon_p1])
                    stats_p1["Life"] = stats_p1["Life"] - damage # faz a vida atual menos o dano 
                    if stats_p1["Life"] < 0:
                        stats_p1["Life"] = 0
                    life['p1'].setText( str(int(stats_p1['Life']))+'/'+str(int(stats_p1['MaxLife']))) 
                    # coloca na tela
                    t = text_battle(str(name_pokemon_npc + ' usuou ' + name_attack.lower()).ljust(33))
                    win.getMouse()
                    t.undraw()
                        # --- Jogador perdeu ---
                if stats_p1['Life'] == 0:
                    t = text_battle(str(name_pokemon_p1 + 'desmaiou.').ljust(33))
                    stats_p1["Life"] = stats_p1["Life"] //stats_p1["MaxLife"] * 100
                    set_pokemon_in_bag(id_pokemon[choice_pokemon_p1], stats_p1)
                    win.getMouse()
                    t.undraw()
                    break
        undraw_array(arr_desmontar)

def main():   
    global battle_montar, battle
    arr_direcao = {False: 4, 'w': 0, 'a': 1, 's': 2, 'd': 3}
    p1 = [
        [Image(Point(180, 120), "src/player1/w/"+str(i)+".png") for i in range(1, 22)],
        [Image(Point(180, 120), "src/player1/a/"+str(i)+".png") for i in range(1, 21)],
        [Image(Point(180, 120), "src/player1/s/"+str(i)+".png") for i in range(1, 21)],
        [Image(Point(180, 120), "src/player1/d/"+str(i)+".png") for i in range(1, 21)],
        [Image(Point(180, 120), "src/player1/s/1.png") for i in range(1, 2)]
    ]
    p1Frame = 0
    direcao = 'w'
    ativo = p1[4][0]
    ativo.draw(win)

    while not (win.isClosed()):
        if is_pressed('p'):
            open_pokemon()
        if is_pressed('i'):
            open_bag(False)
        check_mission_change()
        try:
            check_local_mission()
            check_local_change_maps()
        except:
            pass
        else:
            battle_montar = True
            # localizacao = mapa_ativo[0][mapa_ativo[1]]['Arbustos'].getAnchor() 
            # x, y = localizacao.getX(), localizacao.getY()
            # print(x, y)
            if mapa_ativo == dict_mapas:
                direcao, is_move, dict_mapas[0][dict_mapas[1]] = move(framerate, direcao, dict_mapas[0][dict_mapas[1]] , -10, + 240//2)
            elif mapa_ativo == pallet_interior['lab-00']:
                direcao, is_move, pallet_interior['lab-00'][0][pallet_interior['lab-00'][1]]  = move(framerate, direcao, pallet_interior['lab-00'][0][pallet_interior['lab-00'][1]], 70, 240//2)
            elif mapa_ativo == pallet_interior['house2-01']:
                direcao, is_move, pallet_interior['house2-01'][0][pallet_interior['house2-01'][1]] = move(framerate, direcao, pallet_interior['house2-01'][0][pallet_interior['house2-01'][1]], 70, 240//2 )
            elif mapa_ativo == pallet_interior['house1-02']:
                direcao, is_move, pallet_interior['house1-02'][0][pallet_interior['house1-02'][1]] = move(framerate, direcao, pallet_interior['house1-02'][0][pallet_interior['house1-02'][1]], 70, 240//2 )
            elif mapa_ativo == viridian['exterior-00']:
                direcao, is_move,viridian['exterior-00'][0][viridian['exterior-00'][1]] = move(framerate, direcao, viridian['exterior-00'][0][viridian['exterior-00'][1]],  -213, 240//2)
            elif mapa_ativo == viridian['cura-01']:
                direcao, is_move,viridian['cura-01'][0][viridian['cura-01'][1]] = move(framerate, direcao, viridian['cura-01'][0][viridian['cura-01'][1]], 44, +127)
            elif mapa_ativo == viridian['loja-02']:
                direcao, is_move,viridian['loja-02'][0][viridian['loja-02'][1]] = move(framerate, direcao, viridian['loja-02'][0][viridian['loja-02'][1]],  74, 256//2)
            elif mapa_ativo == viridian['casa-03']:
                direcao, is_move,viridian['casa-03'][0][viridian['casa-03'][1]] = move(framerate, direcao, viridian['casa-03'][0][viridian['casa-03'][1]],  77, 240//2)
            else:
                print('erro')
            p1Frame, p1, ativo = character_animation(win, arr_direcao[direcao], p1Frame, p1, ativo, is_move)
        update()
        time.sleep(framerate)
    win.close()
    print(mapa_ativo[0][mapa_ativo[1]]['Arbustos'])
    centro = mapa_ativo[mapa_ativo[1]]['Arbustos'].getAnchor()
    x, y = str(centro.getX()), str(centro.getY())
    setSave(x + ', ' + y, str(mapa_ativo))

if __name__ == "__main__":
    start = getSave()
    mission_change = True
    # Configurando Graphics
    screen = (240*3/2, 1.5*160)
    half_screen = (screen[0]//2, screen[1]//2)
    framerate = 1/60
    win = GraphWin("Plataform Game", *screen, False)
    win.setBackground('black')

    # Start no jogo
    # intro()

    #dict_mapas
    maps_already_loaded = []
    if start['first']:
        tutorial()
        map_points = "277, -186".split(', ')
    else:
        map_points = "277, 600".split(', ')

        #map_points = start['levels']['level00'].split(', ')
    map_points = tuple([float(i) for i in map_points])
    nivel = '00'
    name_mapas = ['Floor', 'Colision', 'Arbustos', 'Barrar_w', 'Door', 'Other1', 'Other2', 'Other3', 'Other4']
    dir_png = 'pallet/png/'
    dict_mapas = (mapa(dir_png, map_points), '00')
    pallet_interior = dict()
    viridian = dict()
    pallet_interior['lab-00'] = (mapa('palletInterior/png/', half_screen), '00')
    pallet_interior['house2-01'] = (mapa('palletInterior/png/', half_screen), '01')
    pallet_interior['house1-02'] = (mapa('palletInterior/png/', half_screen), '02')
    viridian['exterior-00'] = (mapa('virdianCity/png/', (half_screen[0] - 10, half_screen[1] - 305)), '00')
    viridian['cura-01'] = (mapa('virdianCity/png/', (half_screen[0] + 3, half_screen[1] - 50)), '01')
    viridian['loja-02'] = (mapa('virdianCity/png/', half_screen), '02')
    viridian['casa-03'] = (mapa('virdianCity/png/', half_screen), '03')
    viridian['forest-00'] = (mapa('virdianForest/png/', half_screen), '00')
    if start['first']:
        mapa_ativo = dict_mapas
    else:
        mapa_ativo = dict_mapas
        #carregar mapa ativo
    draw_map(mapa_ativo, 0, 0)
    maps_already_loaded.append(mapa_ativo)
    mapa_anterior = mapa_ativo

    # Config Batalhas
    bg_battle = Image(Point(*half_screen), "src/battle/bg.png")
    battle = False
    battle_montar = True
    #missoes
    missoes_data = getMission()
    main()