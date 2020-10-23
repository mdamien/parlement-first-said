import json, re

said = set()
def process(i, who):
    i = i['fields']
    inter = i['intervention']
    for word in re.compile(r'\w+').findall(inter):
        if len(word) > 1:
            if word[0].isupper() and word[1:].islower():
                # prénom / nom
                continue
        found_number = False
        for n in '0123456789':
            if n in word:
                # truc avec numero
                found_number = True
                break
        if found_number:
            break

        word_ = word.lower()
        if word_ not in said:
            print(i['date'], word)
            pos = inter.index(word)
            debut = pos - 50
            if debut < 0:
                debut = 0
            fin = pos + 50
            if fin > len(inter):
                fin = len(inter) - 1
            print('      contexte:', inter[debut:fin])
            print('      url     :', f"https://nosdeputes.fr/seance/{i['seance_id']}#inter_{i['md5']}")
        said.add(word_)

def read_i():
    for file in ('result13.jsonl', 'result14.jsonl', 'result.jsonl'):
        for line in open(file):
            yield json.loads(line)[0]

def read_i2():
    for line in open('result_senat.jsonl'):
        yield json.loads(line)[0]

i_it = read_i()
i = next(i_it)
i2_it = read_i2()
i2 = next(i2_it)

last_i_date = None
last_i2_date = None
while i or i2:
    i_date, i2_date = None, None
    def refresh_dates():
        global i_date, i2_date, last_i_date, last_i2_date
        if i:
            if i['fields']['date']:
                i_date = i['fields']['date']
                last_i_date = i_date
            else:
                i_date = last_i_date
        else:
            i_date = last_i_date

        if i2:
            if i2['fields']['date']:
                i2_date = i2['fields']['date']
                last_i2_date = i2_date
            else:
                i2_date = last_i2_date
        else:
            i2_date = last_i2_date

    refresh_dates()
    while i and (i_date <= i2_date or i2 is None):
        process(i, "député")
        try:
            i = next(i_it)
        except StopIteration:
            print('end of i file')
            i = None
        refresh_dates()

    while i2 and (i2_date <= i_date or i is None):
        process(i2, 'senateur')
        try:
            i2 = next(i2_it)
        except StopIteration:
            print('end of i2 file')
            i2 = None
        refresh_dates()
