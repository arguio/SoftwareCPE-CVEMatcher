import time, re

#Se declaran los directorios del fichero a leer (Comp(rimido)) y escribir (Ext(endido))
fn = 'C:/.../SoftwareCPEComp.txt'
filename = 'C:/.../SoftwareCPEExt.txt'

#Se lee el fichero fn
lines = open(fn, encoding="utf-8").read().split("\n")

start = time.time()

#Se recorre la lista de softwares mediante un for
length = len(lines)
for i in range(length):
    #Este if comprueba si hay algún CPE guardado (cada software tiene siempre 6 campos, si tiene más es porque hay algún CPE)
    if lines[i].split("|")[6:]:
        #Para eliminar caracteres no soportados, se codifica y decodifica la línea con el estándar cp1252 (ninguna razón en particular, es uno específico de Windows que da algún problema con caracteres raros que no aportan nada)
        line = lines[i].encode('cp1252','ignore').decode("cp1252")
        
        #Se vacía la línea actual, sus datos fueron guardados en la línea anterior en la variable line
        lines[i] = ""
        #Como dijimos, los 6 primeros campos de line son los que corresponden al software: tres publishers (original, filtrado y sacado del CPEUniqueList), dos name (original y filtrado) y un version
        software = line.split("|")[0:6]
        #Se sustituyen espacios al principio o al final de cada campo, y se vuelven a formatear todos juntos mediante |
        software = [re.sub(r'^\s+|\s+$', '', item) for item in software]
        software = "|".join(software)
        #Los CPEs se separan y ahora se creará un elemento nuevo de la lista global (lines) por cada CPE, con su software, que será el mismo
        cpes = line.split("|")[6:]
        order = 1
        for cpe in cpes:
            #Se añaden las líneas al final de la lista junto con un entero, order, que indicará qué CPE es el más parecido
            lines.append(software + "|" + str(order) + "|" + cpe)
            order += 1

print(time.time() - start)
#Se eliminan las líneas vacías, es decir todas las primeras, que vaciamos en la línea 21
lines = list(filter(None, lines))
print(time.time() - start)

#Se escribe la lista en el archivo de texto
with open(filename, 'w') as f:
    for item in lines:
        f.write("%s\n" % item)
        
print(time.time() - start)


########################################## SQL ##########################################


#Para conectarse a SQL se utiliza la libreria pyodbc
import pyodbc

#Se configura la conexión a la tabla, siempre que he ejecutado esto tenía abierto el SQL, no sé si funcionará sin hacerlo. Los valores que habría que modificar para conectarse a otra tabla sería solo el Database
conn = pyodbc.connect(r'Driver={SQL Server};'
                      r'Server=localhost;'
                      r'Database=Software;'
                      r'Trusted_Connection=yes;')

cursor = conn.cursor()

print(time.time() - start)

#Se da la orden de eliminar la tabla (después se creará de nuevo)
cursor.execute('DROP TABLE SoftwareCPE;')
#Se transmite esa orden
conn.commit()

#Se crea de nuevo la tabla
cursor.execute('CREATE TABLE SoftwareCPE (Vendor nvarchar(MAX), VendorFiltrado nvarchar(MAX), VendorOriginal nvarchar(MAX), ProductFiltrado nvarchar(MAX), ProductOriginal nvarchar(MAX), Version nvarchar(MAX), Orden tinyint, CPE nvarchar(MAX))')
conn.commit()

#Se realiza un bulk insert para subir el fichero de texto
cursor.execute('''
BULK INSERT SoftwareCPE
    FROM 'C:/.../SoftwareCPEExt.txt'
    WITH 
        (FIELDTERMINATOR = '|',
         ROWTERMINATOR = '\n')''')
conn.commit()

print(time.time() - start)

#Se cierra la conexión
cursor.close()
conn.close()
