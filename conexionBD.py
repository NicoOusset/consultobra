import pymysql

def conectar(HOST, DB, USER, PASS):

    db = pymysql.connect(host=HOST,
                        user=USER,
                    password=PASS,
                    db=DB)

    return db                

def desconectar(db):
    db.close()