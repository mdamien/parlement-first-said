import json, re, sys

DEPUTES = json.load(open("deputes.json"))['deputes']
DEPUTES = {dep['depute']['id']:dep['depute'] for dep in DEPUTES}
SENATEURS = json.load(open("senateurs.json"))['senateurs']
SENATEURS = {dep['senateur']['id']:dep['senateur'] for dep in SENATEURS}

said = set()
def process(i, who):
    i = i['fields']
    inter = i['intervention'].replace('<p>', ' ').replace('</p>', ' ').replace('<i>', ' ').replace('</i>', ' ')
    for word in re.compile(r'[\w-]+').findall(inter):
        if len(word) > 1:
            if word[0].isupper() and word[1:].islower():
                # prénom / nom
                # oula faux positif "Goals"
                # continue
                pass
        found_number = False
        for n in '0123456789':
            if n in word:
                # truc avec numero
                found_number = True
                break
        if found_number:
            continue

        word_ = word.lower()
        if word_ not in said:
            pos = inter.index(word)
            debut = pos - 70
            if debut < 0:
                debut = 0
            fin = pos + 70 + len(word)
            if fin > len(inter):
                fin = len(inter) - 1

            if debut > 0:
                if inter[debut-1] != ' ':
                    try:
                        debut = inter.index(' ', debut)
                    except:
                        debut = 0
            if fin < len(inter) - 1:
                if inter[fin] != ' ':
                    fin = inter.rfind(' ', 0, fin)
                    if fin == -1:
                        fin = len(inter) - 1


            contexte = '"' + inter[debut:fin+1].strip() + '"'

            parl_id = i['parlementaire_id']
            if who == 'senateur':
                if parl_id in SENATEURS and SENATEURS[parl_id]['twitter']:
                    contexte += ' par ' + '@' + SENATEURS[parl_id]['twitter']
                contexte += f" https://nossenateurs.fr/seance/{i['seance_id']}#inter_{i['md5']}"
            else:
                if parl_id in DEPUTES and DEPUTES[parl_id]['twitter']:
                    contexte += ' par ' + '@' + DEPUTES[parl_id]['twitter']
                contexte += f" https://nosdeputes.fr/15/seance/{i['seance_id']}#inter_{i['md5']}"
            if word.lower() == word:
                print(json.dumps(word + '\n\n' + contexte, ensure_ascii=False))
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
        print(i_date, file=sys.stderr)
        process(i, "député")
        try:
            i = next(i_it)
        except StopIteration:
            i = None
        refresh_dates()

    while i2 and (i2_date <= i_date or i is None):
        print(i2_date, file=sys.stderr)
        process(i2, 'senateur')
        try:
            i2 = next(i2_it)
        except StopIteration:
            i2 = None
        refresh_dates()
