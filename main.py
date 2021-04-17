# This is a sample Python script.
# from google.colab import files
import io
import csv
import json
import statistics

import numpy as np
import pandas

def calculaTempoAleatorio(paramArray):
    # espera o a array no segunte formato:
    # 0: N ou U, indicando se normal ou uniforme
    # 1: parametro 1 da distribuição (centro para N, limite inferior para U)
    # 2: paramentro 2 da distribuição (amplitude para N, limite superior para U)
    if paramArray[0] == "N":
        tempo = np.random.normal(int(paramArray[1]), int(paramArray[2]))
    elif paramArray[0] == "U":
        tempo = np.random.uniform(int(paramArray[1]), int(paramArray[2]))
    if tempo < 0:  # previne tempo negativo
        tempo = 0
    return round(tempo, 2)  # retorna o tempo, arredondando para duas decimais


def calculateDijkstraDistances(vetorArray, origem, destino):
    # identifies NODES from vector array (List)
    nodesArray = set()
    for vetor in vetorArray:
        nodesArray.add(vetor[0])
        nodesArray.add(vetor[1])

    # Creates a Dictionary containing nodes and the acumulated optimal distance
    nodesDijkstra = dict()
    for node in nodesArray:
        nodesDijkstra[node] = dict()
        nodesDijkstra[node]["dist"] = False
        nodesDijkstra[node]["origin"] = False

    # Initializes the starting Point
    nodesDijkstra[origem]["origin"] = origem
    nodesDijkstra[origem]["dist"] = 0

    # DIJKSTRA ALGORITH LOGIC, SET THE DISTANCES COMPUTED TO EACH NODE
    # Loop through nodes
    arrayStartingNode = {origem}  # Set with nodes that still need to be evaluated, starting by the origin
    while len(arrayStartingNode) > 0:  # while there is still a node to be evaluated...
        nodeId = arrayStartingNode.pop()  # fist node to be evaluated
        for vetor in vetorArray:
            if vetor[0] == nodeId:
                dist = int(vetor[2]) + nodesDijkstra[vetor[0]]["dist"]
                if nodesDijkstra[vetor[1]]["origin"] == False or nodesDijkstra[vetor[1]]["dist"] > dist:
                    nodesDijkstra[vetor[1]]["origin"] = vetor[0]
                    nodesDijkstra[vetor[1]]["dist"] = dist
                    arrayStartingNode.add(vetor[1])

    # Builds the path with the node values calculated above
    caminhoDijkstra = list()
    while destino != origem:  # volta o caminho até a origem (vai atlerando a variavel destino)
        for vetor in vetorArray:
            if vetor[0] == nodesDijkstra[destino]["origin"] and vetor[1] == destino:
                caminhoDijkstra.insert(0, vetor)
                destino = vetor[0]

    return caminhoDijkstra


# calculateDijkstraDistances(vetorArray, "A", "Z")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    import os

    # from tkinter import Tk
    # from tkinter.filedialog import askopenfilename
    vetoraux = list()
    vetorArray = list()
    vetorArray2 = list()
    inicio = str()
    fim = str()
    # Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    # filepath = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    # filename = os.path.basename (filepath)
    with open('GRAFOTP1.CSV') as csv_file:

        csv_reader = csv.DictReader(csv_file, fieldnames=["START", "FINISH", "DIST"])
        csv_reader.__next__()
        for row in csv_reader:
            vetoraux = [row["START"], row["FINISH"], row["DIST"]]  # = [i for i in csv.reader(row, delimiter=",") ]
            vetorArray.append(vetoraux)
        vetorArray2 = vetorArray[:]

    #        # print("array:" +str(vetorArray) )
            #vetorArray.pop(0)

    #print("array:" + str(vetorArray))

    # a_csv_file = open("GRAFOTP1.CSV", "r")

    # dict_reader = csv.DictReader(a_csv_file)

    # ordered_dict_from_csv = list(dict_reader)[0]

    # dict_from_csv = dict(ordered_dict_from_csv)
    paramCsv = dict()
    with open('PARAMETROSTP1.CSV') as csv_file:
        #paramaux = dict()
        csv_reader = csv.DictReader(csv_file, fieldnames=["Original", "Tipo", "arg1", "arg2"])
        csv_reader.__next__()
        for row in csv_reader:
            paramaux = [row["Tipo"], row["arg1"], row["arg2"]]
            paramCsv[row["Original"]] = paramaux

    with open('EXTREMIDADES.csv') as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=["START", "END"])
        csv_reader.__next__()
        for row in csv_reader:
            inicio = row["START"]
            fim = row["END"]

import numpy as np
import scipy.stats as st


import copy
#
N = 400 #Define número de simulações
#
# # cria Dictionary para receber as frequencias
vetorcaminho = list()
vetorQnt = dict()
for vetor in vetorArray:
     vetorQnt[vetor[0] + "_" + vetor[1]] = 0
     vetorPerc = copy.deepcopy(vetorQnt)
#
custoamostras = list()
# # LOOP DE SIMULAÇÃO
with open('simulacao.csv', 'w',newline='') as file:
    f = csv.writer(file)
    f.writerow("teste 123")

    for x in range(0, N):
#     # duplica array de vetores para criação de tempos aleatórios
        vetorRandom = copy.deepcopy(vetorArray)
#
      # sobrescreve o tempo com tempos aleatórios
        for vetor in vetorRandom:
            vetor[2] = calculaTempoAleatorio(paramCsv[vetor[2]])
#
#         # aplica algorito de DIJKSTRA
        melhorCaminho = calculateDijkstraDistances(vetorRandom, inicio, fim)
        f.writerow(str(melhorCaminho))
#        melhorCaminho.

        custoprocesso = 0.0
       # print ("Melhor Caminho: " + str(melhorCaminho))
#     # computa ocorrencia do caminho
        for vetor in melhorCaminho:
            tmp = vetor[0] + "_" + vetor[1]
            custo = float(vetor[2])
            custoprocesso = custo + custoprocesso
            vetorQnt[tmp] = vetorQnt[tmp] + 1

       # print("Melhor caminho: " +str(melhorCaminho)) # + " Custo: " + str(custoprocesso))
         #   print ("tmp: " + tmp)
        custoamostras.append(custoprocesso)
    media = np.mean(custoamostras)
    desviopadrao = np.std(custoamostras, axis=None, dtype=float)
    alfa = 0.99
    intervaloconfianca =st.t.interval(float(alfa), len(custoamostras)-1, loc=np.mean(custoamostras), scale=st.sem(custoamostras))
    print("Número de Amostras: ", N)
    print("Média: ", media)
    print("Desvio padrao: ", desviopadrao)
   # print("Desvio padrão populacional: ", statistics.pstdev(custoamostras,mu=None))
    print("Nível de confiança: ", + alfa)
    print("Intervalo de confiança:", intervaloconfianca)
    #     # FIM do loop de simulação
#
print ("Dados " + str(vetorQnt))
#calcula percentual
for vetor in vetorQnt:
     vetorPerc[vetor] = int(vetorQnt[vetor]) / N
#
print("Quantidade de trechos utilizados: ",  vetorQnt)
print("Percentual de trechos utilizados: ", vetorPerc)

import numpy as np
import matplotlib.pyplot as plt
plt.style.use('seaborn-white')
data = custoamostras
n, bins, patches = plt.hist(data, bins='auto', alpha=0.1, histtype='stepfilled', color='blue', edgecolor='none',rwidth=0.85)
plt.ylabel('Frequencia')
plt.xlabel('Custos')
#plt.show()


#
# bins, patches = plt.hist(x=custoamostras.__len__(), bins='auto', color='#0504aa',
#                             alpha=0.7, rwidth=0.85)
# plt.grid(axis='y', alpha=0.75)
# plt.xlabel('Value')
# plt.ylabel('Frequency')
# plt.title('My Very Own Histogram')
# plt.text(23, 45, r'$\mu=15, b=3$')
# maxfreq = custoamostras.max()
# # Set a clean upper y-axis limit.
# plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
