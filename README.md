# crawlerByDomain
## Web Crawler based in keywords domain subject

This project was created to allow the analysis of data (web pages) in a specific context.

Web Crawler is a type of software mainly used to create databases (inverted files) of Internet search engines. It has very specific characteristics in its development, in order to carry out feedback to collect data and store the visited pages.

In this project, the difference of this crawler in relation to others is its ability to allow filters by controlled vocabulary, to capture pages of the chosen theme.

An outline of how this software works can be seen in the figure below, where the main processes for its operation can be seen.

<img src="/img/Esquema.Homeopatia-us.jpg" alt="Schema CrawlerByDomain">

The main feature is the use of *controlled vocabulary* in the process of capturing web pages, in order to filter information that contains the theme of the study, eliminating hours of human evaluation.

**In the beginning for its functioning, some files must be configured:**
### A. Files to define the desired theme:
- urls-seeds.txt | Inform initial urls (*seeds*)
- keywords.txt | Inform the keywords for page filtering

### B. You can limit how many pages should be visited in this iteration 
- consts.py | File of configuration's options for files and consts 
> VISIT_LIMIT = 3000  

Change the value for how many pages to visit in this run.

### C. To use it
To use the program, it is recommended to use a virtual environment (VENV) and use the following file:
- crawDomain.py | The main file 

To start, use: 
> python crawDomain.py

*In its first use, you can create new database (empty) and new output files (spreadsheets) answering the initial questions (Y/N). For continue jobs, choose N.*

## As output, you can analyze the following files:
```
- data.sqlite | Database file [use DBeaver for open it]
- quant_keys.xlsx | Report for count keywords
- bd-result.xlsx | Report for pages and keys found
- keywordsFromVocabulary.png | WordCloud image
```

## Required python libraries:
- requests | https://pypi.org/project/requests/
- urllib | https://pypi.org/project/urllib3/
- sqlite3 | https://docs.python.org/3/library/sqlite3.html [native]
- wordcloud | https://pypi.org/project/wordcloud/
- bs4 | https://pypi.org/project/beautifulsoup4/
- urlextract | https://pypi.org/project/urlextract/
- openpyxl | https://pypi.org/project/openpyxl/