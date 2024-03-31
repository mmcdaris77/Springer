import os 
import csv 
import re
from spacy.lang.en import English
from patterns_additions import A__DURATION_LIST, A__DRUGS_LIST, A__ROUTES_LIST, A__UNITS_LIST, A__FREQ_LIST, A__CYCLE_LIST

# https://spacy.io/usage/rule-based-matching#entityruler
'''
    create a rule based matching model using the output data from omop vocab
    and adding some additional patterns

    tags: 
        - DRG   -> DrugName
        - RTE   -> Therapy Route
        - DOSE  -> Dose
        - FRQ   -> Frequency
        - DUR   -> Duration
        - CYCL  -> Cycles
'''

me_dir = os.path.dirname(os.path.realpath(__file__))

pat_data_file = os.path.join(me_dir, 'pattern_data.csv')

RE_NON_ALPHNUM = r'[^0-9A-Za-z]'
# function to wrap non-alphnumeric chars with spaces and remove double spaces
add_space = lambda x : re.sub(RE_NON_ALPHNUM, lambda m: f' {m.group()} ' if m.group() else ' ' , x).replace('  ', ' ')

drugs_list = []
routes_list = []
units_list = []
freq_list = []
duration_list = []
cycle_list = []

# get pattern strings from omop output file
with open(pat_data_file, 'r', newline='') as f:
    data = csv.reader(f, quotechar='"')

    for d in data:
        if d[0] == 'drug':
            drugs_list.append(d[1])
        if d[0] == 'route':
            routes_list.append(d[1])
        if d[0] == 'unit':
            units_list.append(d[1])
        if d[0] == 'frq':
            freq_list.append(d[1])

# add additions
drugs_list += A__DRUGS_LIST
routes_list += A__ROUTES_LIST
units_list += A__UNITS_LIST
freq_list += A__FREQ_LIST
duration_list += A__DURATION_LIST
cycle_list += A__CYCLE_LIST


# lower and dedup
drugs_list = list(set([add_space(x.lower()) for x in drugs_list]))
routes_list = list(set([add_space(x.lower()) for x in routes_list]))
units_list = list(set([add_space(x.lower()) for x in units_list]))
duration_list = list(set([add_space(x.lower()) for x in duration_list]))
cycle_list = list(set([add_space(x.lower()) for x in cycle_list]))


# generate patterns
numeric_pattern = [{"TEXT": {"REGEX": r"((\d+(\.\d+)?)|(\.\d+))"}}]
string_pattern = lambda s: {'ORTH': s} if re.compile(RE_NON_ALPHNUM).match(s) else {'lower': s}

patterns = []
for d in drugs_list:
    d_list = [string_pattern(x) for x in d.split(' ')]
    patterns.append({"label": "DRG", "pattern": d_list, "id": "drg"})
for d in routes_list:
    d_list = [string_pattern(x) for x in d.split(' ')]
    patterns.append({"label": "RTE", "pattern": d_list, "id": "rte"})
for d in units_list:
    if d not in duration_list:
        d_list = numeric_pattern + [string_pattern(x) for x in d.split(' ')]
        patterns.append({"label": "DOSE", "pattern": d_list, "id": "dose"})
for d in freq_list:
    d_list = [string_pattern(x) for x in d.split(' ')]
    patterns.append({"label": "FRQ", "pattern": d_list, "id": "frq"})
for d in duration_list:
    d_list = [string_pattern(x) for x in d.split(' ')]
    patterns.append({"label": "DUR", "pattern": [{"LOWER": "for"}] + numeric_pattern + d_list, "id": "dur"})
for d in cycle_list:
    d_list = [string_pattern(x) for x in d.split(' ')]
    patterns.append({"label": "CYCL", "pattern": [{"IS_DIGIT": True}] + d_list, "id": "cycle"})


# add some additional custom patterns
    # ex: chars like superscript or non-standard FRQ patterns
patterns += [
            {"label": "DOSE", "pattern": numeric_pattern + [{"LOWER": "mg"}, {"ORTH": "/"}, {"LOWER": "m²"}], "id": "dose"},
            {"label": "FRQ", "pattern": [{"LOWER": "every"}, {"IS_DIGIT": True}, {"LOWER": "weeks"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "every"}, {"IS_DIGIT": True}, {"LOWER": "days"}], "id": "frq"}
            ]

# make the model
nlp = English()
ruler = nlp.add_pipe("entity_ruler")
ruler.add_patterns(patterns)

# save model to disk for future use
nlp.to_disk(os.path.join(me_dir, 'drug_ner_pipe'))





