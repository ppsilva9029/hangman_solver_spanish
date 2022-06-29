# %%
from pandas import DataFrame
from itertools import product
from math import log2
import multiprocessing as mp
#df = pd.read_csv("CREA_procesado2.csv")


# %%
def chk_l(l: str, expr: str):
    """Returns a boolean if the expresion is an undesirable combination
    
    Parameters
    ----------
    l : str
        The character of the combination
    expr : str
        The combination to be checked
        
    Returns
    -------
    bool
        If the comb is a undesirable expression
    """

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
def get_combs(expr: str, char : str):
    """Returns the possible combinations of a letter in a word using the cartesian product

    Parameters
    ----------
    expr : str
        A '.c...s' like expression in which the character char replace the dots
    char : str
    
    Returns
    -------
    list
        Of posible combinations that could match with words    
    """

    dots = expr.count(".")

    posible_chars = [char, "."]

    combs = product(posible_chars, repeat=dots)


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
    """Returns a regular expresion that matchs with the character in the places that aren't dots,
    but vowels match with their accentuated version in spanish (a, á)
    
    Parameters
    ----------
    char : str
    comb : comb
        A combination of an expresion
    """

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
    """Returns a regular expresion that matchs with the character in the places that aren't dots,
    a.a..a matches with amanda but not with aaaaaa
    
    Parameters
    ----------
    char : str
    comb : comb
        A combination of an expresion
    """
    
    r = ""
    for c in comb:
        
        if c == ".":
            r += f"(?!{char})."

        else:
            r += c
    
    return r
    
# get_regex_c("l", "g.il.")

# %%
def get_regex(char: str, comb: str) -> str:
    """A combination of get_regex_c and get_regex_v"""
    
    if char in "aeiou" and char != "":
        return get_regex_v(char, comb)

    else:
        return get_regex_c(char, comb)

#get_regex("s", "g.st..a")


# %%
def get_punt(args) -> float:

        """Obtains the punctuation of a given charcter, high scores means the letter brings more information
        
        Parameters
        ----------
        args : tuple
            a tuple of (char, expr, DataFrame)
            
            char : str
                the character to be tested in the DataFrame
            expr : str
                the current expression or information we have, something like 'a..s.t.'
            df : DataFrame
                The DataFrame in which we are going to test the character
        
        Returns
        -------
        float
            the punctuation of given information by a letter"""

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
            punt += (p * log2(1/p))


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

            info_bits = log2(1/p)

            punt += info_bits * p

        return punt



# %%
def get_puntuations(expr: str, letras: list, df: DataFrame):


    #df = df[[len(p) == len(expr) for p in df["palabra"]]]

    args_ = [(c, expr, df) for c in letras]

    with mp.Pool(mp.cpu_count() - 1) as p: # Modify this with the desired prossesors

        punts = p.map(get_punt, args_)

    lst = list(zip(letras, punts))

    #dic2 = {tup[0]: tup[1] for tup in lst}

    lst = sorted(lst, reverse=True, key = lambda l: l[1])
    for tup in lst[:4]:
        print(tup)

def reduce_df(expr : str, df : DataFrame, c: str) -> DataFrame:
    
    df2 = df[df["palabra"].str.match(get_regex_c(c, expr)) == True]
    return df2






