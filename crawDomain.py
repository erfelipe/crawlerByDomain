import queue
import utils
import requests
import consts
import colors

counter = 0
keywordsList = []
queueUrlsToVisit = queue.Queue() 
queueUrlsVisited = []

def urlNotVisited(url):
    return url not in queueUrlsVisited

def isDataText(header): 
    try:
        cabecalho = header['content-type']
        if ('ASCII'.lower() in cabecalho.lower()) or ('ANSI'.lower() in cabecalho.lower()) or ('8859'.lower() in cabecalho.lower()) or ('UTF'.lower() in cabecalho.lower()) or ('text'.lower() in cabecalho.lower()) or ('html'.lower() in cabecalho.lower()) :
            return True
        else:
            return False
    except:
        return False

def contentFromUrl(url):
    if (utils.urlWellFormat(url)):
        data = requests.Response
        try:
            data = requests.get(url, verify=False, timeout=5) 
        except requests.RequestException as e: 
            data.status_code = 400 
        if (data.status_code == requests.codes.ok) and (isDataText(data.headers)): 
            return data.text 
        else:
            print(colors.bcolors.FAIL + "@ Request NÃO É TEXTO: " + url + colors.bcolors.ENDC) 
            # print(colors.bcolors.FAIL + "@ " + data.headers['content-type'] + colors.bcolors.ENDC)
            return ""
    else:
            return ""

def keyswordsInDocument(data):
    keys = []
    for k in keywordsList:
        if k in data:
            keys.append(k)
    return keys

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
        allUrls = utils.allUrlsFromDocument(page) 
        # allUrls = utils.allUrlsFromPage(page)
        if (len(keywordsFound) > 0): 
            print(colors.bcolors.OKGREEN + "@ URL adicionada: ", url + colors.bcolors.ENDC) 
            utils.insertDataInDB(url, page, keywordsFound) 
        else:
            print(colors.bcolors.FAIL + "# URL sem keywords: ", url + colors.bcolors.ENDC) 
    else: 
        print(colors.bcolors.OKCYAN + "* URL já visitada: ", url + colors.bcolors.ENDC) 
    # se tiver keywords:
    # - lista todas as urls e cadastra na fila a visitar
    # - armazena: url, conteudo, quais keyswords foram encontradas
    # - coloca endereco na fila de visitadas
    queueUrlsVisited.append(url)
    addUrlsToVisit(allUrls)
    allUrls.clear()

def processQueue(counter):
    """ Process the queue with seeds and prior address
    """    
    while (counter < consts.VISIT_LIMIT) and (not queueUrlsToVisit.empty()):
        counter += 1
        url = queueUrlsToVisit.get()
        if (utils.isFileValid(url) and (url is not None)):
            print(colors.bcolors.OKBLUE + "! Processando: " + str(counter) + " - " + url + colors.bcolors.ENDC) 
            processUrl(url) 
        else:
            print(colors.bcolors.WARNING + "% Arquivo inválido: " + url + colors.bcolors.ENDC) 
    utils.saveQueueToVisit(queueUrlsToVisit)
    utils.saveUrlsVisited(queueUrlsVisited) 

if __name__ == "__main__":
    utils.initialize(queueUrlsToVisit)
    keywordsList = utils.loadFileLikeArray(consts.ARQ_KEYWORDS)
    queueUrlsVisited = utils.loadUrlsVisited(consts.ARQ_DATABASE)
    processQueue(counter)
    utils.exportDataBaseToXlsx(consts.ARQ_DATABASE) 
    utils.countKeyWordsFrmDB() 
    utils.madeCloudOfWords()