# Top_250_Movie
***From Crawling to Imagined***

Important **Library** Used:
```
1. request
2. numpy
3. pandas
4. SqlAlchemy
5. pymysql
6. streamlit
7. matplotlib
```
[_Main link_](https://www.imdb.com/chart/top/?ref_=nv_mv_250) for Starting
---
## Describe Files
### [crawl.py]([crawl.py](https://github.com/Mahdi-mghs/Top_250_Movie/blob/master/crawl.py))
Running this script it's begin the crawlling process
> with normally connection it takes around 20 min for extract (*it shows in your terminal how much remain to completed*)

After Completing it creates a _CSV_ file named **movie** :fire:
---
### [Connector.ipynb]([connector.ipynb](https://github.com/Mahdi-mghs/Top_250_Movie/blob/master/connector.ipynb))
Create Database and Insert Data
> you need to create _schema\_test_ in your database after that you can run jupyter file

*Better to use .to_sql() Pandas function instead of "pymysql" library, next project corrected :)*
you can see your datas in _Workbench_ or _mysql.conncetor_ :atom:
---
### [dashboard.py](dashboard.py](https://github.com/Mahdi-mghs/Top_250_Movie/blob/master/dashboard.py))
**Streamlit** Script

you can follow this [link](https://github.com/)