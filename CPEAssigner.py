import re, time, pickle, os, itertools, torch, logging
import pandas as pd
from difflib import SequenceMatcher
import multiprocessing as mp
import numpy as np

#Se declaran algunas variables que serán globales
vendor = ""
filepath = 'C:/.../CVE-NIST/officialCPEdictionary_v2.3.txt'
cpe = pd.read_csv(filepath, dtype = str, names=["title", "lang", "cpe23uri", "Part", "Vendor", "Product", "Version", "Update_sw", "Edition", "Language", "SW_Edition", "Target_SW", "Target_HW", "Other", "Autonumber"], sep='|', encoding='latin-1')

#fn es el fichero donde se guardará la lista de software
fn = 'C:/.../SoftwareCPEComp.txt'

#Como pasaba en NuevoFiltradoSoftware.py, se carga la lista de CPEs únicos
with open('C:/.../UniqueCPEVendor.txt', encoding="utf-8") as f:
    cpeuniquelist = f.readlines()
cpeuniquelist = [x.strip() for x in cpeuniquelist]

# torch.set_num_threads(1)
#Se obtiene el logger, que podrá emitir mensajes de warning, error...
logger = mp.get_logger()

#CPEFinder es la función que seleccionará los CPEs más parecidos al software dado
def CPEFinder(key, q):
    global vendor, cpe, df_mask, cpeuniquelist
    #Si el vendor que se usó anteriormente es el mismo que el nuevo, se ahorra el paso de buscar el que sea más parecido
    if (key.split('|')[0] != vendor):
        #El primer campo de key será vendor
        vendor = key.split('|')[0]
        #Creo una máscara en la que sean True todas las filas en las que el vendor sea el del software, y la aplico al dataframe para obtener uno más pequeño y más manejable
        mask = cpe['Vendor'].str.contains('^' + vendor, case=False)
        df_mask = list(cpe[mask]['cpe23uri'])
        #Esta parte se podría eliminar, ver Guía.txt, pero hace lo que ya se hacía en NuevoFiltradoSoftware.py: buscar el publisher más parecido de la lista cpeuniquelist
        if not df_mask:
            logger.warning("escribo")
            closestvendor = sorted(cpeuniquelist, key=lambda x: SequenceMatcher(None, x, key.split('|')[0]).quick_ratio(), reverse=True)[0]
            mask = cpe['Vendor'].str.contains('^' + closestvendor, case=False)
            df_mask = list(cpe[mask]['cpe23uri'])
    
    # software = " ".join(set((re.sub(r" +", " ", key.replace("|", " "))).split()))
    #Se cogen todas las palabras únicas juntando todos los campos y se ponen en un string separadas por espacios
    software = " ".join(list(dict.fromkeys((re.sub(r" +", " ", key.replace("|", " "))).split())))
    #Se buscan los 20 CPEs más parecidos al software
    results = sorted(df_mask, key=lambda x: SequenceMatcher(None, x, software).quick_ratio(), reverse=True)[:20]
    #Se guarda el software junto con los CPEs unidos por |
    str_soft = r"" + key + "|" + "|".join(results)
    #Se envía el software para que listener lo escriba a un archivo de texto
    q.put(str_soft)
    #logger.warning("Devuelvo" + key)
    return str_soft

#listener espera a que CPEFinder devuelva el software para escribirlo a archivo
def listener(q):
    #Abre el fichero de texto y espera constantemente para poder escribir
    with open(fn, 'w', encoding="utf-8") as f:
        while 1:
            try:
                #Obtiene lo que le puedan haber mandado
                m = q.get()
                #Si el mensaje es kill (palabra arbitraria) será porque el programa ha acabado
                if m == 'kill':
                    #logger.warning("Salgo")
                    #f.write('killed')
                    break
                #Se escribe al archivo de texto
                f.write(str(m) + '\n')
                # logger.warning("escribo")
                f.flush()
            except Exception:
                import sys, traceback
                #print('Whoops! Problem:', file=sys.stderr)
                #logger.warning("ERROR")
                traceback.print_exc(file=sys.stderr)

def main():
    
    #Se carga el fichero de software filtrado y se guarda en un dataframe, sustituyendo, como hemos hecho anteriormente, NaN por espacios vacíos
    filepathread = 'C:/.../SoftwareFiltradoGeneral.csv'
    df_read = pd.read_csv(filepathread, dtype = str, names=['publisher','publisher_filtrado','publisher_original','name','name_original','version'], sep='|', encoding='latin-1')
    df_read = df_read.replace(np.nan, '', regex=True)
    
    #Para cada fila, se juntan todos los campos del dataframe y se unen con |
    list_read = (df_read.agg('|'.join, axis=1)).to_list()
    
    #Esto son pruebas con distintos métodos de hacer lo mismo. Probablemente no funcionen pero los dejo por si se pueden aprovechar
    # a_file = open(r"df_read.pkl", "wb")
    # pickle.dump(df_read, a_file)
    # a_file.close()
    
    # mp.log_to_stderr()
    # logger = mp.get_logger()
    # logger.setLevel(logging.WARNING)
    
    # a_file = open(r"C:\Users\Alejandro Perales\.spyder-py3\data.pkl", "rb")
    # df_dict = pickle.load(a_file)
    # a_file.close()
    
    # df_dict = df_dict.fromkeys(df_dict, "") #RESETEAR VALUES A ""
    # df_dict_extract = dict(itertools.islice(df_dict.items(), 3600))
    
    #Se configura el multiprocesado, con un manager, una cola y un pool, en el que se especificará el número de procesos, que al no especificarse se utilizará el valor por defecto, 4
    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool()#pool = mp.Pool(mp.cpu_count() + 2)
    
    #Se configura el listener
    watcher = pool.apply_async(listener, (q,))
    
    start = time.time()
    
    #Cada software se asigna a un trabajo, que CPEFinder irá desempeñando por orden
    jobs = []
    for i in list_read:
        job = pool.apply_async(CPEFinder, (i, q))
        jobs.append(job)
    
    for job in jobs:
        job.get()
        
    #Una vez acabados todos los trabajos se pone fin al listener y se espera a que acabe
    q.put('kill')
    pool.close()
    pool.join()
    # watcher.join()
    
    print(time.time() - start)
    
    # f = open("demofile2.txt", "a")
    # f.close()
    
    # pool = Pool(processes=2)
    # # result = pool.map(CPEFinder,df_dict_extract)
    # result2 = pool.map_async(CPEFinder,df_dict_extract, f, chunksize = 10) #starmap para mas argumentos
    # #a = result2.get()

if __name__ == '__main__':
    main()
