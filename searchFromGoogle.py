import utils
import time
from googlesearch import search

def searchWeb():
    terms = listTermsForQueries()
    resultSearchGlobal = []
    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
    cont = 0
    for term in terms:
        # A cada 6 termos, o programa espera 1 minuto para prosseguir
        cont = cont + 1
        if ((cont % 4) == 0):
            print("## Aguardando 1 min ##")
            time.sleep(60)
        resultSearchByTerm = []
        saveUrls(["#######",term, "#######"])
        print("####### " ,term, " #######")
        for t in search(term, tld="com", lang="es", num=150, stop=150, pause=20, country="espanha", user_agent=userAgent):
            print(t)
            if (t not in resultSearchGlobal):
                resultSearchByTerm.append(t)
                resultSearchGlobal.append(t)
        saveUrls(resultSearchByTerm)
        # A cada pesquisa, aguardar 15 segundos
        print("## Aguardando 15 seg ##")
        time.sleep(15)
    print("-- FIM --")

def saveUrls(urls):
    utils.saveUrlsSearchers(urls)

def listTermsForQueries():
    # terms = ["Homeopatía", "Nosode",  "Samuel Hahnemann", "Industria homeopática Boiron", "Industria homeopática COFENAT", "Industria homeopática Homeopathy Research Institute", "Industria homeopática Observatorio de Terapias Naturales", "Industria homeopática Swiss Association of Homeopathic Physicians", "Industria homeopática SAHOP/SVHA", "Miasmas", "Ley de los similares", "Ley de los infinitesimales", "Agua polimerizada", "Memoria del agua", "Dilución homeopática", "Número de Avogadro", "Constante de Avogadro", "Prueba homeopática", "Repertorios homeopáticos", "Homeopathic Materia Medica", "Productos homeopáticos", "Tratamientos homeopáticos", "Medicina homeopática", "Remedios homeopáticos", "Homeópata"]
    
    # indicar quais os termos devem ser procurados, para evitar o erro 429, 4-5 termos por vez funcionam
    terms = ["Homeopatía", "Nosode",  "Samuel Hahnemann", "Industria homeopática Boiron", "Industria homeopática COFENAT", "Industria homeopática Homeopathy Research Institute", "Industria homeopática Observatorio de Terapias Naturales", "Industria homeopática Swiss Association of Homeopathic Physicians", "Industria homeopática SAHOP/SVHA", "Miasmas", "Ley de los similares", "Ley de los infinitesimales", "Agua polimerizada", "Memoria del agua", "Dilución homeopática", "Número de Avogadro", "Constante de Avogadro", "Prueba homeopática", "Repertorios homeopáticos", "Homeopathic Materia Medica", "Productos homeopáticos", "Tratamientos homeopáticos", "Medicina homeopática", "Remedios homeopáticos", "Homeópata"]
    return terms

if __name__ == "__main__":
    searchWeb()


 