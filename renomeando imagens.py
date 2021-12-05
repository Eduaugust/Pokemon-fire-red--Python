from pathlib import Path
import os
pasta = 'src/intro/'
mapas = dict()
pathlist = Path('src/intro/').glob('**/*.gif')
i = 0
for path in pathlist:
    i += 1
    try:
        os.rename('src/intro/'+path.name, 'src/intro/'+ str(i)+'.png')
    finally: 
        print('oxi')