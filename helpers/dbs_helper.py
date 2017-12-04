import random

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

# return [(sense.id, sense.mark1, sense.mark2, sense.mark3), ...]
def get_senses_by_word(word):
    senses = []
    try:
        # LIKE %s or name LIKE %s or name LIKE %s or name LIKE %s
        # word, "% " + word + " %", "% " + word, word + " %",
        get_cursor().execute("""SELECT DISTINCT sense.id, item.name, sense.mark1, sense.mark2, sense.mark3 
                                        FROM sense
                                        JOIN
                                        item
                                        ON sense.id = item.sense_id WHERE name LIKE %s or name LIKE %s""",
        (word, "% " + word + " %"))
        sense = get_cursor().fetchall()
        if len(sense) > 0:
            sense = sense[0]
            if sense not in senses:
                senses.append(sense)
        else:
            pass
    except MySQLdb.IntegrityError:
        pass
    return senses

def check_existence_path(first, second):
    get_cursor().execute("""select * from synonym where sense_id_first = %s and sense_id_second = %s""", (first, second))
    exists = get_cursor().fetchall()
    if len(exists) > 0:
        return True
    else:
        return False

def get_mark_by_id(id):
    get_cursor().execute("""select mark1, mark2, mark3 from sense where id = %s""",
                         (id,))
    res = get_cursor().fetchall()
    if res is None:
        return None
    else:
        return res[0]

def get_all_neighbours(sense_id):
    get_cursor().execute("""select * from synonym where sense_id_first = %s""",
                             (sense_id,))
    exists = get_cursor().fetchall()
    if exists is not None:
        return [x[2] for x in exists]

# return [(sense.id, sense.mark1, sense.mark2, sense.mark3), ...]
def get_all_from_db():
    get_cursor().execute("""select sense.id, sense.mark1, sense.mark2, sense.mark3 from sense""")
    sentences = get_cursor().fetchall()
    return sentences

def get_all_sentences_by_sense(id):
    get_cursor().execute("""select sentence_id from sense_in_sentence where sense_id = %s""", (id,))
    sentence_ids = get_cursor().fetchall()
    sentences = []
    if sentence_ids is not None:
        for id in sentence_ids:
            get_cursor().execute("""select name from sentence where id = %s""", (id,))
            sentence = get_cursor().fetchall()
            sentences = sentences + list(sentence[0])
        return sentences
    else:
        return None

def save_sentences_to_dbs():
    with open("test3.txt", "r") as ins:
        for line in ins:
            sentence = line.rstrip('\n')
            print(sentence)
            try:
                get_cursor().execute("""insert into sentence (name) values (%s)""", (sentence, ))
            except MySQLdb.IntegrityError:
                continue
            # from helpers.model_helper import get_all_marks
            # marks = get_all_marks(sentence)
            # if marks is None:
            #     continue
            # try:
            #     for mark in marks:
            #         if mark is None:
            #             continue
            #         get_cursor().execute(
            #             """insert into sentence (name, sense_id) values (%s, %s)""",
            #             (sentence, mark[0]))
            # except MySQLdb.IntegrityError:
            #     continue
    get_db().commit()
    make_links()

def make_links():
    get_cursor().execute("""select id, name from sentence""")
    sentences = get_cursor().fetchall()
    if sentences is None:
        return
    else:
        for id, name in sentences:
            print(id, name)
            from helpers.model_helper import get_all_marks
            marks = get_all_marks(name)
            if marks is None:
                continue
            for mark in marks:
                get_cursor().execute("""insert into sense_in_sentence (sentence_id, sense_id) values (%s, %s)""", (id, mark[0]))
        get_db().commit()