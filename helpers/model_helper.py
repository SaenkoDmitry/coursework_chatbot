import random
import re
from collections import Counter
from datetime import datetime

from numpy import sort
import operator

from helpers.dbs_helper import get_senses_by_word, get_all_from_db, check_existence_path, get_all_sentences_by_sense, \
    get_all_neighbours, get_mark_by_id


def check_coincidence():
    pass

# return return [(sense_id, sense.mark1, sense.mark2, sense.mark3), ...]
def get_all_marks(sentence):
    if len(sentence) < 1:
        return
    regex = re.compile('[^a-zA-Zа-яА-Я ]')
    sentence = sentence.lower()
    sentence = regex.sub('', sentence)
    sentence = sentence.split()
    output = []
    for word in sentence:
        senses = get_senses_by_word(word)
        senses = [x for x in senses if x[1] in sentence]
        if senses is None:
            continue
        output = output + senses
        # print("word : " + word + ", senses : " + str(senses))
    # print(output)
    return output

def get_center_mass(senses):
    mark1 = [x[1] for x in senses]
    mark2 = [x[2] for x in senses]
    mark3 = [x[3] for x in senses]
    return (sum(mark1) / len(mark1), sum(mark2) / len(mark2), sum(mark3) / len(mark3))

def check_distance(i, mark, j, mark2):
    radius = 0.3
    if i == j:
        return True
    elif abs(mark[0] - mark2[0]) <= radius and abs(mark[0] - mark2[0]) <= radius and abs(mark[0] - mark2[0]) <= radius:
        return True
    else:
        return False

def add_to_res(res, id):
    temp = get_all_sentences_by_sense(id)
    if temp is None:
        return
    for y in temp:
        if y not in res:
            res[y] = 1
        else:
            res[y] += 1

def get_result(input):
    senses = get_all_marks(input)
    within0 = [x[0] for x in senses]
    res = dict()
    senses_second = []
    res_second = dict()
    neighbours_global = []
    for id, name, *mark in senses:
        print('mark : ', id, mark)
        # neighbours = [id]
        neighbours = [id] + get_all_neighbours(id)
        print("neighbours ", id, " : ", neighbours)
        neighbours_global = neighbours_global + neighbours
        senses_second.append((id, neighbours))
    for id, name, *mark in senses:
        for id2 in neighbours_global:
            mark2 = get_mark_by_id(id2)
            if check_distance(id, mark, id2, mark2):
                add_to_res(res, id2)
    if len(res) > 0:
        print(res)
        max_key = max(list(res.values()))
        print(max_key)
        res = [key for key, value in res.items() if value == max_key]
        return random.choice(res)
    else:
        print('global ', neighbours_global)
        for x in neighbours_global:
            add_to_res(res_second, x)
        if len(res_second) > 0:
            res_second = [key for key, value in res_second.items() if value is max(list(res_second.values()))]
            return random.choice(res_second)
        else:
            return 'Пожалуйста, введите другое сообщение'