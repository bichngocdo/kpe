from kpe.document_frequency import DocumentFrequency

texts = [
    "A refillable hand - operated liquid sprayer of the type which requires no container pressurizing gas nor "
    "other foreign propellant.",
    "It operates to pump a small quantity of liquid to be sprayed from a container to a small cylindrical chamber "
    "wherein the liquid is pressurized by the force of a coiled spring which is stressed during \"cocking\" "
    "stroke preparatory to spraying the liquid from the device.",
    "A cover unit is removably mounted on the open end of the container, and a spray head is rotatably mounted on "
    "the cover unit, the rotation of the head relative to the unit causing the spring to be compressed and "
    "simultaneously sucking liquid up from the container into the chamber. ",
]

extractor = DocumentFrequency(language='en', n=5,
                              stemmer=None, stopwords=False, normalization='stemming')

# Go through documents and count (up to) n-grams
for text in texts:
    document = extractor.process(text)

print('Num docs:', extractor.num_docs)
print('Num terms:', len(extractor))

# Save document frequency to file
extractor.to_tsv('example_tfidf.tsv')
