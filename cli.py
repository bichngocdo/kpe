import os
from collections import defaultdict

from kpe.base_structures import Document
from kpe.data import parse_xml_file
from kpe.document_frequency import DocumentFrequency
from kpe.tfidf import TfIdf

input_dir = '/data'
model_dir = 'tfidf'
n = 3
k = 30
tfidf_models = {}
allowed_languages = None
redundancy_removal = True


def extract_kp_xml_file(f, name: str = None):
    content = parse_xml_file(f)
    content = defaultdict(lambda: None, content)

    lang = content['lang_abs']
    # fall back: using the description for KPE if there is no abstract
    if lang is None:
        lang = content['lang_desc']

    text = content['abstract']
    # fall back: using the description for KPE if there is no abstract
    if text is None and content['description'] is not None:
        text = []

    if lang is not None and text is not None:
        if allowed_languages and lang not in allowed_languages:
            return None

        if lang not in tfidf_models:
            df_file = os.path.join(model_dir, 'docfreq_{}.tsv'.format(lang))
            if not os.path.exists(df_file):
                print('{}: not support language: {}'.format(name, lang))
                return None
            num_docs, doc_freq = DocumentFrequency.read_tsv(df_file)
            tfidf_models[lang] = TfIdf(
                document_frequency=doc_freq, num_documents=num_docs,
                language=lang, n=n
            )
            print('Load KPE model for language: {}'.format(lang))
        all_text = []
        all_text.extend(text)
        if content['lang_desc'] == lang and content['description'] is not None:
            all_text.extend(content['description'])
        if content['lang_claims'] == lang and content['claims'] is not None:
            all_text.extend(content['claims'])

        # Use all fields to compute term frequency
        model = tfidf_models[lang]
        document = model.read_text(all_text)
        all_candidates = model.extract_candidates(document)
        scores = model.score_candidates(all_candidates)

        # Extract candidates from abstract
        if text == []:  # fall back: using first 100 tokens of the description as abstract
            description = model.read_text(content['description'])
            limit = 100
            sentences = []
            for sentence in description.sentences:
                sentences.append(sentence[:limit])
                limit -= len(sentence)
                if limit <= 0:
                    break
            abstract = Document()
            abstract.sentences = sentences
            abstract.language = description.language
        else:
            abstract = model.read_text(text)

        candidates = model.extract_candidates(abstract)
        keyphrases = model.extract_keyphrases(candidates, scores, k=k, redundancy_removal=redundancy_removal)

        return keyphrases
    else:
        print('{}: has no abstract'.format(name))

    return None


if __name__ == '__main__':
    while True:
        name = input('Input file: ')
        try:
            path = os.path.join(input_dir, name)
            with open(path, 'r') as f:
                keyphrases = extract_kp_xml_file(f, path)
                if keyphrases is not None:
                    for kp, _ in keyphrases:
                        print(kp)
        except Exception as e:
            print(e)
