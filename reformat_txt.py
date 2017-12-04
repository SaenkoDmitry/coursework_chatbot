from helpers.model_helper import get_result

if __name__ == '__main__':
    f = open('test3.txt', 'r')
    ls = []
    for i in f:
        i = i.lstrip().rstrip()
        if i == '' or len(i) < 10 or '{' in i or not (i.endswith('.') or i.endswith('!')):
            continue
        ls.append(i)
    f.close()
    f1 = open('test3.txt', 'w')
    for i in ls:
        f1.write(i + '\n')
    f1.close()