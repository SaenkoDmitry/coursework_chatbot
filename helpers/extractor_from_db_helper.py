import MySQLdb
import scipy.io

db = MySQLdb.connect(host="localhost",  # your host
                         user="root",  # username
                         passwd="root",  # password
                         db="poemsdb",
                     charset="utf8")  # name of the database

cursor = db.cursor()

def get_cursor():
    global cursor
    return cursor

def get_db():
    global db
    return db

def add_from_mat_Dic():
    f = scipy.io.loadmat('resources/Dic.mat', squeeze_me=True)
    x = f['Dic']
    for i, words in enumerate(x):
        print(i)
        words = [x for x in words if x != []]
        for y in words:
            try:
                s = """insert into item (sense_id, name) values (%s, %s)"""
                get_cursor().execute(s, (i, y))
            except MySQLdb.IntegrityError:
                continue
    get_db().commit()

def add_from_mat_x():
    f = scipy.io.loadmat('resources/x.mat', squeeze_me=True)
    x = f['x']
    for i, marks in enumerate(x):
        print(i)
        try:
            s2 = """insert into sense (id, mark1, mark2, mark3) values (%s, %s, %s, %s)"""
            get_cursor().execute(s2, (i, marks[0], marks[1], marks[2]))
        except MySQLdb.IntegrityError:
            continue
    get_db().commit()

def add_from_mat_ww():
    f = scipy.io.loadmat('resources/ww.mat', squeeze_me=True)
    ww = f['ww']
    print(len(ww))
    ww = [x for x in ww if x[2] == 1]
    for i, elem in enumerate(ww):
        print(i)
        try:
            s2 = """insert into synonym (sense_id_first, sense_id_second) values (%s, %s)"""
            get_cursor().execute(s2, (elem[0], elem[1]))
        except MySQLdb.IntegrityError:
            continue
    get_db().commit()