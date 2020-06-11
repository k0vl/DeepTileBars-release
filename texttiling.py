#!/usr/bin/env python3

import os
from nltk.tokenize import TextTilingTokenizer
import sys
from tqdm import tqdm


def texttiling(source_direc, dest_direc):

    files = os.listdir(source_direc)

    tokenizer = TextTilingTokenizer(k=6)

    def texttiling_doc(file_name):
        content = open(os.path.join(source_direc, file_name)).read()
        doc_id = file_name.split(".")[0]
        try:
            segments = tokenizer.tokenize(content)
            output = '\n\n'.join([segment.replace("\n", "\t") for segment in segments])
        except:
            raise

        with open(os.path.join(dest_direc, doc_id), "w") as f:
            print(output, file=f)

    for f in tqdm(files):
        texttiling_doc(f)

if __name__ == "__main__":
    texttiling(sys.argv[1], sys.argv[2])
