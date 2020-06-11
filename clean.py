#!/usr/bin/env python3

import json
from tqdm import tqdm

with open("data2/qrels/rels_trec45.json", 'r') as rels_fp, open("data2/docs.json", 'r') as docs_fp:
    rels = json.load(rels_fp)
    docs = json.load(docs_fp)
    for query in tqdm(rels):
        rels[query]['0'] = [doc for doc in rels[query]['0'] if doc in docs]
    json.dump(rels, open("data2/qrels/rels_trec45_2.json", "w"), indent=2)