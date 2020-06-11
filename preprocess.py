#!/usr/bin/env python3

import utils
import json
import os, sys
import argparse
from tqdm import tqdm

# def generate_querymap():
#     query_map = {}
#     for line in tqdm(open("data/08.million-query-topics", encoding='iso-8859-1')):
#         qid, query = line.split(":")
#         query_map[qid] = ' '.join(utils.tokenize(query.strip()))
#     json.dump(query_map, open("data/query_map.json", "w"), indent=2)

def generate_querymap():
    '''Create a map from query id to query text'''
    print("generating query_map.json ...")
    query_map = {}
    for line in tqdm(open("data2/title-queries.301-450", encoding='iso-8859-1')):
        qid, query = line.split(" ", 1)
        query_map[qid] = ' '.join(utils.tokenize(query.strip()))
    json.dump(query_map, open("data2/query_map.json", "w"), indent=2)

def split_dataset(file):
    '''Create a list of documents that are relevant'''
    print("generating docs.json ...")
    docs = set()
    rels = {}
    for line in tqdm(file):
        query_id, _, doc_id, relevance = line.split()
        if int(relevance) > 0:
            docs.add(doc_id)
        if query_id not in rels:
            rels[query_id] = {}
        if relevance not in rels[query_id]:
            rels[query_id][relevance] = []
        rels[query_id][relevance].append(doc_id)

    json.dump(list(docs), open("data2/docs.json", 'w'))
    json.dump(rels, open("data2/qrels/rels_trec45.json", "w"), indent=2)

    #filter out queries that doesn't have a non-zero relevancy judegment 
    all_neg = set([i for i in rels if not ('1' in rels[i] or '2' in rels[i])])

    folds_test = []
    folds_train = []
    for fold in range(5):
        folds_test.append(open(os.path.join("data2/qrels", "trec45_S" + str(fold + 1) + ".txt"), "w"))
        folds_train.append(set())

    complete_output = open("data2/eval/trec45_test.txt", "w")
    file.seek(0)
    for line_idx, line in enumerate(tqdm(file)):
        query_id, _, doc_id, relevance = line.split()
        if query_id in all_neg:
            continue
        folds_test[line_idx % 5].write(line)
        [s.add(query_id) for i, s in enumerate(folds_train) if i != (line_idx % 5)]
        complete_output.write(f"{relevance} qid:{query_id} " + " ".join(f"{i}:0.000000" for i in range(1,47)) + f" #docid = {doc_id} inc = 1 prob = 0.0000000\n")
    complete_output.close()

    for fold in range(5):
        folds_test[fold].close()
        json.dump(list(folds_train[fold]), open("data2/qrels/trec45_train_" + str(fold+1) + ".json", "w"), indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocess data.')
    parser.add_argument('qrels',help="qrels file to use to generate docs.json", type=argparse.FileType('r'))
    args = parser.parse_args()

    generate_querymap()
    # split_dataset()
    if args.qrels:
        split_dataset(args.qrels)
