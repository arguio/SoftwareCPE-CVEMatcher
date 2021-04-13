import re, time, pickle
import pandas as pd
import numpy as np
from difflib import SequenceMatcher

#Cargo el fichero officialCPEdictionary_v2 al dataframe cpe
filepath = 'C:/Users/Alejandro Perales/Documents/CVE-NIST/officialCPEdictionary_v2.3.txt'
cpe = pd.read_csv(filepath, dtype = str, names=["title", "lang", "cpe23uri", "Part", "Vendor", "Product", "Version", "Update_sw", "Edition", "Language", "SW_Edition", "Target_SW", "Target_HW", "Other", "Autonumber"], sep='|', encoding='latin-1')

#Paso la columna vendor a lista
cpelist = cpe['Vendor'].values.tolist()

#Elimino duplicados
cpeunique = list(set(cpelist[1:]))

#Sustituyo barras simples por dobles
cpeunique = [w.replace('\\','\\\\') for w in cpeunique]

#Ordeno alfabéticamente (no es necesario)
cpeunique.sort()

#Exporto a archivo
with open('UniqueCPEVendor.txt', 'w') as f:
    for item in cpeunique:
        re.compile(item)
        f.write("%s\n" % item)