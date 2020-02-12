from textblob import TextBlob


text = '''
The lesson was prety bad. I did not like it. The instructor was boring, like a GridLayout. It was boring, uninteresting, stupid, horrible, but fun at the same time.
The TableView cell was pretty bad, the IndexPath.row was not very intuitive, and swift is complex such that the View Controller does not have classes but @selectors.
'''
blob = TextBlob(text)
print(blob.correct())
blob = blob.correct() # EXPERIMENTAL
adjectives = []
for item in blob.tags:
    if item[1] == 'JJ' or item[1] == 'JJR' or item[1] == 'JJS':
        adjectives.append(item[0])

print(adjectives)
blob.noun_phrases   # WordList(['titular threat', 'blob',
                    #            'ultimate movie monster',
                    #            'amoeba-like mass', ...])

for sentence in blob.sentences:
    print(sentence.sentiment.polarity)
# 0.060
# -0.341

blob.translate(to="es")  # 'La amenaza titular de The Blob...'
