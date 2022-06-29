import json
import definitions2 as defs2
import pandas as pd

df = pd.read_csv("CREA_procesado2.csv")

letras = [l for l in "abcdefghijklmnñopqrstuvwxyz"]

i = int(input("Número de letras: "))

expr = i * "."
print("\n" + expr)

df2 = df[[len(p) == i for p in df["palabra"]]]

with open("puntuaciones2a15.json") as f:
    s = f.read()    
    punts_init = json.loads(s)[str(i)]
    lst = sorted(list(punts_init.items()), reverse=True, key = lambda l: l[1])
    for punt in lst[:4]:
        print(punt)

not_guessed = True
n = 2
dfs = {1 : df2}

print("Teclee _fin_ para terminar o _reg_ para volver a escribir")

while not_guessed:
    print("-"*15, "\n")
    l = input("Letra elegida: \n> ")
    expr = input("Expresión: \n> ")
    if expr == "_reg_":
        continue
    
    if expr == "_fin_" or expr.count(".") == 0:
        break

    if not l in expr:
        df2 = df2[[(not l in p) for p in df2["palabra"]]]
    df2 = defs2.reduce_df(expr, df2, l)
    dfs[n] = df2
    letras.pop(letras.index(l))

    n += 1
    defs2.get_puntuations(expr, letras, df2)
    print(df2.head())
