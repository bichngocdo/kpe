from kpe.textrank import TextRank

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

# Initialize the TextRank model
extractor = TextRank(pos={'NOUN', 'PNOUN', 'ADJ'}, window=3, top=0.33,
                     language='en', normalization='lowercase')

# Process the document with an NLP pipeline
document = extractor.read_text(text)

# Build the word graph and score words
graph = extractor.build_graph(document)
scores = extractor.score_candidates(graph)

# Extract candidates
candidates = extractor.extract_candidates(document, scores.keys())

# Using the scoring to extract top k keyphrases
keyphrases = extractor.extract_keyphrases(candidates, scores, 10, redundancy_removal=True)
for kw in keyphrases:
    print(kw)
