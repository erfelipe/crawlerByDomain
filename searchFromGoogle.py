import utils
import time
from googlesearch import search

def searchWeb():
    """[summary]
        search function parameters:

        query : query string that we want to search for.
        tld : tld stands for top level domain which means we want to search our result on google.com or google.in or some other domain.
        lang : lang stands for language.
        num : Number of results we want.
        start : First result to retrieve.
        stop : Last result to retrieve. Use None to keep searching forever.
        pause : Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapse will make your program slow but its safe and better option.
        Return : Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.
    """    
    terms = listTermsForQueries()
    resultSearchGlobal = []
    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
    for term in terms:
        resultSearchByTerm = []
        saveUrls(["#######",term, "#######"])
        print("####### " ,term, " #######")
        for t in search(term, tld="com", lang="es", num=100, stop=100, pause=20, country="espanha", user_agent=userAgent):
            print(t)
            if (t not in resultSearchGlobal):
                resultSearchByTerm.append(t)
                resultSearchGlobal.append(t)
        saveUrls(resultSearchByTerm)
        time.sleep(15)

def saveUrls(urls):
    utils.saveUrlsSearchers(urls)

def listTermsForQueries():
    # terms = ["Homeopatía", "Nosode",  "Samuel Hahnemann", "Industria homeopática Boiron", "Industria homeopática COFENAT", "Industria homeopática Homeopathy Research Institute", "Industria homeopática Observatorio de Terapias Naturales", "Industria homeopática Swiss Association of Homeopathic", "Physicians", "Industria homeopática SAHOP/SVHA", "Miasmas", "Ley de los similares", "Ley de los infinitesimales", "Agua polimerizada", "Memoria del agua", "Dilución homeopática", "Número de Avogadro", "Constante de Avogadro", "Prueba homeopática", "Repertorios homeopáticos", "Homeopathic Materia Medica", "Productos homeopáticos", "Tratamientos homeopáticos", "Medicina homeopática", "Remedios homeopáticos", "Homeópata"]
    # indicar quais os termos devem ser procurados, para evitar o erro 429, 8 termos por vez funcionam
    terms = [ "Homeópata"]
    return terms

if __name__ == "__main__":
    searchWeb()


 