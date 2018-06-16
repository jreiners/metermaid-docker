# ReName this file to dbConnect.py fill in hostname (eg. localhost or 127.0.0.1) and password
dbConn  = pymysql.connect(user='root', password='weatherdb', host='127.0.0.1', database='metermaid', autocommit=True)
