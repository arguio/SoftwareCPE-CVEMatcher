import os, pyodbc, pandas as pd, re, time

path = r'C:\Users\Alejandro Perales\Downloads\CVE-NIST'

#Se hace un listado de todos los documentos de texto que hay en el directorio path
files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.txt' in file:
            files.append(os.path.join(r, file))

#Se configura la conexión a la base de datos de SQL
conn = pyodbc.connect(r'Driver={SQL Server};'
                      r'Server=localhost;'
                      r'Database=Software;'
                      r'Trusted_Connection=yes;')
cursor = conn.cursor()

cursor.execute('DROP TABLE CVE;')
conn.commit()

cursor.execute('CREATE TABLE CVE (ID varchar(MAX), Year SMALLINT, Part varchar(MAX), Vendor varchar(MAX), Product varchar(MAX), Version varchar(MAX), V3ImpactScore varchar(MAX), V2ImpactScore varchar(MAX), PublishedDate DATE, ModifiedDate DATE, Description varchar(MAX), ProblemType varchar(MAX), V3ExploitabilityScore varchar(MAX), V3Vectorvarchar varchar(MAX), V3AttackVector varchar(MAX), V3AttackComplexity varchar(MAX), V3PrivilegesRequired varchar(MAX), V3UserInteraction varchar(MAX), V3Scope varchar(MAX), V3ConfidentialityImpact varchar(MAX), V3IntegrityImpact varchar(MAX), V3AvailabilityImpact varchar(MAX), V3BaseScore varchar(MAX), V3BaseSeverity varchar(MAX), V2ExploitabilityScore varchar(MAX), V2Vectorvarchar varchar(MAX), V2AccessVector varchar(MAX), V2AccessComplexity varchar(MAX), V2Authentication varchar(MAX), V2ConfidentialityImpact varchar(MAX), V2IntegrityImpact varchar(MAX), V2AvailabilityImpact varchar(MAX), V2BaseScore varchar(MAX), V2ObtainAllPrivilege varchar(MAX), V2ObtainUserPrivilege varchar(MAX), V2ObtainOtherPrivilege varchar(MAX), V2UserInteractionRequired varchar(MAX), Dependency varchar(MAX), DependConfig varchar(MAX), Subconfig INT, cpeVulnerable varchar(MAX), cpe23uri varchar(MAX), Update_sw varchar(MAX), Edition varchar(MAX), Language varchar(MAX), SW_Edition varchar(MAX), Target_SW varchar(MAX), Target_HW varchar(MAX), Other varchar(MAX), Assigner varchar(MAX), DBUpdated DATE)')
conn.commit()

#Para cada fichero se realiza un bulk insert y se suben los datos a la tabla
for f in files:
    # with open(f,'r') as file:
    #     filedata = file.read()
    #     # filedata = re.sub(r"(\d),(?=\d)", "$1.", filedata)
    #     # filedata = filedata.replace('|$','|')
    # with open(f,'w') as file:
    #     file.write(filedata)
    
    print("Subiendo " + f)
    cursor.execute('''BULK INSERT CVE
                   FROM "''' + f + '''"
                   WITH 
                       (FIRSTROW = 2,
                        FIELDTERMINATOR = '|',
                        ROWTERMINATOR = '\n')''')
    conn.commit()

#Se prueba a parsear a float varias columnas que tenían una coma decimal
cursor.execute('''UPDATE CVE
SET CVE.V2ImpactScore=(TRY_PARSE( CVE.V2ImpactScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V3ImpactScore=(TRY_PARSE( CVE.V3ImpactScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V3ExploitabilityScore=(TRY_PARSE( CVE.V3ExploitabilityScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V3BaseScore=(TRY_PARSE( CVE.V3BaseScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V2ExploitabilityScore=(TRY_PARSE( CVE.V2ExploitabilityScore AS NUMERIC(4,2) USING 'El-GR' )),
CVE.V2BaseScore=(TRY_PARSE( CVE.V2BaseScore AS NUMERIC(4,2) USING 'El-GR' ))''')
conn.commit()

cursor.close()
conn.close()