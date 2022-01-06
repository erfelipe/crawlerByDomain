from openpyxl import Workbook 
import consts
import sqlite3

def exportDataBaseToXlsx():
    wb = Workbook() 
    ws0 = wb.active 
    ws0.title = 'Craw-Homeopatia' 

    conn = sqlite3.connect(consts.ARQ_DATABASE) 
    cursor = conn.cursor() 
    cursor.execute("""  select *
                        from crawlerByDomain cbd  
                    """)
    result = cursor.fetchall()
    conn.close() 
    ws0.append(["id", "domain", "url", "page", "keys", "quantkeys", "titleFromPage", "keysFromPage", "langFromPage", "descFromPage", "authorFromPage"])
    for line in result: 
        ws0.append([line[0], line[1], line[2], line[3], line[4], line[5], line[6], line[7], line[8], line[9], line[10]])
    wb.save(consts.ARQ_XLSRESULT)

if __name__ == "__main__":
    exportDataBaseToXlsx()