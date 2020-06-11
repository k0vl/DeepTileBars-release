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

def genertae_docs_json(file):
    '''Create a list of documents that are relevant'''
    print("generating docs.json ...")
    docs = set()
    for line in tqdm(file):
        query_id, _, doc_id, relevance = line.split()
        if int(relevance) > 0:
            docs.add(doc_id)
    json.dump(list(docs), open("data2/docs.json", 'w'))

def split_dataset():
    os.makedirs("qrels", exist_ok=True)
    # docs = set()
    rels = {}
    topics = []

    #parse MQ2008
    for i in range(1, 6):
        qids = set()
        for line in open(os.path.join("MQ2008", "S" + str(i) + ".txt")):
            parts = line.split()
            r = parts[0]
            qid = parts[1].split(":")[-1]
            doc_id = parts[-7]

            if qid not in rels:
                rels[qid] = {}

            if r not in rels[qid]:
                rels[qid][r] = []
            rels[qid][r].append(doc_id)

            qids.add(qid)

        topics.append(qids)

    # json.dump(list(docs), open("data/docs.json", 'w'))
    json.dump(rels, open("qrels/rels08.json", "w"), indent=2)

    #filter out queries that doesn't have a non-zero relevancy judegment 
    all_neg = set([i for i in rels if not ('1' in rels[i] or '2' in rels[i])])

    topics = [[qid for qid in qids if qid not in all_neg] for qids in topics]

    cnt = 1

    complete_output = open("eval/MQ2008_test.txt", "w")
    simplified_output = open("qrels/MQ2008.txt", "w")
    for fold in [4, 0, 1, 2, 3]:
        test = set(topics[fold])
        train_folds = [i for i in [0, 1, 2, 3, 4] if i != fold]
        train = [topic for i in train_folds for topic in topics[i]]
        json.dump(train, open("qrels/MQ2008_train_" + str(cnt) + ".json", "w"), indent=2)

        simplified_per_fold = open(os.path.join("qrels", "MQ2008_S" + str(fold + 1) + ".txt"), "w")
        for line in open("MQ2008/S" + str(fold + 1) + ".txt"):
            parts = line.split()

            r = parts[0]
            qid = parts[1].split(":")[-1]
            doc_id = parts[-7]

            if qid not in test:
                continue
            simplified_str = "{} 0 {} {}\n".format(qid, doc_id, r)
            simplified_per_fold.write(simplified_str)
            simplified_output.write(simplified_str)
            complete_output.write(line)

        simplified_per_fold.close()
        cnt += 1
    complete_output.close()
    simplified_output.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='preprocess data.')
    parser.add_argument('qrels',help="qrels file to use to generate docs.json", type=argparse.FileType('r'))
    args = parser.parse_args()

    generate_querymap()
    # split_dataset()
    if args.qrels:
        genertae_docs_json(args.qrels)
