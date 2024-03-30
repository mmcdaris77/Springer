import os 
import csv 
import json
from spacy.lang.en import English
from spacy import displacy

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

drugs_list = []
routes_list = []
units_list = []

with open(pat_data_file, 'r', newline='') as f:
    data = csv.reader(f, quotechar='"')

    for d in data:
        if d[0] == 'drug':
            drugs_list.append(d[1])
        if d[0] == 'route':
            routes_list.append(d[1])
        if d[0] == 'unit':
            units_list.append(d[1])

# lower and dedup
drugs_list = list(set([x.lower() for x in drugs_list]))
routes_list = list(set([x.lower() for x in routes_list]))
units_list = list(set([x.lower() for x in units_list]))

patterns = []
for d in drugs_list:
    d_list = [{'lower': x} for x in d.split(' ')]
    patterns.append({"label": "DRG", "pattern": d_list, "id": "drg"})
for d in routes_list:
    d_list = [{'lower': x} for x in d.split(' ')]
    patterns.append({"label": "RTE", "pattern": d_list, "id": "rte"})
for d in units_list:
    d_list = [{"IS_DIGIT": True}] + [{'lower': x} for x in d.split(' ')]
    patterns.append({"label": "DOSE", "pattern": d_list, "id": "dose"})


nlp = English()
ruler = nlp.add_pipe("entity_ruler")


patterns += [
            {"label": "DOSE", "pattern": [{"IS_DIGIT": True}, {"LOWER": "mg"}, {"ORTH": "/"}, {"LOWER": "m²"}], "id": "dose"},
            {"label": "DOSE", "pattern": [{"IS_DIGIT": True}, {"LOWER": "mg"}, {"ORTH": "/"}, {"LOWER": "m"}], "id": "dose"},
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
            {"label": "DUR", "pattern": [{"LOWER": "for"}, {"IS_DIGIT": True}, {"LOWER": "days"}], "id": "dur"},
            {"label": "DUR", "pattern": [{"LOWER": "for"}, {"IS_DIGIT": True}, {"LOWER": "years"}], "id": "dur"},
            {"label": "DUR", "pattern": [{"LOWER": "for"}, {"IS_DIGIT": True}, {"LOWER": "weeks"}], "id": "dur"}
            ]
ruler.add_patterns(patterns)

# save model to disk for future use
nlp.to_disk(os.path.join(me_dir, 'drug_ner_pipe'))





