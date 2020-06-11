# DeepTileBars-release

Implementation of [DeepTileBars: Visualizing Term Distribution of Neural Information Retrieval](https://arxiv.org/abs/1811.00606)


## Dependencies
```
pyspark
nltk
BeautifulSoup
keras
krovetzstemmer
gensim
```
install these dependencies via

```pipenv install```

enter the virtual environment shell via

```pipenv shell```

## Running the model

### 0 Required files

* Trained gensim word2vec model: `data2/word2vec.100`

* Queries: `data2/title-queries.301-450`

* TREC45 documents: `data2/corpus/trec45-processed.xml`

* qrels: `data2/qrels.trec6-8.nocr`

Note: this repo uses Git LFS to store the large files. You may need to download these manually from github.com. 
 
### 1 Preprocessing
```bash
./preprocess.py data2/qrels.trec6-8.nocr
```

### 2 Extracting and cleaning documents
 ```bash
mkdir /data2/clean
./extract_file.py /path/to/corpus /data2/clean
```

### 3 TextTiling
```bash
mkdir /data2/segmented
./texttiling.py /data2/clean /data2/segmented
```

### 4 Coloring
```bash
mkdir /data2/images
./text2img.py  /data2/segmented /data2/images
```

### 5 Run the model
```bash
./rank.py /data2/images 5
```

## Citation

If you are using this repo, please cite the following paper:


    @inproceedings{deeptilebars2018,
        title={DeepTileBars: Visualizing Term Distribution for Neural Information Retrieval},
        author={Tang, Zhiwen and Yang, Grace Hui},
        journal={AAAI 2019},
        year={2019}
    }
