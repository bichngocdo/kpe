# Keyphrase Extraction

This repository contains the codes for the keyphrase extraction (KPE) task for patent documents.

## Table of Content

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Package Structure](#package-structure)
- [Challenge: Key Concept Extraction for Patent Documents](#challenge-key-concept-extraction-for-patent-documents)
- [Implementation](#implementation)
- [Usage](#usage)

## Installation

The project was tested with Python 3.8.

Step 1: Install the dependencies in [requirements.txt](requirements.txt).

```shell
pip install -r requirements.txt
```

Step 2: Download spaCy models for all supported languages (e.g., English, German) in ISO 639-1 codes.

```shell
python -m spacy download en
python -m spacy download de
```

## Quick Start

- See [example_compute_df.py](example_compute_df.py) for how to extract document frequency statistics.
- See [example_tfidf.py](example_tfidf.py) for how to run an TF-IDF Keyphrase Extractor.
- See [example_textrank.py](example_textrank.py) for how to run a TextRank Keyphrase Extractor.

## Package Structure

See [kpe/README.md](kpe/README.md)

## Challenge: Key Concept Extraction for Patent Documents

### Task description

A patent is stored in an XML format. It has 3 text fields: ``abstract``, ``description`` and ``claims``
corresponding to 3 tags of the same name in the XML file. Each of these tags has an attribute ``lang`` indicating the
language of the field. Note that not all patients have all 3 fields and the languages of the 3 fields are not necessary
the same. If a patient has no abstract, use the *first 100 words* of the description as abstract.

The goal of this task is to enrich patent documents by extracting **30** key concepts (or keyphrases) from the abstract
so that users can later quickly review documents by looking only at the keyphrases.

### Solution: TF-IDF

This task belongs to the *unsupervised keyphrase extraction* (KPE) problem. One of the simplest but effective approach
for this problem is to extract keyphrases based on TF-IDF scores.

First, we need to compute the document frequency in our data. Run:

```shell
python compute_document_frequency.py --input data --output tfidf -n 3 --stopwords  --tags abstract
```

to extract term up to 3-gram from the input folder ``data`` and save the computed document frequency to the output
folder ``tfidf``. The script can be configured with option ``--tags`` to use all 3 text fields to compute the document
frequency.
``data`` is a folder containing compressed files ``.tgz``, each file contains patents in ``.xml`` format. The document
frequency of *each language* is saved in a separate file in the output folder ``tfidf``. In practice, since there are
more data in English than in German, the document frequency is computed using these commands:

```shell
python compute_document_frequency.py --input data --output tfidf -n 3 --stopwords  --languages en --tags abstract
python compute_document_frequency.py --input data --output tfidf -n 3 --stopwords  --languages de
```

After that, keyphrase extraction is performed by running:

```shell
python run_tfidf.py --input data --model tfidf --output results.csv -n 3 -k 30 --stopwords --tags abstract --redundancy_removal True
```

The command extracts top 30 keyphrases up to 3-gram and save the output to ``results.csv``. In the same manner, the
script can be configured with option ``--tags`` to use all 3 text fields to compute the term frequency, but keyphrases
are only extracted from the abstract.

Run each script with option ``-h`` to learn more about its parameters.

The results are stored in ``.csv`` format and can be effectively query using ``pandas``. The demo script for querying
keyphrases is [retrieve_keyphrases.py](retrieve_keyphrases.py). Start a ``python`` interpreter and run:

```python
from retrieve_keyphrases import keyphrases

keyphrases('AU6027B1.xml')
```

to see the extracted keyphrases of a particular document.

### Solution: TextRank

TextRank is another unsupervised KPE method based on graphs. Unlike TF-IDF, it does not rely on pre-computed statistics.

TextRank can be run in a very simple way:

```shell
python run_textrank.py < patent_file.xml
```

The parameters can be seen and adjusted in the script.

### Docker: TF-IDF

Requirements: Docker is installed and the Docker server is running.

Step 1: Build the Docker image

```shell
docker build --tag kpe-tfidf -f docker/tfidf/Dockerfile .
```

Step 2: Mount the local folder containing ``.xml`` documents to ``/data`` in the docker container and start the docker
image

```shell
docker run -v /absolute/path/data/in/your/machine:/data -it kpe-tfidf
```

Step 3: Keyphrase extraction. The prompt will ask for the name of the file you want to extract from:

```shell
Input file:
```

Type a name (e.g. ``AT508B.xml``), press Enter. The program will display a list of ranked keyphrases.

### Docker: TextRank

Requirements: Docker is installed and the Docker server is running.

Step 1: Build the Docker image

```shell
docker build --tag kpe-textrank -f docker/textrank/Dockerfile .
```

Step 2: Keyphrase extraction

```shell
docker run -i kpe-textrank < patent_file.xml
```

### Delivery

- Package [``kpe``](kpe): see [kpe/README.md](kpe/README.md) for the package information
- [compute_document_frequency.py](compute_document_frequency.py)
- [run_tfidf.py](run_tfidf.py)
- [retrieve_keyphrases.py](retrieve_keyphrases.py)
- [cli.py](cli.py)
- [run_textrank.py](run_textrank.py)
- Document frequency is in folder [tfidf](tfidf).
- Results of the TF-IDF model are in file [results_tfidf.csv](results_tfidf.csv).

### Note on language support

In theory, the program can process documents in *any* language as long as there is a spaCy model of that language. The
model for a language need to be downloaded *before* running the scripts. To download models, see step 2
in [Installation](#installation).

If the script ``compute_document_frequency.py`` encounter a language but cannot find the corresponding model, it will
print out a warning:

```
Warning: AT508B.xml: no spaCy model for language: de
```

However, there is no need to stop the script. You can later rerun it *only* on documents with specific languages defined
with option ``--languages``, for example ``--languages de fr``.

### Ideas for Improvement

- TF-IDF is only one of the available unsupervised approaches for KPE, so it is advisable to try and/or combine with
  other KPE approaches to see which one is more suitable for this type of data.
- Supervised methods are generally superior to unsupervised methods. Using a combination of labeled and synthetic (from
  unsupervised approach) data in a semi-supervised self-training approach is shown to improve *keyphrase generation*
  over models trained with only labeled data ([Ye and Wang, 2018](https://aclanthology.org/D18-1447/)).
- Parallel or distributed computing (e.g. MapReduce) can reduce the running time.

## Implementation

Package ``kpe`` implements the following keyphrase extraction systems:

- Unsupervised
    - Statistical
        - [**TF-IDF**](kpe/tfidf.py)
    - Graph
        - [**TextRank**](kpe/textrank.py)

The codes are reusable and the [base model](kpe/base_kpe.py) can easily be extended to add different keyphrase
extraction methods.

## Usage

### TF-IDF

TF-IDF is an unsupervised, statistical-based method for KPE. As its name suggests, it ranks keyphrase candidates based
on the TF-IDF scores.

Parameters:

- ``language``: language of documents, must be set to process documents correctly
- ``stemmer``: stemmer to extract the stem of a word. If there is no available stemmer for the current language, the
  stems fall back to the lemmas of words
- ``stopwords``: type of stopwords used to filter candidates
- ``normalization``: type of normalization used for a term, either by lowercasing or stemming

Step 1: Compute document frequency

As a statistical-based KPE method, TF-IDF relies on statistics of data, *document frequency*. An example of how to
compute document frequency can be seen in [example_compute_df.py](example_compute_df.py). Document frequency can be
computed *less strict* than when using it. For example:

- The maximum size of *n*-grams, ``n`` can be set to ``5`` for document frequency computation, and ``3`` for KPE.
- Filtering *n*-gram by stopword can be disabled for document frequency computation (``stopwords=False``) and enabled
  for KPE.

Step 2: Keyphrase extraction

An example of how to extract keyphrases using TF-IDF can be seen in [example_tfidf.py](example_tfidf.py).

### TextRank

TextRank ([Mihalcea and Tarau, 2004](https://aclanthology.org/W04-3252/)) is an unsupervised KPE method based on
PageRank.

Parameters:

- ``pos``: part of speech tags to be selected as a vertex
- ``window``: size of the co-occurrence window
- ``top``: use only the top percentage of vertices for KPE

An example of how to extract keyphrases using TF-IDF can be seen in [example_textrank.py](example_textrank.py).
