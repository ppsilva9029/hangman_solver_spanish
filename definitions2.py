# %%
import pandas as pd
from itertools import product
# from math import log2
import time
import numpy as np
import json
import multiprocessing as mp
df = pd.read_csv("CREA_procesado2.csv")


# %%
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


# %%
def get_combs(expr: str, char):
    '''
    Obtiene las posibles coincidencias de una letra en una palabra
    '''

    underls = expr.count(".")

    posible_chars = [char, "."]

    combs = product(posible_chars, repeat=underls)


    exps = []

    for comb in combs:

        myGen = (elem for elem in comb)
        p = ""

        for i, c in enumerate(expr):
            if c == ".":
                p += next(myGen)
            else:
                p += expr[i]

        if len(expr) > 7 and chk_l(char, p): continue
        exps.append(p)
        

    return exps

#print(len(get_combs("."*20, "l")))


# %%
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

# %%
def get_regex_c(char: str, comb: str):
    
    r = ""
    for c in comb:
        
        if c == ".":
            r += f"(?!{char})."

        else:
            r += c
    
    return r
    
# get_regex_c("l", "g.il.")

# %%
def get_regex(char: str, comb: str):
    
    if char in "aeiou" and char != "":
        return get_regex_v(char, comb)

    else:
        return get_regex_c(char, comb)

get_regex("s", "g.st..a")


# %%
def get_punt(args):

        char, expr, df = args

        # posible combinations of the letter in the expresion
        combs = get_combs(expr, char)

        # original rows of the dataframe
        rows = len(df.index)

        punt = 0

        # Get the puntuation for the combination "_______"
        regx = get_regex(char, len(expr)*".")
        df2 = df[df["palabra"].str.match(regx) == True]
        p = len(df2.index) / rows

        if p != 0:
            punt += (p * np.log2(1/p))


        if char in "aeiou":
            vocals = {
                "a":"á",
                "e":"é",
                "i":"í",
                "o":"ó",
                "u":"ú"
            }

            df = df[[(char in p or vocals[char] in p) for p in df["palabra"]]]
        else:
            df = df[[char in p for p in df["palabra"]]]
        
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



# %%
def get_puntuations(expr: str, letras: str, df: pd.DataFrame):

    df = df[[len(p) == len(expr) for p in df["palabra"]]]

    args_ = [(c, expr, df) for c in letras]

    with mp.Pool(6) as p:

        punts = p.map(get_punt, args_)


    lst = list(zip(letras, punts))

    dic2 = {tup[0]: tup[1] for tup in lst}

    lst = sorted(list(dic2.items()), reverse=True, key = lambda l: l[1])
    print(lst[:3])


letras = [l for l in "abcdefghijklmnñopqrstuvwxyz"]



