import sys
from collections import defaultdict

from kpe.base_structures import Document
from kpe.data import parse_xml_file
from kpe.textrank import TextRank

pos = {'NOUN', 'PNOUN', 'ADJ'}
window = 3
top = 0.33
k = 30
textrank_models = {}
redundancy_removal = True


def extract_kp_xml_file(f):
    content = parse_xml_file(f)
    content = defaultdict(lambda: None, content)

    lang = content['lang_abstract']
    # fall back: using the description for KPE if there is no abstract
    if lang is None:
        lang = content['lang_description']

    text = content['abstract']
    # fall back: using the description for KPE if there is no abstract
    if text is None and content['description'] is not None:
        text = []

    if lang is not None and text is not None:
        if lang not in textrank_models:
            textrank_models[lang] = TextRank(
                pos=pos, window=window, top=top,
                language=lang, spacy_model=None, stemmer=None,
                normalization='lowercase',
            )

        model = textrank_models[lang]

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

        graph = model.build_graph(abstract)
        scores = model.score_candidates(graph)

        candidates = model.extract_candidates(abstract, scores.keys())
        keyphrases = model.extract_keyphrases(candidates, scores, k=k, redundancy_removal=redundancy_removal)

        return keyphrases
    else:
        print('File has no abstract')

    return None


if __name__ == '__main__':
    keyphrases = extract_kp_xml_file(sys.stdin)
    if keyphrases is not None:
        for kp, _ in keyphrases:
            print(kp)
