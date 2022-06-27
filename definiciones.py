# -*- coding: utf-8 -*-

import pandas as pd
from itertools import product
# from math import log2
import numpy as np
# from numba import jit
import json

df = pd.read_csv("CREA_procesado2.csv")

# tamano = 9

# f = [len(p) == tamano for p in df["palabra"]]

# df_fbl = df[f]

# df_fbl

def chk_l(l: str, expr: str):

    if l in "aeiou":
        dic = {
            "a": "á",
            "e": "é",
            "i": "í",
            "o": "ó",
            "u": "ú"
        }
        ocurrencias = expr.count(l) + expr.count(dic[l])

    else:
        ocurrencias = expr.count(l)
    if ocurrencias / len(expr) > 0.56 or (l*3 in expr):
        return True

    return False


def get_combs(expr: str, char):
    '''
    Obtiene las posibles coincidencias de una letra en una palabra
    '''

    underls = expr.count("_")

    posible_chars = [char, "."]

    combs = product(posible_chars, repeat=underls)


    exps = []

    for comb in combs:

        myGen = (elem for elem in comb)
        p = ""

        for i, c in enumerate(expr):
            if c == "_":
                p += next(myGen)
            else:
                p += expr[i]

        if len(expr) > 7 and chk_l(char, p): continue
        exps.append(p)
        

    return exps

# print(len(get_combs("_"*20, "l")))

def get_regex_v(char: str, comb: str):

    dic = {
            "a": "á",
            "e": "é",
            "i": "í",
            "o": "ó",
            "u": "ú"
        }

    r = ""
    for c in comb:
        
        if c == ".":
            r += f"(?!{char}|{dic[char]})."

        elif c == char:
            r += f"[{char}{dic[char]}]"
        else:
            r += c
    
    return r

# get_regex_v("a", "g.aia.")

def get_regex_c(char: str, comb: str):
    
    r = ""
    for c in comb:
        
        if c == ".":
            r += f"(?!{char})."

        else:
            r += c
    
    return r
    
# get_regex_c("l", "g.il.")

def get_regex(char: str, comb: str):
    
    if char in "aeiou":
        return get_regex_v(char, comb)

    else:
        return get_regex_c(char, comb)

# get_regex("s", "g.st..a")

def get_punt(char: str, expr: str, df: pd.DataFrame):

        combs = get_combs(expr, char)

        rows = len(df.index)

        punt = 0
        for comb in combs:
            
            regx = get_regex(char, comb)

            df2 = df[df["palabra"].str.match(regx) == True]

            reduced_rows = len(df2.index)

            p = reduced_rows / rows

            if p == 0:
                continue

            info_bits = np.log2(1/p)

            punt += info_bits * p

        return punt

# get_punt("a", "________", df_fbl)
'''
dic = {}

for i in range(15, 18):

    tamano = i

    f = [len(p) == tamano for p in df["palabra"]]

    df_fbl = df[f]

    f2 = [not ("'" in p) for p in df_fbl["palabra"]]

    df_fbl = df_fbl[f2]

    punts = []

    for c in "abcdefghijklmnñopqrstuvwxyz":

        punt = get_punt(c, "_"*tamano, df_fbl)

        punts.append((c, punt))

    dic[i] = punts




dic_def = {}

for i in range(14, 15):
    d = {lst[0]:lst[1] for lst in dic[i]}

    dic_def[i] = d

s = json.dumps(dic_def, indent=4)

with open("puntuaciones6.json", "w") as f:
    f.write(s)

'''
