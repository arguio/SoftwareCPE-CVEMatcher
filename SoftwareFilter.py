import re, fileinput, pandas as pd, numpy as np, time
from difflib import SequenceMatcher

#Cargo el fichero de texto
filepath = 'C:/.../MAES_Software2.csv'

#Elimino comillas
with fileinput.FileInput(filepath, inplace=True, backup='.bak') as file:
    for line in file:
        print(line.replace("\"", ""), end='')
        
#Guardo en dataframe
df = pd.read_csv(filepath, dtype = str, names=["name", "publisher", "version"], sep='|', encoding='latin-1')
#Sustituyo NaN (Not a Number) por espacios vacíos
df = df.replace(np.nan, '', regex=True)

#df.publisher
df_sorted = df.sort_values(by=['publisher', 'name'])
#df_sorted = df.drop_duplicates()

#Duplico la columna name en name_original
df_sorted['name_original'] = df_sorted['name']

#Escapo los caracteres especiales
df_sorted['name_original'] = [str(x).replace(r'\\', '\\\\') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('^','\^') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('$','\$') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('.','\.') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('|','\|') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('?','\?') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('*','\*') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('+','\+') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('(','\(') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace(')','\)') for x in df_sorted['name_original']]
df_sorted['name_original'] = [str(x).replace('[','\[') for x in df_sorted['name_original']]
df_sorted['publisher_original'] = df_sorted['publisher']

#Ordeno las columnas
df_sorted = df_sorted[["publisher", "publisher_original", "name", "name_original", "version"]]

#A partir de aquí filtro y elimino palabras redundantes
df_sorted['name'] =  [re.sub(r' corporation$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r' inc\.?(orporated)?$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r' technologies$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r' corporation$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['publisher'] =  [re.sub(r'\\Status Monitor$','', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]
df_sorted['publisher'] =  [re.sub("[^a-zA-Z' ]+", '', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]
df_sorted['publisher'] =  [re.sub("^ $", '', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]

df_sorted['publisher'] =  [re.sub(r' ?inc\.?(orporated)?$|corp\.?(oration)?|\bsoftware|tech\.?(nolog.*?\b)|ltd\.?|limited|group','', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]

df_sorted['publisher'] =  [re.sub(r'^ ','', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]
df_sorted['publisher'] =  [re.sub(r'^The ','', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]
df_sorted['publisher'] =  [re.sub(r' Project$','', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]
#df_sorted['publisher'] =  [re.sub(r'\d+(\.\d+)+','', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]
df_sorted['publisher'] =  [re.sub(r',','', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher']]
#df_sorted['name'] =  [re.sub(r'v?\d+(\.\d+)+| #\d+','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
#df_sorted['name'] =  [re.sub(r'\(\d\d/\d\d/\d\d\d\d ?\)','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Chinese Standard|Chinese Traditional|Czech|Danish|Dutch|English|Finnish|French|German|Greek|Hungarian|Italiano?|Japanese|Korean|Norwegian|Polish|Portuguese (Brazil)|Portugu.se?|Russian|Spanish|Swedish|Thai|Turkish|Basque|Catalan|Galician|Arabic|Nederlands|Espa.ol|Fran.ais|Deutsch','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'\(\)|\?| - ,','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
#df_sorted['name'] =  [re.sub(r'\b20\d\d\b','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'\(.*\)','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]

df_sorted['name'] =  [re.sub(r'\(?x?64.?bits?\)?|\(?x?64(.?bit)?\)?','64', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'\(?x?86.?bits?\)?|\(?x?86(.?bit)?\)?','86', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'\(?x?32.?bits?\)?|\(?x?32(.?bit)?\)?','32', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]

df_sorted['name'] =  [re.sub(r' for ',' ', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r' {2,}',' ', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r' $|^ |.*%.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r' edition$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'\|','&amp', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
prev_shape = 0
df_sorted['name'] = [re.sub(r'\bedition.?\b|\bprofessional\b|\bsprint\b|\bplus\b|\bcorporate\b|\bstandard\b|\bprofessional\b|\bpro\b|\bpremium\b|\bplugin$| support\b|\bstudio\b|\btool.\b','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
    
df_sorted['name'] =  [re.sub(r'^ ','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]

#df_sorted = df_sorted.drop_duplicates()

#######################################


df_sorted['name'] =  [re.sub(r'.*desinst.*|.*uninstall.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'(?<=CorelDRAW Graphics Suite X.)(.*)','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'CorelDRAW Home & Student Suite.*','CorelDRAW Home & Student Suite', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'^[A0-Za-z]+_help$|_Software_Min$|_Sw_Min$|_readme$|_edocs$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'-? ?series.*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'registro de usuario de |manual de usuario |manual de red (de )?','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
#df_sorted['name'] =  [re.sub(r' \d+$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'^Catalyst Control Center.*','Catalyst Control Center', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Canon M[A0-Za-z]+$','Canon MX000', str(x), flags=re.IGNORECASE) for x in df_sorted['name']] #x es letra y X es número
df_sorted['name'] =  [re.sub(r'.*agregar o quitar.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'.*aplicac.*|.*paquete.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]

df_sorted['name'] =  [re.sub(r'7-Zip.*','7-Zip', str(x), flags=re.IGNORECASE) for x in df_sorted['name']] #SE PODRÍA QUITAR PERO LO DEJO PORQUE LO ÚNICO QUE QUITABA ERA LA VERSIÓN, PERO ESTA ESTÁ GUARDADA EN EL CAMPO 'VERSION' TAMBIÉN
df_sorted['name'] =  [re.sub(r'ABBYY FineReader.*','ABBYY FineReader', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'ACDSee.*','ACDSee', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Acer eDisplay.*','Acer eDisplay', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Acronis True Image.*','Acronis True Image', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'herramienta.*|.*actualizac.*|administrac.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Adobe Premier.*','Adobe Premiere', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Altair HyperWorks.*','Altair HyperWorks', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'AMD Catalyst.*','AMD Catalyst', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'.*setting.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Android.*','Android SDK', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'Apache Tomcat.*','Apache Tomcat', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'ApexSQL.*','ApexSQL', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'ArcGIS Data Interoperability.*','ArcGIS Data Interoperability Desktop', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'ArcGIS Desktop.*','ArcGIS Desktop', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'ArcGIS Server.*','ArcGIS Server', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'ArcGIS Web Adaptor.*','ArcGIS Web Adaptor', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'.*install(er)?\b.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'.*asesor.*|.*asistente.*|.*Accesos.*|.*Administrador.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'ASUS GPU Tweak.*','ASUS GPU Tweak', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
df_sorted['name'] =  [re.sub(r'.*AutoCAD.*','AutoCAD', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]
#df_sorted = df_sorted.drop_duplicates()
#df_sorted = df_sorted.drop_duplicates(subset='name')

# Adobe

mask = df_sorted['publisher'].str.contains('^Adobe', case=False)
df_sorted_adobe = df_sorted[mask]
df_sorted_not_adobe = df_sorted[~mask]

df_sorted_adobe['publisher'] = "Adobe"
df_sorted_adobe['name'] =  [re.sub(r'CC.*| CS.*| CP.*','', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r',.*|-.*|NPAPI|PPAPI','', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r' \d+.*','', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Acrobat.*','Adobe Acrobat', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Color.*','Adobe Color', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Bridge.*','Adobe Bridge', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Captivate.*','Adobe Captivate', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Creative Suite.*','Adobe Creative Suite', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Common File Installer.*','', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Flash.*','Adobe Flash', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Help.*','', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Lightroom.*','Adobe Lightroom', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Media.*','Adobe Media', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe PDF.*','Adobe PDF', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Photoshop.*','Adobe Photoshop', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Premiere.*','Adobe Premiere', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Reader.*','Adobe Reader', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe Type.*','Adobe Type', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'Adobe�? Content Viewer.*','Adobe Content Viewer', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'AdobeColor.*','Adobe Color', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r' {2,}|_',' ', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r' $|^ ','', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted_adobe['name'] =  [re.sub(r'^(?!(Adobe Acrobat|Adobe After Effects|Adobe AIR|Adobe Animate|Adobe Audition|Adobe Bridge|Adobe Camera Raw|Adobe Captivate|Adobe Character Animator|Adobe CMaps|Adobe CMM|Adobe Color|Adobe Content Viewer|Adobe Creative Cloud|Adobe Creative Suite|Adobe Device Central|Adobe Dimension|Adobe Dreamweaver|Adobe Drive|Adobe Dynamiclink|Adobe eLearning Suite|Adobe Encore|Adobe ExtendScript Toolkit|Adobe Fireworks|Adobe Flash|Adobe FrameMaker|Adobe Glyphlet Creation Tool|Adobe Illustrator|Adobe InDesign|Adobe Lightroom|Adobe Linguistics|Adobe LiveCycle Designer ES4|Adobe Media|Adobe MotionPicture Color Files|Adobe Muse|Adobe OnLocation|Adobe Output Module|Adobe PageMaker|Adobe PDF|Adobe Photoshop|Adobe Prelude|Adobe Premiere|Adobe Reader|Adobe SGM|Adobe Shockwave Player|Adobe SING|Adobe Soundbooth|Adobe Stock Photos|Adobe SVG Viewer|Adobe Type|Adobe Ultra|Adobe Video Profiles|Adobe WAS|Adobe Widget Browser)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_adobe['name']]
df_sorted = pd.concat([df_sorted_adobe,df_sorted_not_adobe])

#df_sorted = df_sorted.drop_duplicates()
#df_sorted = df_sorted.drop_duplicates(subset='name')
del df_sorted_adobe,df_sorted_not_adobe

# HP

mask = (df_sorted['publisher'].str.contains('Hewlett', case=False)) | df_sorted['name'].str.contains('HP') | df_sorted['publisher'].str.contains('.*HP.*')
df_sorted_hp = df_sorted[mask]
df_sorted_not_hp = df_sorted[~mask]

df_sorted_hp['publisher'] = "HP"
#df_sorted_hp['name'] =  [re.sub(r'.*\d\d.*','', str(x), flags=re.IGNORECASE) for x in df_sorted_hp['name']]
df_sorted_hp['name'] =  [re.sub(r'HP Display.*','HP Display Control', str(x), flags=re.IGNORECASE) for x in df_sorted_hp['name']]
df_sorted_hp['name'] =  [re.sub(r'HP JumpStart.*','HP JumpStart', str(x), flags=re.IGNORECASE) for x in df_sorted_hp['name']]
df_sorted_hp['name'] =  [re.sub(r'HP Photo and Imaging.*','HP Photo and Imaging', str(x), flags=re.IGNORECASE) for x in df_sorted_hp['name']]
df_sorted_hp['name'] =  [re.sub(r'HP Print.*','HP Print', str(x), flags=re.IGNORECASE) for x in df_sorted_hp['name']]
df_sorted_hp['name'] =  [re.sub(r'^(?!(Enterprise|HP 3D DriveGuard|HP Client Security Manager|HP Color Laser|HP Connection Optimizer|HP DesignJet Utility|HP Deskjet|HP Device Access Manager|HP Display Control|HP Documentation|HP EmailSMTP|HP ENVY|HP ePrint|HP Hotkey|HP Image Zone|HP Imaging Device Functions|HP JumpStart|HP MFP Scan|HP My Display|HP MyRoom|HP OneDrive|HP PageWide|HP Performance Advisor|HP Photo and Imaging|HP Photo Creations|HP Photosmart|HP Print|HP Recovery Manager|HP Registration Service|HP Scan|HP Scanjet|HP Smart Document Scan Software|HP Smart Web Printing|HP Solution Center|HP Sure Click|HP Sure Recover|HP Sure Run|HP Velocity|Insight Diagnostics|MarketResearch|Smart Storage Administrator)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_hp['name']]
#df_sorted_hp = df_sorted_hp.drop_duplicates()

#df_sorted_hp['name_2'] = df_sorted_hp['name'].str.strip()
#df_sorted_hp['name_2'] = df_sorted_hp['name'].str.lower()
#df_sorted_hp = df_sorted_hp.drop_duplicates(subset=['name_2'])
#df_sorted_hp = df_sorted_hp.drop(columns = 'name_2')

df_sorted = pd.concat([df_sorted_hp,df_sorted_not_hp])
#df_sorted = df_sorted.drop_duplicates(subset='name')
df_sorted['name'].loc[df_sorted['publisher'].str.contains('^hp$')] =  [re.sub(r'.*','', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('^hp$')]]
del df_sorted_hp,df_sorted_not_hp

# Autodesk

mask = df_sorted['publisher'].str.contains('^Autodesk', case=False)
df_sorted_autodesk = df_sorted[mask]
df_sorted_not_autodesk = df_sorted[~mask]

df_sorted_autodesk['name'] =  [re.sub(r'Autodesk Navisworks.*','Autodesk Navisworks', str(x), flags=re.IGNORECASE) for x in df_sorted_autodesk['name']]
df_sorted_autodesk['name'] =  [re.sub(r'^FormIt.*','FormIt', str(x), flags=re.IGNORECASE) for x in df_sorted_autodesk['name']]
df_sorted_autodesk['name'] =  [re.sub(r'^(?!(A360 Desktop|AutoCAD|Autodesk 3ds Max|Autodesk App Manager|Autodesk Backburner|Autodesk CAD Manager|Autodesk Design Review|Autodesk Download Manager|Autodesk DWF Viewer|Autodesk DWG TrueView|Autodesk Express Viewer|Autodesk Infrastructure Administrator|Autodesk Inventor|Autodesk Navisworks|Autodesk ReCap|Autodesk Revit|Autodesk Showcase|Autodesk Single Sign On Component|Autodesk Storm and Sanitary Analysis|Autodesk Sync|Autodesk Vault Basic|Autodesk Vehicle Tracking Core|Autodesk Workflows|Dynamo|FormIt)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_autodesk['name']]

df_sorted = pd.concat([df_sorted_autodesk,df_sorted_not_autodesk])
#df_sorted = df_sorted.drop_duplicates(subset='name')
del df_sorted_autodesk,df_sorted_not_autodesk

# Brother

mask = (df_sorted['name'].str.contains('.*Brother.*', case=False)) | (df_sorted['publisher'].str.contains('.*Brother.*', case=False))
df_sorted_brother = df_sorted[mask]
df_sorted_not_brother = df_sorted[~mask]
df_sorted_brother['publisher'] = "Brother"
df_sorted_brother['name'] =  [re.sub(r'^(?!(Brother BRAdmin|Brother CanvasWorkspace|Brother iPrint&Scan|Brother MFL-Pro Suite|Brother P-touch Software|Brother Software Suite|StatusMonitor|UsbRepairTool)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_brother['name']]
df_sorted = pd.concat([df_sorted_brother,df_sorted_not_brother])
#df_sorted = df_sorted.drop_duplicates(subset='name')
del df_sorted_brother,df_sorted_not_brother

# Canon

mask = (df_sorted['name'].str.contains('.*Canon.*', case=False)) | (df_sorted['publisher'].str.contains('.*Canon.*', case=False))
df_sorted_canon = df_sorted[mask]
df_sorted_not_canon = df_sorted[~mask]
df_sorted_canon['publisher'] = "Canon"
df_sorted_canon['name'] =  [re.sub(r'.*Camera Window.*','Camera Window', str(x), flags=re.IGNORECASE) for x in df_sorted_canon['name']]
df_sorted_canon['name'] =  [re.sub(r'.*CaptureOnTouch.*','CaptureOnTouch', str(x), flags=re.IGNORECASE) for x in df_sorted_canon['name']]
df_sorted_canon['name'] =  [re.sub(r'^(?!(Camera Window|Canon CanoScan Toolbox|Canon CAPT Print Monitor|Canon Easy-PhotoPrint|Canon Easy-WebPrint EX|Canon IJ Network Tool|Canon IJ Printer Assistant Tool|Canon IJ Scan Utility|Canon Inkjet Printer Driver Add-On Module|Canon Lite Driver|Canon MF Scan Utility|Canon MOV Decoder|Canon MOV Encoder|Canon MP Navigator|Canon MX000|Canon My Image Garden|Canon My Printer|Canon PhotoRecord|Canon Print|Canon RAW Image TaskZoomBrowser EX|Canon Scanner Management Agent|Canon Solution Menu EX|Canon ZoomBrowser EX|CaptureOnTouch|CapturePerfect|Color Network ScanGear|IJ Network Device Setup Utility|Internet Library|MovieEdit Task|PhotoStitch|RAW Image Task|RemoteCapture Task|ScanFront administration tool|Scanner Wireless Connection Utility)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_canon['name']]
#df_sorted_canon = df_sorted_canon.drop_duplicates(subset='name')
df_sorted = pd.concat([df_sorted_canon,df_sorted_not_canon])
del df_sorted_canon,df_sorted_not_canon

# Citrix

mask = (df_sorted['name'].str.contains('.*Citrix.*', case=False)) | (df_sorted['publisher'].str.contains('.*Citrix.*', case=False))
df_sorted_citrix = df_sorted[mask]
df_sorted_not_citrix = df_sorted[~mask]
df_sorted_citrix['publisher'] = "Citrix"
df_sorted_citrix['name'] =  [re.sub(r'.*Citrix HDX.*','Citrix HDX', str(x), flags=re.IGNORECASE) for x in df_sorted_citrix['name']]
df_sorted_citrix['name'] =  [re.sub(r'^(?!(Citrix AD Identity Service|Citrix Analytics|Citrix AppDisk VDA|Citrix Authentication Manager|Citrix Diagnostics Facility|Citrix Director|Citrix HDX|Citrix Identity Assertion VDA|Citrix Personalization AppV -|Citrix Receiver|Citrix Remote Broker Provider -|Citrix Screen CastingWindows|Citrix StoreFront|Citrix Universal Print Client|Citrix WMI Proxy|Citrix Workspace|Citrix XenApp|Citrix XenCenter)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_citrix['name']]
#df_sorted_citrix = df_sorted_citrix.drop_duplicates(subset='name')
df_sorted = pd.concat([df_sorted_citrix,df_sorted_not_citrix])
del df_sorted_citrix,df_sorted_not_citrix

# Microsoft

mask = (df_sorted['publisher'].str.contains('.*Microsoft.*', case=False))
df_sorted_microsoft = df_sorted[mask]
df_sorted_not_microsoft = df_sorted[~mask]
df_sorted_microsoft['publisher'] = "Microsoft"
df_sorted_microsoft['name'] =  [re.sub(r'^Hotfix.*','Hotfix', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft .NET Core.*','Microsoft .NET Core', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Access.*','Microsoft Access', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Advertising.*','Microsoft Advertising', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Application.*','Microsoft Application', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft ASP.NET.*','Microsoft ASP.NET', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Azure.*','Microsoft Azure', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Device Emulator.*','Microsoft Device Emulator', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Document.*','Microsoft Document', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Edge.*','Microsoft Edge', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft HEVC Media Extension.*','Microsoft HEVC Media Extension', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office Excel.*','Microsoft Office Excel', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office OneNote.*','Microsoft Office OneNote', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office OSM.*','Microsoft Office OSM', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office Outlook.*','Microsoft Office Outlook', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office PowerPoint.*','Microsoft Office PowerPoint', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office Publisher.*','Microsoft Office Publisher', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office Server.*','Microsoft Office Server', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office Shared.*','Microsoft Office Shared', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office SharePoint.*','Microsoft Office SharePoint', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office Web Apps.*','Microsoft Office Web Apps', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Office Word.*','Microsoft Office Word', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Report Viewer.*','Microsoft Report Viewer', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Search.*','Microsoft Search', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Server Speech.*','Microsoft Server Speech', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft SkypeBusiness.*','Microsoft SkypeBusiness', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Slide.*','Microsoft Slide', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Visual Basic.*','Microsoft Visual Basic', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Visual C\+\+.*','Microsoft Visual C++', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Visual F#.*','Microsoft Visual F#', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Visual FoxPro.*','Microsoft Visual FoxPro', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Visual J#.*','Microsoft Visual J#', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Visual SourceSafe.*','Microsoft Visual SourceSafe', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Visual Studio.*','Microsoft Visual Studio', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft VSS.*','Microsoft VSS', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Web Analytics.*','Microsoft Web Analytics', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Web Developer Tools.*','Microsoft Web Developer Tools', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Microsoft Workflow.*','Microsoft Workflow', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^PowerShell.*','PowerShell', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Skype.*','Skype', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^SQL Server.*','SQL Server', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^WCF Data Services.*','WCF Data Services', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Windows 10.*','Windows 10', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Windows 8.*','Windows 8', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Windows Live.*','Windows Live', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Windows Mobile.*','Windows Mobile', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Windows Phone.*','Windows Phone', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^Windows XP.*','Windows XP', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
df_sorted_microsoft['name'] =  [re.sub(r'^WinRT Intellisense.*','WinRT Intellisense', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]

df_sorted_microsoft['name'] =  [re.sub(r'^(?!(Appman Auto Sequencer|Behaviors SDK Visual|Bing Bar|BrowserSQL Server|Business Contact Manager para Microsoft Outlook|ClickOnce Bootstrapper PackageMicrosoft .NET Framework|Custom UI EditorMicrosoft Office|DHTML Editing Component|DiagnosticsHub_CollectionService|Dictate|Document Translator|Entity Framework Tools Visual|Hotfix|IIS Express|Imaging|Integration Services|JavaScript Tooling|Kerberos Configuration ManagerSQL Server|Local Administrator Password Solution|Log Parser|MDI To TIFF File Converter|Memory Profiler|Messaging API and Collaboration Data Objects|Microsoft .NET Core|Microsoft .NET Framework|Microsoft .NET Native SDK|Microsoft ActiveSync|Microsoft Advertising|Microsoft AgentsVisual Studio Preview|Microsoft Analysis Services OLE DB Provider|Microsoft Application|Microsoft AS OLE DB ProviderSQL Server|Microsoft ASP.NET|Microsoft Assessment and Planning Toolkit|Microsoft Azure|Microsoft Baseline Security Analyzer|Microsoft BlendVisual|Microsoft Build|Microsoft Camera Codec Pack|Microsoft CAPICOM SDK|Microsoft Chart ControlsMicrosoft .NET Framework|Microsoft DaRT|Microsoft DCF MUI|Microsoft Default Manager|Microsoft Device Emulator|Microsoft Document|Microsoft Edge|Microsoft Exchange Web Services Managed API|Microsoft Expression Web|Microsoft FrontPage Client -|Microsoft FxCop|Microsoft Garage Mouse without Borders|Microsoft HEVC Media Extension|Microsoft Identity Extensions|Microsoft IE ActiveX Analyzer|Microsoft InfoPath|Microsoft IntelliPoint|Microsoft iSCSI Software Target|Microsoft Keyboard Layout Creator|Microsoft LightSwitch SDK|Microsoft Lync|Microsoft Managed DirectX|Microsoft Mathematics|Microsoft Message Analyzer|Microsoft MPI|Microsoft NetStandard SDK|Microsoft Network Monitor|Microsoft NuGet - Visual|Microsoft Office|Microsoft Office Access|Microsoft Office Components|Microsoft Office Developer ToolsVisual|Microsoft Office Enterprise|Microsoft Office Excel|Microsoft Office Groove MUI|Microsoft Office OneNote MUI|Microsoft Office OSM|Microsoft Office Outlook|Microsoft Office PowerPoint|Microsoft Office Project|Microsoft Office Publisher|Microsoft Office Server|Microsoft Office Shared|Microsoft Office SharePoint|Microsoft Office Visio|Microsoft Office Visual Web Developer|Microsoft Office Web Apps|Microsoft Office Web Components|Microsoft Office Word|Microsoft OLE DB DriverSQL Server|Microsoft Power QueryExcel|Microsoft PowerBI Desktop|Microsoft Primary Interoperability Assemblies|Microsoft R Client|Microsoft R Open|Microsoft Report Viewer|Microsoft Robocopy GUI|Microsoft S/MIME|Microsoft Search|Microsoft Server Speech|Microsoft Silverlight|Microsoft Slide|Microsoft SOAP Toolkit|Microsoft SQL Server|Microsoft Sync Framework Core Components ENU|Microsoft Team Foundation Server - ENU|Microsoft TestPlatform SDK Local Feed|Microsoft UniversalWindowsPlatform SDK|Microsoft UrlScan Filter|Microsoft User Profiles|Microsoft Virtual Machine Converter|Microsoft Visual Basic|Microsoft Visual C\+\+|Microsoft Visual F#|Microsoft Visual FoxPro|Microsoft Visual J#|Microsoft Visual SourceSafe|Microsoft Visual Studio .NET|Microsoft Visual Studio Code|Microsoft VSS|Microsoft Web Analytics|Microsoft Web Deploy|Microsoft Workflow|Microsoft Works|Microsoft XML Parser|Movie Maker|MSI Development|MSN Toolbar|Photo Common|Photo Gallery|PowerShell|Skype|TypeScript SDK|VBA|WCF Data Services|Web Deployment Tool|Windows 10|Windows 8|Windows Live|Windows Media Encoder|Windows Mobile|Windows Movie Maker|Windows Phone|Windows SDK|Windows Simulator|Windows Software Development Kit|Windows System Image Manager|Windows Team Extension SDK|Windows XP|WinRT Intellisense|WPF Toolkit February|WPT|XML Notepad)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_microsoft['name']]
#df_sorted_microsoft = df_sorted_microsoft.drop_duplicates(subset='name')
df_sorted = pd.concat([df_sorted_microsoft,df_sorted_not_microsoft])
del df_sorted_microsoft,df_sorted_not_microsoft
#df_sorted = df_sorted.drop_duplicates(subset='name')

# NI

mask = (df_sorted['publisher'].str.contains('.*National Instruments.*', case=False))
df_sorted_ni = df_sorted[mask]
df_sorted_not_ni = df_sorted[~mask]
df_sorted_ni['publisher'] = "ni"
df_sorted_ni['name'] =  [re.sub(r'^NI LabVIEW.*','NI LabVIEW', str(x), flags=re.IGNORECASE) for x in df_sorted_ni['name']]
df_sorted_ni['name'] =  [re.sub(r'^NI Measurement Studio.*','NI Measurement Studio', str(x), flags=re.IGNORECASE) for x in df_sorted_ni['name']]
df_sorted_ni['name'] =  [re.sub(r'^NI PXI Platform.*','NI PXI Platform', str(x), flags=re.IGNORECASE) for x in df_sorted_ni['name']]
df_sorted_ni['name'] =  [re.sub(r'^NI Remote PXI.*','NI Remote PXI', str(x), flags=re.IGNORECASE) for x in df_sorted_ni['name']]
df_sorted_ni['name'] =  [re.sub(r'^NI System.*','NI System', str(x), flags=re.IGNORECASE) for x in df_sorted_ni['name']]
df_sorted_ni['name'] =  [re.sub(r'^(?!(Microsoft Visual C\+\+ Run-Time|NI \.NET Framework|NI ActiveX Container|NI Atomic PXIe Peripheral Module Driver|NI Authentication|NI Circuit Design Suite|NI Curl|NI DataSocket|NI Error Reporting|NI Example Finder|NI Help Assistant|NI I\/O Trace|NI LabVIEW|NI LabWindows\/CVI Run-Time Engine|NI Launcher|NI License Manager|NI Math Kernel Libraries|NI mDNS Responder|NI Measurement Studio|NI MXI Manager|NI MXS|NI Network Browser|NI OPC|NI Portable Configuration|NI PXI Platform|NI Remote PXI|NI Software ProviderMAX|NI SSL|NI System|NI TDM Streaming|NI TDMS|NI Trace Engine|NI Update Service|NI USI|NI Variable Engine|NI Visual C\+\+ Redistributable Package|NI Web Application Server|NI Web Pipeline|NI WS Repl Library|NI Xalan Delay Load|NI Xerces Delay Load|Reset NI Config)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_ni['name']]
#df_sorted_ni = df_sorted_ni.drop_duplicates(subset='name')
df_sorted = pd.concat([df_sorted_ni,df_sorted_not_ni])
del df_sorted_ni,df_sorted_not_ni
#df_sorted = df_sorted.drop_duplicates(subset='name')

# Nero

mask = (df_sorted['name'].str.contains('.*Nero.*', case=False)) | (df_sorted['publisher'].str.contains('.*Nero.*', case=False))
df_sorted_nero = df_sorted[mask]
df_sorted_not_nero = df_sorted[~mask]
df_sorted_nero['publisher'] = "Nero"
df_sorted_nero['name'] =  [re.sub(r'^(?!(Advertising Center|DolbyFiles|LG Burning|Nero|Nero Audio Pack|Nero BackItUp|Nero Blu-ray Player|Nero Burning ROM|Nero BurnRights|Nero Cliparts|Nero Control Center|Nero Core Components|Nero CoverDesigner|Nero Disc Copy Gadget|Nero Disc to Device|Nero DiscSpeed|Nero Dolby Files|Nero DriveSpeed|Nero Effects Basic|Nero Express|Nero Image Samples|Nero Info|Nero InfoTool|Nero Kwik Media|Nero Launcher|Nero Live|Nero MediaHome|Nero MediaHub|Nero Multimedia Suite|Nero PhotoSnap|Nero Recode|Nero Rescue Agent|Nero ShowTime|Nero SoundTrax|Nero StartSmart|Nero Suite|Nero Video|Nero Vision|Nero WaveEditor)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_nero['name']]
#df_sorted_nero = df_sorted_nero.drop_duplicates(subset='name')
df_sorted = pd.concat([df_sorted_nero,df_sorted_not_nero])
del df_sorted_nero,df_sorted_not_nero
#df_sorted = df_sorted.drop_duplicates(subset='name')

# Epson

mask = (df_sorted['name'].str.contains('.*Epson(?!( sudoku))', case=False)) | (df_sorted['publisher'].str.contains('.*Epson.*', case=False))
df_sorted_epson = df_sorted[mask]
df_sorted_not_epson = df_sorted[~mask]
df_sorted_epson['publisher'] = "Epson"
df_sorted_epson['name'] =  [re.sub(r'^Easy Interactive.*','Easy Interactive', str(x), flags=re.IGNORECASE) for x in df_sorted_epson['name']]
df_sorted_epson['name'] =  [re.sub(r'^EpsonNet.*','EpsonNet', str(x), flags=re.IGNORECASE) for x in df_sorted_epson['name']]
df_sorted_epson['name'] =  [re.sub(r' Ver\.*','', str(x), flags=re.IGNORECASE) for x in df_sorted_epson['name']]
df_sorted_epson['name'] =  [re.sub(r'^(?!(Easy Interactive|EpsonNet|Document Capture|Easy Photo Scan|EasyMP Multi PC Projection|EasyMP Network Projection|Epson Copy Utility|Epson Device Admin|Epson Easy Photo Print|Epson Event Manager|Epson FAX Utility|EPSON File Manager|EPSON Image Clip Palette|Epson iProjection|EPSON LFP Remote Panel|Epson Monitoring Tool|EPSON Monochrome Laser P6|EPSON Photo Print|EPSON PhotoQuicker|EPSON Port Communication Service|Epson Scan|EPSON Smart Panel|EPSON Standard Business Printers|EPSON Status Monitor|Epson USB Display|EPSON Web-To-Page|EpsonNet|SureLab OrderController LE)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_epson['name']]
#df_sorted_epson = df_sorted_epson.drop_duplicates(subset='name')
df_sorted = pd.concat([df_sorted_epson,df_sorted_not_epson])
del df_sorted_epson,df_sorted_not_epson
#df_sorted = df_sorted.drop_duplicates(subset='name')

# SAP

mask = (df_sorted['name'].str.contains('SAP\b')) | (df_sorted['publisher'].str.contains('SAP($| )'))
df_sorted_sap = df_sorted[mask]
df_sorted_not_sap = df_sorted[~mask]
df_sorted_sap['publisher'] = "SAP"
df_sorted_sap['name'] =  [re.sub(r'^Crystal ReportsVisual.*','Crystal Reports Visual', str(x), flags=re.IGNORECASE) for x in df_sorted_sap['name']]
df_sorted_sap['name'] =  [re.sub(r'^Crystal Report.*','Crystal Reports', str(x), flags=re.IGNORECASE) for x in df_sorted_sap['name']]
df_sorted_sap['name'] =  [re.sub(r'.*SAP Business One.*','SAP Business One', str(x), flags=re.IGNORECASE) for x in df_sorted_sap['name']]
df_sorted_sap['name'] =  [re.sub(r'^(?!(Crystal Reports Visual|Crystal Reports|SAP Business One|SAP PowerBuilder|SAP PowerDesigner)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted_sap['name']]
#df_sorted_sap = df_sorted_sap.drop_duplicates(subset='name')
df_sorted = pd.concat([df_sorted_sap,df_sorted_not_sap])
del df_sorted_sap, df_sorted_not_sap
#df_sorted = df_sorted.drop_duplicates(subset='name')

#

df_sorted['name'].loc[df_sorted['name'].str.contains('^ArcGIS')] =  [re.sub(r'^ArcGIS Pro.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('^ArcGIS')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('^Zebra') | df_sorted['publisher'].str.contains('Zebra')] = [re.sub(r'.*windows.*|.*zxp.*|.*driver.*|.*font.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('^Zebra') | df_sorted['publisher'].str.contains('Zebra')]]
df_sorted['publisher'].loc[df_sorted['name'].str.contains('Xerox') | df_sorted['publisher'].str.contains('Xerox')] = "Xerox"
df_sorted['name'].loc[df_sorted['name'].str.contains('Xerox') | df_sorted['publisher'].str.contains('Xerox')] =  [re.sub(r'^(?!(Xerox Scan Assistant|AccXES)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Xerox') | df_sorted['publisher'].str.contains('Xerox')]]
df_sorted['publisher'].loc[df_sorted['name'].str.contains('Veritas') | df_sorted['publisher'].str.contains('Veritas')] = "Veritas"
df_sorted['name'].loc[df_sorted['name'].str.contains('Veritas') | df_sorted['publisher'].str.contains('Veritas')] =  [re.sub(r'^(?!(Veritas Quick Assist|Veritas Backup Exec|Veritas System Recovery)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Veritas') | df_sorted['publisher'].str.contains('Veritas')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('VMware') | df_sorted['publisher'].str.contains('VMware')] =  [re.sub(r'^(?!(VMware OVF Tool|VMware Player|VMware PowerCLI|VMware Remote Console|VMware VIX|VMware Workstation|VMware vCenter Converter Standalone|VMware vCloud Automation Center Agents - vCenter|VMware vSphere CLI)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('VMware') | df_sorted['publisher'].str.contains('VMware')]]
df_sorted['publisher'].loc[df_sorted['name'].str.contains('Trimble') | df_sorted['publisher'].str.contains('Trimble')] = "Trimble"
df_sorted['name'].loc[df_sorted['name'].str.contains('Trimble') | df_sorted['publisher'].str.contains('Trimble')] =  [re.sub(r'.*gps.*|.*geospatial.*|.*add-on.*|.*updater?$|.*-.*|.*emulator.*|.*installation.*|.*photogrammetry.*|.*activation.*|.*solutions.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Trimble') | df_sorted['publisher'].str.contains('Trimble')]]
df_sorted['publisher'].loc[df_sorted['name'].str.contains('Trend Micro') | df_sorted['publisher'].str.contains('Trend Micro')] = "Trend Micro"
df_sorted['name'].loc[df_sorted['name'].str.contains('Trend Micro') | df_sorted['publisher'].str.contains('Trend Micro')] =  [re.sub(r'.*agente.*|.*infrastructure.*','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Trend Micro') | df_sorted['publisher'].str.contains('Trend Micro')]]
df_sorted['publisher'].loc[~df_sorted['publisher'].str.contains('Sierra|Wordcraft', case=False) & (df_sorted['name'].str.contains('Toshiba', case=False) | df_sorted['publisher'].str.contains('Toshiba', case=False))] = "Toshiba"
df_sorted['name'].loc[~df_sorted['publisher'].str.contains('Sierra|Wordcraft', case=False) & (df_sorted['name'].str.contains('Toshiba', case=False) | df_sorted['publisher'].str.contains('Toshiba', case=False))] =  [re.sub(r'^(?!(Bluetooth Mon.*|TOSHIBA Fingerprint.*|TOSHIBA HDD.*|TOSHIBA Hardware.*|TOSHIBA Sync.*|TOSHIBA Web Camera.*|Toshiba Assist|TOSHIBA e-STUDIO Address.*|TOSHIBA e-STUDIO BackUp.*|TOSHIBA e-STUDIO File.*|Bluetooth Link|TOSHIBA Audio.*|TOSHIBA Display.*|TOSHIBA Function.*|TOSHIBA PC Health.*|TOSHIBA Password.*|TOSHIBA Recovery Media.*|TOSHIBA Service.*|TOSHIBA VIDEO PLAYER|TOSHIBA eco.*|TOSHIBA System Modules|Toshiba TEMPRO|SSD Utility|TOSHIBA Button.*)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[~df_sorted['publisher'].str.contains('Sierra|Wordcraft', case=False) & (df_sorted['name'].str.contains('Toshiba', case=False) | df_sorted['publisher'].str.contains('Toshiba', case=False))]]
df_sorted['publisher'].loc[df_sorted['name'].str.contains('Tibco', case=False) | df_sorted['publisher'].str.contains('Tibco', case=False)] = "Tibco"
df_sorted['name'].loc[df_sorted['name'].str.contains('Tibco', case=False) | df_sorted['publisher'].str.contains('Tibco', case=False)] = [re.sub(r'^TIBCO Rendezvous.*','TIBCO Rendezvous', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Tibco') | df_sorted['publisher'].str.contains('Tibco')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('Tibco', case=False) | df_sorted['publisher'].str.contains('Tibco', case=False)] = [re.sub(r'^(?!(TIBCO Jaspersoft|TIBCO Rendezvous)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Tibco') | df_sorted['publisher'].str.contains('Tibco')]]
df_sorted['publisher'].loc[df_sorted['name'].str.contains('MATLAB', case=False) | df_sorted['publisher'].str.contains('MathWorks', case=False)] = "MathWorks"
df_sorted['name'].loc[df_sorted['name'].str.contains('MATLAB', case=False) | df_sorted['publisher'].str.contains('MathWorks', case=False)] = [re.sub(r'^.*$','MATLAB', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('MATLAB') | df_sorted['publisher'].str.contains('MathWorks')]]
df_sorted['publisher'].loc[df_sorted['name'].str.contains('Apache', case=False) | df_sorted['publisher'].str.contains('Apache', case=False)] = "The Apache Software Foundation"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('The Apache Software Foundation', case=False)] = [re.sub(r'apache-ant-.*','Apache Ant', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('The Apache Software Foundation')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('The Apache Software Foundation', case=False)] = [re.sub(r'Apache Directory Studio -.*','Apache Directory Studio', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('The Apache Software Foundation')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('The Apache Software Foundation', case=False)] = [re.sub(r'^(?!(Apache HTTP Server|OpenOffice|Apache Tomcat|Apache Directory Studio|Apache Ant)$).*$', '', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('The Apache Software Foundation')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('Texas Instruments', case=False) | df_sorted['publisher'].str.contains('Texas Instruments', case=False)] = [re.sub(r'^(?!(TIPCI)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Texas Instruments') | df_sorted['publisher'].str.contains('Texas Instruments')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('TechSmith', case=False) | df_sorted['publisher'].str.contains('TechSmith', case=False)] = [re.sub(r'^(?!(Camtasia|SnagIt)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('TechSmith') | df_sorted['publisher'].str.contains('TechSmith')]]
df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('SysTools', case=False)] = [re.sub(r'SysTools Software.*','SysTools Software', str(x), flags=re.IGNORECASE) for x in df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('SysTools', case=False)]]
df_sorted['name'].loc[df_sorted['name'].str.contains('Synology', case=False) | df_sorted['publisher'].str.contains('Synology', case=False)] = [re.sub(r'^(?!(Synology Assistant|Synology Surveillance Station Client)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Synology') | df_sorted['publisher'].str.contains('Synology')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('Sybase', case=False) | df_sorted['publisher'].str.contains('Sybase', case=False)] = [re.sub(r'Sybase DataWindow.*','Sybase DataWindow', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Sybase') | df_sorted['publisher'].str.contains('Sybase')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('Sybase', case=False) | df_sorted['publisher'].str.contains('Sybase', case=False)] = [re.sub(r'^(?!(Sybase DataWindow|Sybase PowerBuilder|Sybase PowerDesigner|Sybase Adaptive Server Enterprise Suite)$).*$','Sybase DataWindow', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Sybase') | df_sorted['publisher'].str.contains('Sybase')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sun Microsystems', case=False)] = [re.sub(r', se.*| update','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sun Microsystems', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sun Microsystems', case=False)] = [re.sub(r'^(?!(J2SE Development Kit|J2SE Runtime Environment|Java 2 SDK)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sun Microsystems', case=False)]]
df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Sublime HQ', case=False)] = "Sublime HQ"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sublime HQ', case=False)] = [re.sub(r' Build','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sublime HQ', case=False)]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Sparx Systems', case=False)] = "Sparx Systems"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sparx Systems', case=False)] = [re.sub(r'^MDG.*','MDG', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sparx Systems')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sparx Systems', case=False)] = [re.sub(r'^(?!(Enterprise Architect|MDG|Sparx Systems Keystore Service)$).*$','', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Sparx Systems', case=False)]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Sony', case=False) | df_sorted['publisher'].str.contains('Sony', case=False)] = "Sony"
df_sorted['name'].loc[df_sorted['name'].str.contains('Sony', case=False) | df_sorted['publisher'].str.contains('Sony', case=False)] = [re.sub(r'^(?!(Image Data Converter|Media Go|PlayMemories Home|Xperia Companion|Sony PC Companion|Sound Organizer|PlayStationStore|Sony Mobile Update Engine)$).*$','', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Sony', case=False) | df_sorted['publisher'].str.contains('Sony', case=False)]]

df_sorted['name'].loc[df_sorted['name'].str.contains('SolarWinds', case=False) | df_sorted['publisher'].str.contains('SolarWinds', case=False)] = [re.sub(r'^SolarWinds Engineer.*$',r'SolarWinds Engineers Toolset', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('SolarWinds', case=False) | df_sorted['publisher'].str.contains('SolarWinds', case=False)]]
df_sorted['name'].loc[df_sorted['name'].str.contains('PuTTY', case=False) | df_sorted['publisher'].str.contains('Simon Tatham', case=False)] = [re.sub(r'^(?!(PuTTY)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('PuTTY', case=False) | df_sorted['publisher'].str.contains('Simon Tatham', case=False)]]
df_sorted['name'].loc[df_sorted['name'].str.contains('Sierra Wireless', case=False) | df_sorted['publisher'].str.contains('Sierra Wireless', case=False)] = [re.sub(r'^(?!(Sierra Wireless Skylight)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Sierra Wireless', case=False) | df_sorted['publisher'].str.contains('Sierra Wireless', case=False)]]
df_sorted['name'].loc[df_sorted['name'].str.contains('Schneider Electric', case=False) | df_sorted['publisher'].str.contains('Schneider Electric', case=False)] = [re.sub(r'^(?!(Advanced View|EcoStruxure IT Gateway|PowerChute Personal|Rapsody ES)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Schneider Electric', case=False) | df_sorted['publisher'].str.contains('Schneider Electric', case=False)]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('ScanSoft', case=False) | df_sorted['publisher'].str.contains('ScanSoft', case=False)] = "Nuance Communications/ScanSoft"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('ScanSoft', case=False)] = [re.sub(r'^(?!(ScanSoft OmniPage|ScanSoft PaperPort|Scansoft PDF)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('ScanSoft', case=False)]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Samsung', case=False) | df_sorted['publisher'].str.contains('Samsung', case=False)] = "Samsung"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Samsung', case=False)] = [re.sub(r'^(?!(iDRS OCR Software by I.R.I.S|Samsung Data Migration|Samsung Easy Wireless Setup|Samsung Kies|Samsung Magician|Samsung Network PC Fax|Samsung Portable SSD Software|Samsung Printer Center|Samsung Printer Live Update|Samsung Scan Assistant|Samsung Scan Process Machine|Samsung SideSync|Samsung UD Sender|SAMSUNG USB DriverMobile Phones|Smart Switch|SmarThru|SNS UploadEasy Document Creator|WebViewer DVR)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Samsung', case=False)]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('SMART') | df_sorted['publisher'].str.contains('SMART')] = "SMART"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('SMART')] = [re.sub(r'^Software de ',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('SMART')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('SMART')] = [re.sub(r'^(?!(MyScript HWR|SMART Image Mate|SMART Ink|SMART Notebook|SMART Sync|SMART Response)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('SMART')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('SHARP')] = [re.sub(r'^(?!(Network Scanner Tool Lite|Sharpdesk)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('SHARP')]]
df_sorted['name'].loc[df_sorted['name'].str.contains('SAS') | df_sorted['publisher'].str.contains('SAS')] = [re.sub(r'^(?!(SAS)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('SAS') | df_sorted['publisher'].str.contains('SAS')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Roxio')] = [re.sub(r'^(?!(Roxio BackOnTrack|Roxio Central|Roxio CinePlayer|Roxio Creator|Roxio Drag-to-Disc|Roxio Express Labeler|Roxio File Backup|Roxio MyDVD)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Roxio')]]

df_sorted['name'].loc[df_sorted['name'].str.contains('Ricoh', case=False) | df_sorted['publisher'].str.contains('Ricoh', case=False)] = [re.sub(r'^(?!(RICOH Media Driver|Smart Organizing Monitor|DeskTopBinder Lite|Device Manager NX Lite)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Ricoh', case=False) | df_sorted['publisher'].str.contains('Ricoh', case=False)]]

df_sorted['name'].loc[df_sorted['name'].str.contains('Recovery ToolBox', case=False) | df_sorted['publisher'].str.contains('Recovery ToolBox', case=False)] = [re.sub(r'^Recovery Toolbox.*',r'Recovery Toolbox', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Recovery ToolBox', case=False) | df_sorted['publisher'].str.contains('Recovery ToolBox', case=False)]]

df_sorted['name'].loc[df_sorted['name'].str.contains('Realtek', case=False) | df_sorted['publisher'].str.contains('Realtek', case=False)] = [re.sub(r'^(?!(Realtek Ethernet Diagnostic Utility)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['name'].str.contains('Realtek', case=False) | df_sorted['publisher'].str.contains('Realtek', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Quest Software', case=False)] = [re.sub(r'^Quest Change Auditor.*$',r'Quest Change Auditor', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Quest Software', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Quest Software', case=False)] = [re.sub(r'^Quest Software Toad.*$',r'Quest Software Toad', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Quest Software', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Quest Software', case=False)] = [re.sub(r'^(?!(Benchmark FactoryDatabases|Knowledge Xpert|Quest ActiveRoles Management ShellActive Directory|Quest Application Integration Tool|Quest Backup Reporter|Quest Change Auditor|Quest Software Toad|Quest SQL Optimizer Oracle|Quest Toad Data Modeler|vWorkspace ConnectorWeb Access)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Quest Software', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Portrait Displays', case=False)] = [re.sub(r'^(?!(Pivot|SDK)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Portrait Displays', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Pinnacle', case=False)] = [re.sub(r'.*',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Pinnacle', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Photodex', case=False)] = [re.sub(r'^(?!(ProShow Gold|Photodex Presenter)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Photodex', case=False)]]


df_sorted['publisher'].loc[df_sorted['name'].str.contains('Philips', case=False) | df_sorted['publisher'].str.contains('Philips', case=False)] = "Philips"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Philips', case=False)] = [re.sub(r'^SpeechMagic.*$',r'SpeechMagic', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Philips', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Philips', case=False)] = [re.sub(r'^(?!(Philips Actiware|Philips Device Control Center|Philips Intelligent Agent|Philips IntelliSpace Portal Client|Philips VLounge|SpeechMagic)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Philips', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Paragon Software', case=False)] = [re.sub(r'.* Software.*',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Paragon Software', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Panda Security', case=False)] = [re.sub(r'Panda USB Vaccine.*',r'Panda USB Vaccine', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Panda Security', case=False)]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Panasonic', case=False) | df_sorted['publisher'].str.contains('Panasonic', case=False)] = "Panasonic"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Panasonic', case=False)] = [re.sub(r'^(?!(BTup Service|Communications Utility|IDREngine|Image Capture|Multi Monitoring and Control Software|Panasonic Communications Utility|PHOTOfunSTUDIO AE|Recovery Disc Creation Utility|System Interface Manager|Wireless Toolbox)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Panasonic', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('PTC', case=False)] = [re.sub(r'.*Arbortext IsoView$',r'Arbortext IsoView', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('PTC', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('PFU')] = [re.sub(r'^.*$',r'Fujitsu ScandAll', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('PFU', case=False)]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Oracle')] = "Oracle"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle')] = [re.sub(r'^MySQL.*$',r'MySQL', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle')] = [re.sub(r'^Oracle Database.*$',r'Oracle Database Express', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle')] = [re.sub(r'^Oracle Developer ToolsVisual Studio Help.*$',r'Oracle Developer ToolsVisual', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle', case=False)] = [re.sub(r'^(?!(Java|Java SE Development Kit|JavaFX SDK|MySQL|Oracle Database Express|Oracle Developer ToolsVisual|Oracle VM VirtualBox)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oracle', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('OpenText')] = [re.sub(r'^AuWebVwr.*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('OpenText', case=False)]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Oki ?Data', case=False)] = "Oki Data"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oki Data', case=False)] = [re.sub(r'^(?!(OKI Configuration Tool)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Oki Data', case=False)]] #DEJO UNO COMO MUESTRA. DIRÍA QUE EL SOFTWARE DE OKIDATA SE INSTALA SOLO CUANDO CONECTAS UNA IMPRESORA, POR ESO PREFIERO DEJAR AUNQUE SEA UN SOFTWARE COMO MUESTRA DE QUE HAY MÁS

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('O2Micro', case=False)] = "O2Micro"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('O2Micro', case=False)] = [re.sub(r'^(?!(O2Micro Flash Memory Card Reader Driver)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('O2Micro', case=False)]]


df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Nuance', case=False) & ~df_sorted['publisher'].str.contains('ScanSoft', case=False)] = "Nuance Communications"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('^Nuance Communications$', case=False)] = [re.sub(r' Professional| Ultimate| Java Component.*',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('^Nuance Communications$', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('^Nuance Communications$', case=False)] = [re.sub(r'^(?!(Dragon|Equitrac Express|Nuance Cloud Connector|Nuance OmniPage|Nuance PaperPort|Nuance PDF Create|Nuance PDF Converter|Nuance PDF Viewer|Nuance Recognizer|Nuance Speech Server|Nuance VocalizerNetwork|SpeechMagic)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('^Nuance Communications$', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Nokia', case=False)] = [re.sub(r'^(?!(Nokia PC Suite|PC Connectivity Solution)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Nokia', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Nikon', case=False)] = [re.sub(r'^(?!(Capture NX-D|Nikon File Uploader|ViewNX)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Nikon', case=False)]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('NewSoft', case=False)] = "NewSoft"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('NewSoft', case=False)] = [re.sub(r'^(?!(Presto! BizCard|Presto! PageManager|NewSoft CD Labeler)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('NewSoft', case=False)]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('NVIDIA', case=False)] = [re.sub(r'^NVIDIA SHIELD.*$',r'NVIDIA SHIELD', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('NVIDIA', case=False)]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('NVIDIA', case=False)] = [re.sub(r'^(?!(NVIDIA ABHub|NVIDIA Ansel|NVIDIA Control Panel|NVIDIA GAME System Software|NVIDIA GeForce Experience|NVIDIA Network Service|NVIDIA NodeJS|NVIDIA nView|NVIDIA PhysX|NVIDIA ShadowPlay|Nvidia Share|NVIDIA SHIELD Streaming)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('NVIDIA', case=False)]]

# COMO QUEDAN MUCHOS, PASO A HACERLOS SEGÚN SEAN MÁS COMUNES

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Intel', case=False)] = "Intel"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel')] = [re.sub(r'�',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel')] = [re.sub(r'^Intel Optane.*$',r'Intel Optane', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel')] = [re.sub(r'^Intel RealSense SDK.*$',r'Intel RealSense SDK', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel')] = [re.sub(r'^(?!(Intel Accelerated Storage Manager|Intel CCF Manager|Intel Computing Improvement Program|Intel CPU RuntimeOpenCL Applications|Intel Driver & Support Assistant|Intel Dynamic Platform and Thermal Framework|Intel GFX Driver|Intel Hardware Accelerated Execution Manager|Intel Manageability Engine Firmware Recovery Agent|Intel Network Connections|Intel Online Connect|Intel OpenCL CPU Runtime|Intel Optane|Intel Processor Diagnostic Tool|Intel Processor Identification Utility|Intel PROSet/Wireless Software|Intel RealSense SDK|Intel Security Assist|Intel Unite|Intel WiDi|Intel Wireless Bluetooth|STCServ|Thunderbolt Software|XMLinst)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Intel', case=False)]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Logitech', case=False)] = "Logitech"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Logitech')] = [re.sub(r'^(?!(Dell App LauncherUnifying Software|erLT|Logitech Capture|Logitech Options|Logitech Presentation|Logitech Vid)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Logitech')]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('IBM', case=False)] = "IBM"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('IBM')] = [re.sub(r'�| v?\d.*',r'', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('IBM')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('IBM')] = [re.sub(r'^(?!(Aspera Connect|Host Access Toolkit|IBM - Type Transformer and Utilities|IBM ILOG CPLEX Optimization|IBM Lotus Organizer|IBM Managed Host On-Demand|IBM Notes Social|IBM Personal Communications|IBM RMF Performance Monitoring|IBM Runtime EnvironmentJava|IBM SDKNode.js|IBM Security zSecure Visual|IBM SoftCopy Librarian|IBM Spectrum Protect Client|IBM Spectrum Protect JVM|IBM SPSS Amos|IBM SPSS Modeler|IBM SPSS Statistics|IBM SPSS Text AnalyticsSurveys|IBM Tivoli Monitoring|IBM Tivoli Storage Manager Client|IBM UPS Manager|IBM Rational Application DeveloperWebSphere Software|Lotus Notes|Rational Engineering Lifecycle Manager)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('IBM')]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Dell', case=False)] = "Dell"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Dell')] = [re.sub(r'^(?!(Dell Change Auditor Agent|Dell Digital Delivery|Dell EMC OpenManage Systems Management Software|Dell Precision Optimizer|Dell SQL OptimizerOracle|Dell Toad Data Modeler|Dell Watchdog Timer|PowerNap|ToadMySQL Freeware|ToadOracle|Unisphere Service Manager|USBTypeC Status Display)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Dell')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('\?', case=False)] = ""

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Konica', case=False) | df_sorted['publisher'].str.contains('Konica', case=False)] = "Konica Minolta"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Konica Minolta')] = [re.sub(r'^(?!(FTP Utility|KONICA MINOLTA Font Manager|KONICA MINOLTA PageScope Direct Print)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Konica Minolta')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('InterSystems', case=False)] = "" #OJO CON ESTO PORQUE EL "SOFTWARE" QUE TIENEN ES UN POCO RARO, NO PARECE SOFTWARE SINO RESTOS DE UNA INSTALACIÓN PREVIA QUE NO SE DESINSTALARON BIEN
 
df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Hitachi', case=False)] = "Hitachi"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Hitachi')] = [re.sub(r'^(?!(StarBoard Document Capture|StarBoard Software|i-learn: maths toolbox)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Hitachi')]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Harris RF', case=False)] = "Harris RF"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Harris RF')] = [re.sub(r'^(?!(Harris Communications Planning Application|Imager|Tactical Chat)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Harris RF')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Google', case=False) | df_sorted['publisher'].str.contains('Google', case=False)] = "Google"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Google')] = [re.sub(r'^Google Earth Plug-in$|^Google Update Helper$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Google')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Garmin', case=False) | df_sorted['publisher'].str.contains('Garmin', case=False)] = "Garmin"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Garmin')] = [re.sub(r' tray$| v\d',r'', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Garmin')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Gigabyte', case=False) | df_sorted['publisher'].str.contains('Gigabyte', case=False)] = "Gigabyte"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Gigabyte')] = [re.sub(r'^(?!(3DOSD|@BIOS|AORUS ENGINE|APP Center|AutoGreen|BUSB|Cloud Station|EasyBoost|EasyTune|EZRAID|Fast Boot|Game Boost|GIGABYTE OC_GURU|GService|PlatformPowerManagement|SIV|Smart Backup|Smart TimeLock|SmartHUD|SmartKeyboard|VTuner)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Gigabyte')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Fujitsu', case=False) | df_sorted['publisher'].str.contains('Fujitsu', case=False)] = "Fujitsu"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Fujitsu')] = [re.sub(r'^(?!(AIS Connect|Fujitsu Hotkey Utility|FUJITSU PalmSecure SensorDriver|Fujitsu ServerView PrimeUp|Fujitsu ServerView RAID Manager|Fujitsu Siemens Computers WLAN b/g|Pointing Device Utility|Scanner UtilityMicrosoft Windows|Wireless Radio Switch Driver|Fujitsu ScandAll)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Fujitsu')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('McAfee', case=False) | df_sorted['publisher'].str.contains('McAfee', case=False)] = "McAfee"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('McAfee')] = [re.sub(r'^(?!(McAfee Active Response|McAfee Agent|McAfee Data Exchange Layer|McAfee Endpoint Security Firewall|McAfee Endpoint Security Platform|McAfee Endpoint Security Threat Prevention|McAfee Host Intrusion Prevention|McAfee RSD Sensor|McAfee Security Scan|McAfee VirusScan Enterprise|McAfee WebAdvisor)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('McAfee')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Martin Prikryl')] = [re.sub(r'^(?!(WinSCP)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Martin Prikryl')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Kyocera', case=False) | df_sorted['publisher'].str.contains('Kyocera', case=False)] = "Kyocera"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Kyocera')] = [re.sub(r'^(?!(File Management Utility|KM-NET VIEWER|Kyocera Address Editor|KYOCERA Client Tool|KYOCERA Net Direct Print|KYOCERA Net Viewer|Kyocera Printer Extension|Kyocera Product Library|Kyocera Scanner File Utility|KYOCERA Status Monitor|Kyocera TWAIN Driver|KyoceraMita Scanner File Utility|NETWORK PRINT MONITOR|Olivetti Product Library|Product Library|Status Monitor|TWAIN Driver)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Kyocera')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Flexera', case=False) | df_sorted['publisher'].str.contains('Flexera', case=False)] = "Flexera"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Flexera')] = [re.sub(r'^(?!(EFI Flexera License Manager|InstallShield Limited|Download Manager)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Flexera')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('FileMaker')] = [re.sub(r'^FileMaker.*$',r'FileMaker', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('FileMaker')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('FastReports')] = [re.sub(r'^FastReport.*$',r'FastReport', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('FastReports')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('Environmental Systems')] = [re.sub(r'^(?!(ArcGIS|ArcGIS ArcReader|ArcGIS Coordinate Systems Data|ArcGIS Data Interoperability Desktop|ArcGIS Desktop|ArcGIS Earth|ArcGIS Engine Runtime|ArcGIS Explorer Desktop|ArcGIS Full Motion Video Geoprocessing|ArcGIS Server|ArcGIS Web Adaptor|ArcGIS Workflow Manager Desktop|ArcSDE Command Line|ArcSDE Microsoft SQL Server|Intelligence ConfigurationArcGIS|Mapping and Charting Solutions|Military Overlay Editor)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Environmental Systems')]]

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Embarcadero', case=False)] = "Embarcadero"

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Advanced Micro Devices', case=False)] = "amd"

df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Dassault', case=False)] = "Dassault Systemes" 
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Dassault')] = [re.sub(r' sp\d.*$',r'', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Dassault')]]

df_sorted['name'].loc[df_sorted['publisher'].str.contains('CyberLink')] = [re.sub(r'^(?!(CyberLink InstantBurn|CyberLink LabelPrint|CyberLink Media Suite|CyberLink PhotoNow|CyberLink Power2Go|CyberLink PowerBackup|CyberLink PowerDirector|CyberLink PowerDVD|CyberLink PowerProducer|CyberLink Screen Recorder|CyberLink WaveEditor|CyberLink Wedding Pack|CyberLink YouCam|Gear 360 ActionDirector|Gear 360 Live Broadcast)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('CyberLink')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Corel', case=False) | df_sorted['publisher'].str.contains('Corel', case=False)] = "Corel"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Corel')] = [re.sub(r'^(?!(Corel ActiveCGM Browser|Corel Applications|Corel Graphics Suite|Corel Shell Extension -|Corel VideoStudio|Ghostscript GPL|Pinnacle Studio|Title Extreme|CorelDRAW Graphics Suite.*)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Corel')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Cisco', case=False) | df_sorted['publisher'].str.contains('Cisco', case=False)] = "Cisco"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Cisco')] = [re.sub(r'^(?!(Cisco AnyConnect Secure Mobility Client|Cisco ASDM-IDM Launcher|Cisco FindIT|Cisco IP Communicator|Cisco Network Assistant|Cisco Packet Tracer|Cisco SDM|Cisco TFTP Server|Cisco Unified CallManager Assistant Console|Cisco Unified Real-Time Monitoring Tool|Cisco VideoGuard Player|Network Recording Player)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Cisco')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains(r'\bCA\b', case=False) | df_sorted['publisher'].str.contains(r'\bCA\b', case=False)] = "CA"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('CA')] = [re.sub(r' sp\d| r\d?',r'', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('CA')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('CA')] = [re.sub(r'CA AllFusion.*$',r'CA AllFusion', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('CA')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('CA')] = [re.sub(r'CA DSM.*$',r'CA DSM', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('CA')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('Bentley', case=False) | df_sorted['publisher'].str.contains('Bentley', case=False)] = "Bentley"
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Bentley')] = [re.sub(r'Bentley MicroStation.*$',r'Bentley MicroStation', str(x), flags=re.IGNORECASE) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Bentley')]]
df_sorted['name'].loc[df_sorted['publisher'].str.contains('Bentley')] = [re.sub(r'^(?!(Bentley CADscript|Bentley DGN IFilter|Bentley DGN Index Service|Bentley DGN Preview Handler|Bentley DGN Thumbnail Provider|Bentley MicroStation|Bentley View XM|HDR Preview|Visualization Content)$).*$',r'', str(x)) for x in df_sorted['name'].loc[df_sorted['publisher'].str.contains('Bentley')]]

df_sorted['publisher'].loc[df_sorted['name'].str.contains('LibreOffice', case=False)] = "LibreOffice"
df_sorted['publisher'].loc[df_sorted['name'].str.contains('GIMP', case=False)] = "GIMP"
df_sorted['publisher'].loc[df_sorted['publisher'].str.contains('Git Development')] = "Git"

df_sorted['name'] =  [re.sub(r'\+','\+', str(x), flags=re.IGNORECASE) for x in df_sorted['name']]

# df_sorted['name_original'] =  [re.sub(r'\p{P}|\p{S}|\s|\d',' ', str(x), flags=re.IGNORECASE) for x in df_sorted['name_original']]

#Guardo la version que pudiera aparecer en el campo nombre, en el campo version, para que estén ahí todas
for i in range(df_sorted.shape[0]):
    version = re.findall('(\d+(\.\d+)+)', df_sorted.name_original[i])
    if version:
        version = list(set(version)) #ELIMINA DUPLICADOS
        for s in version:
            df_sorted.version[i] = df_sorted.version[i] + ' ' + s[0]
            
#Exporto a archivo de texto y convierto cpeuniquelist en una lista
with open('C:/.../UniqueCPEVendor.txt') as f:
    cpeuniquelist = f.readlines()
cpeuniquelist = [x.strip() for x in cpeuniquelist]

#Vuelvo a escapar caracteres especiales, ahora en publisher_original
df_sorted['publisher_original'] = [str(x).replace(r'\\', '\\\\') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('^','\^') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('$','\$') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('.','\.') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('|','\|') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('?','\?') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('*','\*') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('+','\+') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('(','\(') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace(')','\)') for x in df_sorted['publisher_original']]
df_sorted['publisher_original'] = [str(x).replace('[','\[') for x in df_sorted['publisher_original']]

#Creo la columna publisher_filtrado, que guardará los publisher que habíamos filtrado hasta ahora
df_sorted['publisher_filtrado'] = df_sorted['publisher']

start = time.time()

#En la columna publisher ahora se guardará, de la lista cpeuniquelist, el publisher que sea más parecido
publisher = ""
unique_publisher = ""
for i in range(df_sorted.shape[0]):
    if df_sorted.publisher_filtrado[i]:
        if publisher == (df_sorted.publisher_filtrado[i]).lower():
            df_sorted.publisher[i] = unique_publisher
        else:
            publisher = (df_sorted.publisher_filtrado[i]).lower()
            unique_publisher = sorted(cpeuniquelist, key=lambda x: SequenceMatcher(None, x, publisher).ratio(), reverse=True)[0]
            df_sorted.publisher[i] = unique_publisher

print(time.time() - start) #14 min

#Se exporta a fichero de texto, ordenando las columnas para mayor comodidad al manejarlas
filepathexport = 'C:/.../SoftwareFiltradoGeneral.csv'
df_sorted = df_sorted[['publisher','publisher_filtrado','publisher_original','name','name_original','version']]
df_sorted.to_csv(path_or_buf=filepathexport, sep='|', index=False, header=False, encoding='latin-1')


#df_prueba = pd.concat([df_sorted,df_read])
#df_prueba_2 = df_sorted.drop_duplicates(subset='name')
#df_prueba = df_prueba.drop_duplicates(subset='name')




########################################## SQL ##########################################




#Esta parte de SQL funciona pero no se utiliza
# import pyodbc

# filepathexport = 'C:/.../SoftwareFiltradoGeneral.csv'
# df_read = pd.read_csv(filepathexport, dtype = str, names=["publisher", "publisher_original", "name", "name_original", "version"], sep='|', encoding='latin-1')
# df_read = df_read.replace(np.nan, '', regex=True)

# conn = pyodbc.connect(r'Driver={SQL Server};'
#                       r'Server=localhost;'
#                       r'Database=Software;'
#                       r'Trusted_Connection=yes;')

# cursor = conn.cursor()

# #cursor.execute('DROP TABLE Filtered_Software;')
# #conn.commit()

# cursor.execute('CREATE TABLE Filtered_Software (Publisher nvarchar(100), Publisher_original nvarchar(100), Name nvarchar(500), Name_original nvarchar(500), Version nvarchar(100))')
# conn.commit()

# cursor.execute('''
# BULK INSERT Filtered_Software
#     FROM 'C:/.../SoftwareFiltradoGeneral.csv'
#     WITH 
#         (FIELDTERMINATOR = '|',
#          ROWTERMINATOR = '\n')''')
# conn.commit()

# for row in df_read.itertuples():
#     cursor.execute('''
#                 INSERT INTO Software.dbo.Filtered_Software (Publisher, Publisher_original, Name, Name_original, Version)
#                 VALUES (?,?,?,?,?)
#                 ''',
#                 row[1], 
#                 row[2],
#                 row[3],
#                 row[4],
#                 row[5]
#                 )
# conn.commit()

# cursor.close()
# conn.close()


# #cursor.execute('SELECT * FROM Software.dbo.software')
# #for row in cursor:
# #    print(row)
