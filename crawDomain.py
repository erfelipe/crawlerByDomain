import queue
import utils
import requests
import consts
from urlextract import URLExtract 

begin = 0
limiteVisitas = 9000 
keywordsList = []
queueUrlsToVisit = queue.Queue() 
queueUrlsVisited = []

def urlNotVisited(url):
    return url not in queueUrlsVisited

def contentFromUrl(url):
    if (utils.urlWellFormat(url)):
        data = requests.Response
        try:
            data = requests.get(url, verify=False, timeout=10)
        except requests.RequestException as e:
            data.status_code = 400
        if (data.status_code == requests.codes.ok):
            return data.text
        else:
            return ""
    else:
            return ""

def keyswordsInDocument(data):
    keys = []
    for k in keywordsList:
        if k in data:
            keys.append(k)
    return keys

def allUrlsFromDocument(data):
    extractor = URLExtract()
    urls = extractor.find_urls(data)
    return urls

def addUrlsToVisit(urls):
    for url in urls:
        queueUrlsToVisit.put(url)

def processUrl(url):
    """ For each url, process it

    Args:
        url (str): internet address 
    """ 
    allUrls = []
    keywordsFound = []
    if (urlNotVisited(url)):
        page = contentFromUrl(url)
        keywordsFound = (keyswordsInDocument(page))
        if (len(keywordsFound) > 0): 
            allUrls = allUrlsFromDocument(page)
            utils.insertDataInDB(url, page, keywordsFound) 
        else:
            print("# URL sem keywords: ", url)
    # se tiver keywords:
    # - lista todas as urls e cadastra na fila a visitar
    # - armazena: url, conteudo, quais keyswords foram encontradas
    # coloca endereco na fila de visitadas
    else: 
        print("* URL já visitada: ", url)
    queueUrlsVisited.append(url)
    addUrlsToVisit(allUrls)

def processQueue(begin):
    """ Process the queue with seeds and prior address
    """    
    while (begin < limiteVisitas) and (not queueUrlsToVisit.empty()):
        begin += 1
        url = queueUrlsToVisit.get()
        print("! Processando: ", url)
        processUrl(url) 

if __name__ == "__main__":
    utils.initialize(queueUrlsToVisit)
    keywordsList = utils.loadFileLikeArray(consts.ARQ_KEYWORDS)
    queueUrlsVisited = utils.loadUrlsVisited(consts.ARQ_DATABASE)
    processQueue(begin)
