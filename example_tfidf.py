from kpe.document_frequency import DocumentFrequency
from kpe.tfidf import TfIdf

text = [
    "A refillable hand - operated liquid sprayer of the type which requires no container pressurizing gas nor "
    "other foreign propellant."
    "It operates to pump a small quantity of liquid to be sprayed from a container to a small cylindrical chamber "
    "wherein the liquid is pressurized by the force of a coiled spring which is stressed during \"cocking\" "
    "stroke preparatory to spraying the liquid from the device."
    "A cover unit is removably mounted on the open end of the container, and a spray head is rotatably mounted on "
    "the cover unit, the rotation of the head relative to the unit causing the spring to be compressed and "
    "simultaneously sucking liquid up from the container into the chamber. "
]

# Read the document frequency from files and initialize the TfIdf model
# The following parameters of the keyphrase extractor must be set to the same ones
# that are used to extract document frequency: language, stemmer, normalization.
# n and stopword can be set less strict than when extracting document frequency.
num_docs, doc_freq = DocumentFrequency.read_tsv('tfidf/docfreq_en.tsv')
extractor = TfIdf(num_documents=num_docs, document_frequency=doc_freq, language='en',
                  n=3, stemmer=None, stopwords=True, normalization='stemming')

# Process the document with an NLP pipeline
document = extractor.read_text(text)

# Extract and score the candidates
candidates = extractor.extract_candidates(document)
scores = extractor.score_candidates(candidates)

# Using the scoring to extract top k keyphrases
keyphrases = extractor.extract_keyphrases(candidates, scores, 10, redundancy_removal=True)
for kw in keyphrases:
    print(kw)
