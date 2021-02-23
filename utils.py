# from sqlite3.dbapi2 import Cursor
from urllib.parse import urlparse
import crawDomain as craw 
import consts
import sqlite3
import unicodedata 
from bs4 import BeautifulSoup
from urlextract import URLExtract 
from openpyxl import Workbook 

keywords = []
caracteresAcentuados = ["á", "à", "ã", "é", "í", "ô", "ç"]

def createDataBase():
    conn = sqlite3.connect(consts.ARQ_DATABASE) 
    cursor = conn.cursor() 
    cursor.execute("""  CREATE TABLE if not exists crawlerByDomain(
                        id integer primary key autoincrement,
                        domain text, 
                        url text not null,
                        page text not null,
                        keys text not null,
                        quantkeys integer not null, 
                        titleFromPage text, 
                        keysFromPage text, 
                        langFromPage text, 
                        descFromPage text, 
                        authorFromPage text)
                    """) 
    conn.commit() 
    conn.close() 

def insertDataInDB(url, page, keywordsFound): 
    keys = ', '.join(keywordsFound) 
    quantk =  len(keywordsFound) 
    domain = getDomainFromURL(url) 

    metadata = extractMetaFromPage(page)
    titleFromPage = metadata["title"]
    keysFromPage = metadata["keywords"] 
    langFromPage = metadata["lang"] 
    descFromPage = metadata["description"] 
    authorFromPage = metadata["author"] 

    conn = sqlite3.connect(consts.ARQ_DATABASE) 
    cursor = conn.cursor() 
    cursor.execute("""  INSERT INTO crawlerByDomain (domain, url, page, keys, quantkeys, titleFromPage, keysFromPage, langFromPage, descFromPage, authorFromPage) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? ) """, (domain, url, page, keys, quantk, titleFromPage, keysFromPage, langFromPage, descFromPage, authorFromPage,))
    conn.commit()
    conn.close() 

def fillKeywords():
    lista = open(consts.ARQ_KEYWORDS, 'r').read().splitlines()
    listaMinuscula = [x.lower().strip() for x in lista] 
    for l in listaMinuscula:
        keywords.append(l)

def fillQueueWithSeeds(queueUrlsVisitar):
    seeds = loadFileLikeArray(consts.ARQ_SEEDS)
    for seed in seeds:
        queueUrlsVisitar.put(seed)

def initialize(queueUrlsVisitar):
    createDataBase()
    fillKeywords() 
    initQueueToVisit(queueUrlsVisitar)

def textNoAccent(texto):
    text = unicodedata.normalize('NFD', texto)\
           .encode('ascii', 'ignore')\
           .decode("utf-8")
    return text

def loadFileLikeArray(arq):
    """ Le o arquivo txt e gera um array em minusculas e sem espaços nas bordas
        Muito importante notar que caso tenha algum acento, o texto equivalente sem acento sera adicionado aa lista
    Returns:
        list -- Siglas tecnicas em minusculas 
    """    
    lista = open(arq, 'r').read().splitlines()
    listaMinuscula = [x.lower().strip() for x in lista] 
    for item in listaMinuscula:
        for letra in caracteresAcentuados:
            if letra in item:
                listaMinuscula.append(textNoAccent(item.lower()))
    return set(listaMinuscula)

def urlWellFormat(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc, result.path])
    except:
        return False

def loadUrlsVisited(BD):
    conn = sqlite3.connect(BD) 
    cursor = conn.cursor() 
    cursor.execute("""  select cbd.url 
                        from crawlerByDomain cbd  
                    """)
    result = cursor.fetchall()
    urls = []
    for address in result: 
        urls.append(address) 
    conn.commit()
    conn.close() 
    return urls

def getDomainFromURL(url):
    return urlparse(url).netloc
    
def isFileValid(url):
    return ( (url.rfind('.js') == -1) and (url.rfind('.jpg') == -1) and (url.rfind('.jpeg') == -1) and (url.rfind('.png') == -1) and (url.rfind('.css') == -1) and (url.rfind('.gif') == -1) and (url.rfind('.mp4') == -1) and (url.rfind('.ico') == -1) and (url.rfind('.svg') == -1))

def saveUrlsVisited(urls):
    with open(consts.ARQ_URLSVISITED, "w") as f:
        for url in urls:
            f.write(str(url) +"\n")

def saveQueueToVisit(urls):
    with open(consts.ARQ_URLSTOVISIT, "w") as f:
        while (not urls.empty()):
            link = urls.get()
            f.write(str(link) +"\n")

def loadQueueToVisit():
    resp = []
    with open(consts.ARQ_URLSTOVISIT, "r") as f:
        for line in f:
            resp.append(line.strip())
    return resp

def initQueueToVisit(queueUrlsVisitar):
    links = loadQueueToVisit()
    if len(links) > 0:
        for l in links:
            queueUrlsVisitar.put(l)
    else:
        fillQueueWithSeeds(queueUrlsVisitar)

def extractMetaFromPage(page):
    metas = {}
    metas["title"] = ""
    metas["keywords"] = ""
    metas["author"] = ""
    metas["lang"] = ""
    metas["description"] = ""

    soup = BeautifulSoup(page, "html.parser")
    if (soup.title is not None):
        metas["title"] = soup.title.string
    metas["lang"] = soup.find("html", "lang")
    meta = soup.find_all('meta')
    for tag in meta:
        if 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['description']:
            metas["description"] = tag.attrs['content']
        elif 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['keywords']:
            metas["keywords"] = tag.attrs['content']
        elif 'name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['author']:
            metas["author"] = tag.attrs['content']
        elif ('name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['lang']) or ('name' in tag.attrs.keys() and tag.attrs['name'].strip().lower() in ['language']):
            metas["lang"] = tag.attrs['content']
    return metas

def allUrlsFromDocument(data):
    extractor = URLExtract()
    urls = []
    try:
        urls = extractor.find_urls(data)
        return urls
    except:
        return urls

def allUrlsFromPage(page):
    soup = BeautifulSoup(page, "html.parser")
    links = []
    for link in soup.find_all('a'):
        links.append(link.get('href'))
    return links

def exportDataBaseToXlsx(BD):
    wb = Workbook() 
    ws0 = wb.active 
    ws0.title = 'Craw-Homeopatia' 

    conn = sqlite3.connect(BD) 
    cursor = conn.cursor() 
    cursor.execute("""  select *
                        from crawlerByDomain cbd  
                    """)
    result = cursor.fetchall()
    conn.commit()
    conn.close() 
    ws0.append(["id", "domain", "url", "page", "keys", "quantkeys", "titleFromPage", "keysFromPage", "langFromPage", "descFromPage", "authorFromPage"])
    for line in result: 
        ws0.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10]])
    wb.save(consts.ARQ_XLSRESULT)
