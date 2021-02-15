# from sqlite3.dbapi2 import Cursor
from urllib.parse import urlparse
import crawDomain as craw 
import consts
import sqlite3
import unicodedata

keywords = []
caracteresAcentuados = ["á", "à", "ã", "é", "í", "ô", "ç"]

def fillKeywords():
    lista = open(consts.ARQ_KEYWORDS, 'r').read().splitlines()
    listaMinuscula = [x.lower().strip() for x in lista] 
    for l in listaMinuscula:
        keywords.append(l)

def fillQueueWithSeeds(queueUrlsVisitar):
    seeds = loadFileLikeArray(consts.ARQ_SEEDS)
    for seed in seeds:
        queueUrlsVisitar.put(seed)

def saveQueueToVisit():
    pass

def createDataBase():
    conn = sqlite3.connect(consts.ARQ_DATABASE) 
    cursor = conn.cursor() 
    cursor.execute("""  CREATE TABLE if not exists crawlerByDomain(
                        id integer primary key autoincrement,
                        url text not null,
                        page text not null,
                        keys text not null,
                        quantkeys integer not null )
                    """) 
    conn.commit() 
    conn.close() 

def insertDataInDB(url, page, keywordsFound):
    keys = ', '.join(keywordsFound)
    quantk =  len(keywordsFound) 
    conn = sqlite3.connect(consts.ARQ_DATABASE) 
    cursor = conn.cursor() 
    cursor.execute("""  INSERT INTO crawlerByDomain (url, page, keys,quantkeys) 
                        VALUES (?, ?, ?, ? ) """, (url, page, keys, quantk, ))
    conn.commit()
    conn.close() 

def initialize(queueUrlsVisitar):
    createDataBase()
    fillKeywords()
    fillQueueWithSeeds(queueUrlsVisitar)

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

