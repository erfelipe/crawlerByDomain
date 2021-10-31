from websearch import WebSearch

# web = WebSearch(['Gaetan Jonathan BAKARY', 'iTeam-S'])
web = WebSearch('Nosode')
webpages = web.pages
for wp in webpages[:20]:
   print(wp) 

