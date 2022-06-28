import json
import definitions2 as defs2
import pandas as pd

df = pd.read_csv("CREA_procesado2.csv")

letras = [l for l in "abcdefghijklmnñopqrstuvwxyz"]

expr = int(input("Número de letras: ")) * "."

with open("puntuaciones2a15.json") as f:
    s = f.read()    
    punts_init = json.loads(s)[str(len(expr))]
    lst = sorted(list(punts_init.items()), reverse=True, key = lambda l: l[1])
    for punt in lst:
        print(punt)
