import queue
import utils
import requests
import consts
import colors
import urllib3
import validators 

pagesVisited = 0
validDomains = 0
keywordsList = []
queueUrlsVisited = []
queueUrlsToVisit = queue.Queue() 

def contentFromUrl(url):
    data = requests.Response
    try:
        data = requests.get(url, verify=False, timeout=5) 
    except requests.RequestException as e: 
        print(colors.bcolors.FAIL + "* request.get with Exception: " + url + colors.bcolors.ENDC) 
        data.status_code = 400 
    if (data.status_code == requests.codes.ok): #and (utils.isDataText(data.headers)) 
        return data.text 
    else:
        print(colors.bcolors.FAIL + "@ Request NÃO É TEXTO: " + url + colors.bcolors.ENDC) 
        # print(colors.bcolors.FAIL + "@ " + data.headers['content-type'] + colors.bcolors.ENDC)
        return ""

def addUrlsToVisit(urls):
    for url in urls:
        if validators.url(url) and utils.urlWellFormat(url) and not(utils.urlInBlackList(url) and utils.isFileValid(url)):
            queueUrlsToVisit.put(url)

def processUrl(url):
    """ For each url, process it

    Args:
        url (str): internet address 
    """ 
    global validDomains
    allUrls = []
    keywordsFound = []
    if (utils.urlNotVisited(url, queueUrlsVisited) and not(utils.urlInBlackList(url))):
        page = contentFromUrl(url)
        keywordsFound = (utils.keyswordsInDocument(page, keywordsList))
        allUrls = utils.allUrlsFromDocument(page) 
        # allUrls = utils.allUrlsFromPage(page)
        if (len(keywordsFound) > 0): 
            print(colors.bcolors.OKGREEN + "@@ URL added: ", url + colors.bcolors.ENDC) 
            utils.insertDataInDB(url, page, keywordsFound) 
            validDomains += 1
            if (validDomains % consts.RECORD_EACH == 0):
                print(colors.bcolors.OKCYAN + "$ Valid Domains: ", str(validDomains) + " of pages visited: " + str(pagesVisited) + colors.bcolors.ENDC) 
                utils.insertQuantsInDB(pagesVisited, validDomains)
        else:
            print(colors.bcolors.WARNING + "# URL without keywords: ", url + colors.bcolors.ENDC) 
    else: 
        print(colors.bcolors.FAIL + "* URL already visited or in black list: ", url + colors.bcolors.ENDC) 

    queueUrlsVisited.append(url)
    addUrlsToVisit(allUrls)
    allUrls.clear()

def processQueue():
    """ Process the queue with seeds and prior address
    """    
    global pagesVisited
    while (validDomains < consts.VISIT_LIMIT) and (not queueUrlsToVisit.empty()):
        pagesVisited += 1
        url = queueUrlsToVisit.get()
        if (utils.isFileValid(url) and (url is not None) and utils.urlWellFormat(url) ):
            print(colors.bcolors.OKBLUE + "Processando: " + str(pagesVisited) + " - " + url + colors.bcolors.ENDC) 
            processUrl(url) 
        else:
            print(colors.bcolors.WARNING + "% Arquivo inválido: " + url + colors.bcolors.ENDC) 
    
    utils.saveQueueToVisit(queueUrlsToVisit)
    utils.saveUrlsVisited(queueUrlsVisited) 

if __name__ == "__main__":
    urllib3.disable_warnings()
    utils.initialize(queueUrlsToVisit, keywordsList, queueUrlsVisited)
    processQueue()
    # utils.exportDataBaseToXlsx() 
    # utils.countKeyWordsFrmDB() 
    # utils.madeCloudOfWords() 

