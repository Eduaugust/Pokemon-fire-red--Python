#CALCULA DE "PANELINHAS"
# O(|V| + |A|)

qtd_nodos = 10007
qtd_arestas = int(input())
while qtd_arestas != 0:
    try:
        lista_adj = []
        visitados = []
        for i in range(qtd_nodos + 1):
            lista_adj.append([])
            visitados.append(False)

        input_relacoes = input().split()

        lista_adj[1].append(1)

        for item in input_relacoes:
            middle = item.rindex(',')
            end = item.rindex(')')
            u, v = int(item[1:middle]), int(item[middle+1: end])
            lista_adj[u].append(v)
            lista_adj[v].append(u)

        #FAZENDO A BFS

        # visitados = []
        # for i in range(qtd_nodos + 1):
        #     visitados.append(False)

        # COMENCANDO PELO VERTICE X
        total = 0
        x = 1

        # for nodo in range(1, qtd_nodos+1):
        #     if not visitados[nodo]:
        #         visitados[nodo] = True
        #         fila = [nodo]
                
        #         panelinhas += 1
        fila = [x]
        while len(fila) > 0:
            pai = fila[0]
            fila.pop(0)

            for filho in lista_adj[pai]:
                if not visitados[filho]:
                    visitados[filho] = True
                    fila.append(filho)
                    total += 1
                    

        print(total)
        qtd_arestas = int(input())
    except EOFError:
        pass