from openpyxl import Workbook 
import consts
import sqlite3

def countKeyWordsFromDB():
    wb = Workbook() 
    ws0 = wb.active 
    ws0.title = 'Quant-Keywords'
    ws1 = wb.create_sheet(title='Quant-Key-FromPage')
    conn = sqlite3.connect(consts.ARQ_DATABASE) 
    cursor = conn.cursor() 
    cursor.execute("""  select keys, keysFromPage 
                        from crawlerByDomain cbd  
                    """)
    result = cursor.fetchall()
    conn.commit()
    conn.close() 
    colection = {}
    colectionFromPage = {}
    for keys in result:
        if (keys[0]):
            terms = keys[0].split(",")
            for term in terms:
                termNoSpace = term.strip()
                if termNoSpace in colection:
                    value = colection.get(termNoSpace)
                    colection[termNoSpace] = value + 1
                else:
                    colection[termNoSpace] = 1
            terms.clear()
        if (keys[1]):
            terms = keys[1].split(",")
            for term in terms:
                termNoSpace = term.strip()
                if termNoSpace in colectionFromPage: 
                    value = colectionFromPage.get(termNoSpace) 
                    colectionFromPage[termNoSpace] = value + 1 
                else:
                    colectionFromPage[termNoSpace] = 1 
            terms.clear()

    for chave, valor in colection.items():
        ws0.append([chave, valor]) 

    for chave, valor in colectionFromPage.items():
        ws1.append([chave, valor]) 
    
    saveTxtToCloud(colection)

    wb.save(consts.ARQ_XLSQUANTKEYS)

def saveTxtToCloud(colect):
    str = ""
    for chave, valor in colect.items():
        str = str + ' '.join([chave for i in range(valor)]) + ' '
    str = str.strip()
    with open(consts.ARQ_TXTFORCLOUD, 'w', encoding="utf-8") as text_file:
        text_file.write(str)

if __name__ == "__main__":
        countKeyWordsFromDB()