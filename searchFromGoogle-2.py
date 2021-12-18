import utils
import time
from serpapi import GoogleSearch
import json

def searchWeb(): 
    terms = listTermsForQueries()
    resultSearchGlobal = []
    userAgent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40'
    cont = 0
    for term in terms:
        # A cada n termos, o programa espera 1 minuto para prosseguir
        cont = cont + 1
        if ((cont % 4) == 0):
            print("## Aguardando 1 min ##")
            time.sleep(60)
        resultSearchByTerm = []
        saveUrls(["#######",term, "#######"])
        print("####### " ,term, " #######")
        results = GoogleSearch({
            "q": term,
            "location": "Region of Murcia, Spain",
            "api_key": "776b0f838bb3bc24924749ff72537cc21945a7cfd31cb0fd64029919165d2751"}).get_dict()
        # print(results)
        print(json.dumps(results, indent=4))

        
        # for item in results:
        #     print(item.link)
        #     if (item.link not in resultSearchGlobal):
        #         resultSearchByTerm.append(item.link)
        #         resultSearchGlobal.append(item.link)
        # saveUrls(resultSearchByTerm)
        # A cada pesquisa, aguardar 15 segundos
        print("## Aguardando 15 seg ##")
        time.sleep(15)
    print("-- FIM --")

def saveUrls(urls):
    utils.saveUrlsSearchers(urls)

def listTermsForQueries():
    # terms = ["Homeopatía", "Nosode",  "Samuel Hahnemann", "Industria homeopática Boiron", "Industria homeopática COFENAT", "Industria homeopática Homeopathy Research Institute", "Industria homeopática Observatorio de Terapias Naturales", "Industria homeopática Swiss Association of Homeopathic Physicians", "Industria homeopática SAHOP/SVHA", "Miasmas", "Ley de los similares", "Ley de los infinitesimales", "Agua polimerizada", "Memoria del agua", "Dilución homeopática", "Número de Avogadro", "Constante de Avogadro", "Prueba homeopática", "Repertorios homeopáticos", "Homeopathic Materia Medica", "Productos homeopáticos", "Tratamientos homeopáticos", "Medicina homeopática", "Remedios homeopáticos", "Homeópata"]
    # indicar quais os termos devem ser procurados, para evitar o erro 429, 8 termos por vez funcionam
    terms = ["Homeopatía", "Nosode",  "Samuel Hahnemann", "Industria homeopática Boiron", "Industria homeopática COFENAT", "Industria homeopática Homeopathy Research Institute", "Industria homeopática Observatorio de Terapias Naturales", "Industria homeopática Swiss Association of Homeopathic Physicians", "Industria homeopática SAHOP/SVHA", "Miasmas", "Ley de los similares", "Ley de los infinitesimales", "Agua polimerizada", "Memoria del agua", "Dilución homeopática", "Número de Avogadro", "Constante de Avogadro", "Prueba homeopática", "Repertorios homeopáticos", "Homeopathic Materia Medica", "Productos homeopáticos", "Tratamientos homeopáticos", "Medicina homeopática", "Remedios homeopáticos", "Homeópata"]
    return ["Homeopatía"]

if __name__ == "__main__":
    searchWeb()


 