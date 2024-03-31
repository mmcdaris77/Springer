import os 
import csv 
import re
from spacy.lang.en import English

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

with open(pat_data_file, 'r', newline='') as f:
    data = csv.reader(f, quotechar='"')

    for d in data:
        if d[0] == 'drug':
            drugs_list.append(add_space(d[1]))
        if d[0] == 'route':
            routes_list.append(add_space(d[1]))
        if d[0] == 'unit':
            units_list.append(add_space(d[1]))


# lower and dedup
drugs_list = list(set([x.lower() for x in drugs_list]))
routes_list = list(set([x.lower() for x in routes_list]))
units_list = list(set([x.lower() for x in units_list]))

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
    d_list = numeric_pattern + [string_pattern(x) for x in d.split(' ')]
    patterns.append({"label": "DOSE", "pattern": d_list, "id": "dose"})


nlp = English()
ruler = nlp.add_pipe("entity_ruler")


patterns += [
            {"label": "DOSE", "pattern": numeric_pattern + [{"LOWER": "mg"}, {"ORTH": "/"}, {"LOWER": "m²"}], "id": "dose"},
            {"label": "DOSE", "pattern": numeric_pattern + [{"LOWER": "mg"}, {"ORTH": "/"}, {"LOWER": "m"}], "id": "dose"},
            {"label": "RTE", "pattern": [{"LOWER": "im"}], "id": "rte"},
            {"label": "RTE", "pattern": [{"LOWER": "orally"}], "id": "rte"},
            {"label": "FRQ", "pattern": [{"LOWER": "once"}, {"LOWER": "daily"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "once"}, {"LOWER": "per"}, {"LOWER": "day"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "twice"}, {"LOWER": "daily"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "twice"}, {"LOWER": "per"}, {"LOWER": "day"}], "id": "frq"},
            {"label": "CYCL", "pattern": [{"IS_DIGIT": True}, {"LOWER": "cycles"}], "id": "cycle"},
            {"label": "FRQ", "pattern": [{"LOWER": "every"}, {"IS_DIGIT": True}, {"LOWER": "weeks"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "every"}, {"IS_DIGIT": True}, {"LOWER": "days"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "monthly"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "weekly"}], "id": "frq"},
            {"label": "FRQ", "pattern": [{"LOWER": "twice"}, {"LOWER": "a"}, {"LOWER": "day"}], "id": "frq"},
            {"label": "DUR", "pattern": [{"LOWER": "for"}, {"IS_DIGIT": True}, {"LOWER": "days"}], "id": "dur"},
            {"label": "DUR", "pattern": [{"LOWER": "for"}, {"IS_DIGIT": True}, {"LOWER": "years"}], "id": "dur"},
            {"label": "DUR", "pattern": [{"LOWER": "for"}, {"IS_DIGIT": True}, {"LOWER": "weeks"}], "id": "dur"}
            ]
ruler.add_patterns(patterns)

# save model to disk for future use
nlp.to_disk(os.path.join(me_dir, 'drug_ner_pipe'))





